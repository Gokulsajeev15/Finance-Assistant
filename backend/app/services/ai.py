import asyncio
import json
import logging
import os
from datetime import datetime
from openai import AsyncOpenAI
from ..database import save_message, get_history

logger = logging.getLogger(__name__)

# The available tools our AI can request. Each maps to a real Python function.
# We describe these in the planning prompt so the LLM knows what it can ask for.
AVAILABLE_TOOLS = {
    "get_stock_price": "Get current price, daily change, and volume for a ticker.",
    "get_technical_analysis": "Get RSI, moving averages (SMA/EMA), Bollinger Bands, and trend for a ticker.",
    "get_company_info": "Get company background: sector, market cap, employees, description."
}


class OpenAIFinancialAI:

    def __init__(self, stock_service, company_service):
        self.stock_service = stock_service
        self.company_service = company_service
        self.client = None
        self._init_client()

    def _init_client(self):
        # --- HF free tier (active) ---
        api_key = os.getenv('HF_TOKEN')
        if not api_key:
            logger.error("HF_TOKEN not set")
            return
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://router.huggingface.co/v1"
        )

        # --- OpenAI paid (uncomment when you have a key, comment block above) ---
        # api_key = os.getenv('OPENAI_API_KEY')
        # if not api_key:
        #     logger.error("OPENAI_API_KEY not set")
        #     return
        # self.client = AsyncOpenAI(api_key=api_key)

    async def process_query(self, query, session_id):
        return await self._answer(query, session_id)

    async def _answer(self, question, session_id):
        if not self.client:
            return {"type": "error", "message": "AI service not available. Check your API key."}

        try:
            # Save the user's message to the DB before doing anything else
            await save_message(session_id, "user", question)

            # Fetch the last 10 messages for this session so the LLM has context.
            # This is what makes the AI remember what was said earlier.
            history = await get_history(session_id, limit=10)

            # --- Call 1: ask the LLM to plan what data it needs ---
            plan = await self._get_plan(question, history)

            # If the LLM says no tools needed, answer directly
            if not plan:
                answer = await self._answer_directly(question, history)
                await save_message(session_id, "ai", answer["message"])
                return answer

            # --- Run the plan: fetch all the data ---
            data_results = await self._execute_plan(plan)

            # --- Call 2: give the LLM the question + history + real data ---
            # We build the messages list as a real conversation:
            # system prompt → past messages → current question with live data
            data_text = json.dumps(data_results, indent=2)
            messages = [{"role": "system", "content": self._answer_prompt()}]

            # Inject history — the LLM sees the full conversation so far
            for msg in history[:-1]:  # exclude the current message, we add it below with data
                messages.append({"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]})

            # Current question with the fetched data appended
            messages.append({"role": "user", "content": f"{question}\n\nReal-time data:\n{data_text}"})

            final_response = await self.client.chat.completions.create(
                model="openai/gpt-oss-120b:groq",
                # model="gpt-4o-mini",
                messages=messages,
                max_tokens=1500,
                temperature=0.3
            )

            ai_message = final_response.choices[0].message.content

            # Save the AI's answer to the DB
            await save_message(session_id, "ai", ai_message)

            return {
                "type": "analysis",
                "message": ai_message,
                "has_real_time_data": len(data_results) > 0,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"AI error: {e}")
            return {"type": "error", "message": "Failed to process your request. Please try again."}

    async def _get_plan(self, question, history=None):
        """
        Call 1 — ask the LLM: "what data do you need to answer this question?"
        The LLM responds with a JSON array of tool calls, e.g.:
          [{"tool": "get_stock_price", "ticker": "AAPL"},
           {"tool": "get_technical_analysis", "ticker": "TSLA"}]
        Or an empty array [] if no live data is needed.
        """
        tools_desc = "\n".join(f"  - {name}: {desc}" for name, desc in AVAILABLE_TOOLS.items())

        # Build the planning conversation — include history so the planner
        # understands context. e.g. "what about its RSI?" after asking about Apple
        # → planner sees "Apple" in history and knows to fetch AAPL technical data.
        planning_messages = [
            {"role": "system", "content": (
                "You are a planning assistant. Your ONLY job is to decide what data is needed "
                "to answer a financial question.\n\n"
                "Available tools:\n"
                f"{tools_desc}\n\n"
                "Rules:\n"
                "- If multiple companies are mentioned, include a tool call for EACH company.\n"
                "- If the question needs multiple types of data (e.g. company info AND RSI), "
                "include BOTH tools for each company.\n"
                "- Use conversation history to resolve references like 'it', 'that stock', 'the same company'.\n"
                "- Common ticker mappings: Apple=AAPL, Tesla=TSLA, Nvidia=NVDA, Microsoft=MSFT, "
                "Google=GOOGL, Amazon=AMZN, Meta=META.\n"
                "- If the question is general (e.g. 'what is RSI?'), return an empty array.\n\n"
                "Respond with ONLY a JSON array. No explanation, no markdown, just the JSON.\n"
                "Example: [{\"tool\": \"get_stock_price\", \"ticker\": \"AAPL\"}, "
                "{\"tool\": \"get_technical_analysis\", \"ticker\": \"AAPL\"}]"
            )}
        ]

        # Add past messages as context for the planner
        for msg in (history or []):
            role = "user" if msg["role"] == "user" else "assistant"
            planning_messages.append({"role": role, "content": msg["content"]})

        planning_messages.append({"role": "user", "content": question})

        response = await self.client.chat.completions.create(
            model="openai/gpt-oss-120b:groq",
            # model="gpt-4o-mini",
            messages=planning_messages,
            max_tokens=500,
            temperature=0
        )

        raw = response.choices[0].message.content.strip()
        logger.info(f"Plan from LLM: {raw}")

        # Parse the JSON plan — handle cases where LLM wraps it in markdown
        try:
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning(f"Could not parse plan, falling back to direct answer: {raw}")
            return []

    # Tools that hit Alpha Vantage — need a 1.2s gap between calls to stay under
    # the free tier's 1 req/second rate limit
    _AV_TOOLS = {"get_stock_price", "get_technical_analysis"}

    async def _execute_plan(self, plan):
        """Run each tool in the plan and collect results."""
        results = {}
        last_was_av_call = False  # track whether the previous call hit Alpha Vantage

        for call in plan:
            tool = call.get("tool", "")
            ticker = call.get("ticker", "").upper()
            key = f"{tool}_{ticker}"

            if key in results:
                continue  # skip duplicate calls

            # Alpha Vantage allows 1 req/second on the free tier.
            # If the previous call also hit AV, wait before firing the next one.
            if last_was_av_call and tool in self._AV_TOOLS:
                await asyncio.sleep(1.2)

            try:
                if tool == "get_stock_price":
                    data = self.stock_service.get_stock_data(ticker)

                elif tool == "get_technical_analysis":
                    data = self.stock_service.get_technical_indicators(ticker)

                elif tool == "get_company_info":
                    data = await self.company_service.get_company_by_ticker(ticker)
                    if not data:
                        data = {"error": f"No company info found for {ticker}"}

                else:
                    logger.warning(f"Unknown tool in plan: {tool}")
                    continue

                logger.info(f"Executed: {tool}({ticker})")
                results[key] = {"tool": tool, "ticker": ticker, "data": data}

            except Exception as e:
                logger.error(f"Tool {tool} failed for {ticker}: {e}")
                results[key] = {"tool": tool, "ticker": ticker, "data": {"error": str(e)}}

            last_was_av_call = tool in self._AV_TOOLS

        return results

    async def _answer_directly(self, question, history=None):
        """For general questions that need no live data."""
        messages = [{"role": "system", "content": self._answer_prompt()}]

        for msg in (history or []):
            role = "user" if msg["role"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})

        messages.append({"role": "user", "content": question})

        response = await self.client.chat.completions.create(
            model="openai/gpt-oss-120b:groq",
            # model="gpt-4o-mini",
            messages=messages,
            max_tokens=1500,
            temperature=0.3
        )
        return {
            "type": "general",
            "message": response.choices[0].message.content,
            "has_real_time_data": False,
            "timestamp": datetime.now().isoformat()
        }

    def _answer_prompt(self):
        return (
            "You are a financial AI assistant. Answer questions factually and concisely "
            "using the real-time data provided. For comparisons, analyze all companies. "
            "For general questions, provide educational insight. "
            "Always note that responses are for informational purposes and not financial advice."
        )
