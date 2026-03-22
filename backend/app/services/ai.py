import logging
import os
from openai import AsyncOpenAI
from datetime import datetime

logger = logging.getLogger(__name__)


class OpenAIFinancialAI:

    def __init__(self, stock_service, company_service):
        self.stock_service = stock_service
        self.company_service = company_service
        self.client = None
        self._init_client()

    def _init_client(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY not set")
            return
        self.client = AsyncOpenAI(api_key=api_key)

    async def process_query(self, query):
        return await self._answer(query)

    async def _answer(self, question):
        if not self.client:
            return {"type": "error", "message": "AI service not available. Check your OpenAI API key."}

        try:
            tickers = await self._extract_tickers(question)
            financial_data = await self._fetch_financial_data(tickers)

            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user", "content": self._build_prompt(question, financial_data)}
                ],
                max_tokens=1500,
                temperature=0.3  # low temperature keeps responses factual and grounded
            )

            answer = response.choices[0].message.content
            return {
                "type": self._classify(question),
                "message": answer,
                "companies_analyzed": tickers,
                "has_real_time_data": len(financial_data.get("companies", {})) > 0,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return {"type": "error", "message": "Failed to process your request. Please try again."}

    async def _extract_tickers(self, question):
        """Pull potential tickers and company names out of the question text."""
        tickers = []
        words = question.split()
        candidates = []

        # Uppercase words 2–5 chars are likely ticker symbols
        for word in words:
            clean = word.strip('.,!?()[]{}":;')
            if 2 <= len(clean) <= 5 and clean.isupper():
                candidates.append(clean)

        # Words near company indicators (Inc, Corp, etc.) are likely company names
        indicators = {'corporation', 'corp', 'company', 'inc', 'ltd', 'llc', 'group', 'holdings'}
        for i, word in enumerate(words):
            if word.lower().strip('.,!?()[]{}":;') in indicators:
                start = max(0, i - 2)
                candidates.append(' '.join(words[start:i + 1]).strip('.,!?()[]{}":;'))

        # Also try individual alpha words as company name searches
        for word in words:
            clean = word.strip('.,!?()[]{}":;')
            if len(clean) > 2 and clean.isalpha():
                candidates.append(clean)

        for term in candidates[:10]:
            try:
                results = await self.company_service.search_companies(term)
                if results:
                    ticker = results[0].get('ticker')
                    if ticker and ticker not in tickers:
                        tickers.append(ticker)
                        if len(tickers) >= 5:
                            break
            except Exception as e:
                logger.warning(f"Search failed for '{term}': {e}")

        return tickers

    async def _fetch_financial_data(self, tickers):
        data = {"market_timestamp": datetime.now().isoformat(), "companies": {}}

        for ticker in tickers:
            try:
                company_info = await self.company_service.get_company_by_ticker(ticker)
                stock_info = self.stock_service.get_stock_data(ticker)

                if company_info and stock_info and 'error' not in stock_info:
                    data["companies"][ticker] = {
                        "basic_info": {
                            "name": company_info.get('name', 'Unknown'),
                            "sector": company_info.get('sector', 'Unknown'),
                            "employees": company_info.get('employees', 'N/A')
                        },
                        "current_price": stock_info.get('current_price'),
                        "change_percent": stock_info.get('change_percent'),
                        "volume": stock_info.get('volume'),
                        "pe_ratio": stock_info.get('pe_ratio'),
                        "market_cap": stock_info.get('market_cap')
                    }
            except Exception as e:
                logger.error(f"Failed to fetch data for {ticker}: {e}")

        return data

    def _system_prompt(self):
        return (
            "You are a financial AI assistant with access to real-time market data. "
            "Use the data provided to answer questions factually and concisely. "
            "For comparisons, analyze all companies. For general questions, provide educational insight. "
            "Always note that responses are for informational purposes and not financial advice."
        )

    def _build_prompt(self, question, financial_data):
        prompt = f"Question: {question}\n\n"
        companies = financial_data.get("companies", {})

        if companies:
            prompt += f"Real-time data (as of {financial_data['market_timestamp']}):\n\n"
            for ticker, d in companies.items():
                prompt += f"**{ticker} — {d['basic_info']['name']}**\n"
                prompt += f"  Sector: {d['basic_info']['sector']}\n"
                prompt += f"  Price: ${d['current_price']} ({d['change_percent']:.2f}%)\n"
                prompt += f"  Volume: {d['volume']}\n"
                prompt += f"  P/E: {d['pe_ratio']} | Market Cap: {d['market_cap']}\n"
                prompt += f"  Employees: {d['basic_info']['employees']}\n\n"
        else:
            prompt += "No specific company data found for this query.\n\n"

        return prompt

    def _classify(self, question):
        q = question.lower()
        if any(w in q for w in ['compare', 'versus', 'vs', 'between']):
            return 'comparison'
        if any(w in q for w in ['price', 'cost', 'trading', 'worth']):
            return 'price'
        if any(w in q for w in ['analysis', 'technical', 'performance']):
            return 'analysis'
        if any(w in q for w in ['company', 'business', 'about']):
            return 'company'
        if any(w in q for w in ['invest', 'should i', 'strategy']):
            return 'strategy'
        if any(w in q for w in ['what is', 'explain', 'define']):
            return 'education'
        return 'general'
