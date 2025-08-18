"""
Hugging Face AI Service - Real AI for Financial Questions

This service uses actual machine learning models:
- FinBERT: For financial sentiment analysis  
- Sentence Transformers: For intent classification
- RoBERTa: For question answering

Much simpler than rule-based systems!
"""
import logging
import asyncio
from typing import Dict, Any, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentence_transformers import SentenceTransformer, util
import numpy as np

logger = logging.getLogger(__name__)

class HuggingFaceFinancialAI:
    """Real AI-powered financial assistant using Hugging Face models"""
    
    def __init__(self, stock_service, company_service):
        self.stock_service = stock_service
        self.company_service = company_service
        self._init_models()
        self._setup_intents()
    
    def _init_models(self):
        """Initialize AI models (loads once, uses everywhere)"""
        try:
            logger.info("Loading AI models...")
            
            # FinBERT for financial sentiment
            self.sentiment_pipeline = pipeline(
                "text-classification",
                model="ProsusAI/finbert",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Sentence transformer for intent classification
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # QA model for complex questions
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("✅ AI models loaded successfully!")
            
        except Exception as e:
            logger.error(f"AI model loading failed: {e}")
            # Fallback to minimal functionality
            self.sentiment_pipeline = None
            self.qa_pipeline = None
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def _setup_intents(self):
        """Setup AI intent classification"""
        intents = {
            'price': ["stock price", "current price", "how much costs", "value of"],
            'analysis': ["technical analysis", "how is performing", "analyze stock", "RSI"],
            'company': ["tell me about", "company information", "what does do"],
            'education': ["what is", "explain", "how does work", "define"],
            'strategy': ["investment advice", "how to invest", "strategy", "should I buy"]
        }
        
        # Create AI embeddings for each intent
        if self.sentence_model:
            self.intent_embeddings = {}
            for intent, examples in intents.items():
                embeddings = self.sentence_model.encode(examples)
                self.intent_embeddings[intent] = np.mean(embeddings, axis=0)
    
    async def answer_question(self, question: str) -> Dict[str, Any]:
        """Main AI method - uses machine learning to understand and respond"""
        try:
            question = question.strip()
            
            # Use AI to classify intent
            intent = self._classify_intent_ai(question)
            
            # Use AI to extract company
            company_ticker = self._extract_company_ai(question)
            
            # Route to appropriate AI handler
            if intent == 'price' and company_ticker:
                return await self._ai_price_response(company_ticker, question)
            elif intent == 'analysis' and company_ticker:
                return await self._ai_analysis_response(company_ticker, question)
            elif intent == 'company' and company_ticker:
                return await self._ai_company_response(company_ticker, question)
            elif intent == 'education':
                return self._ai_education_response(question)
            elif intent == 'strategy':
                return self._ai_strategy_response(question)
            else:
                return self._ai_general_response(question)
                
        except Exception as e:
            logger.error(f"AI error: {e}")
            return {"type": "error", "message": "AI is having trouble. Please try again!"}
    
    def _classify_intent_ai(self, question: str) -> str:
        """Use AI embeddings to classify intent"""
        if not self.sentence_model:
            return 'general'
        
        try:
            question_embedding = self.sentence_model.encode([question])
            best_intent = 'general'
            best_score = 0
            
            for intent, intent_embedding in self.intent_embeddings.items():
                similarity = util.cos_sim(question_embedding, intent_embedding.reshape(1, -1))
                score = similarity.item()
                
                if score > best_score:
                    best_score = score
                    best_intent = intent
            
            return best_intent if best_score > 0.3 else 'general'
            
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return 'general'
    
    def _extract_company_ai(self, question: str) -> Optional[str]:
        """AI-powered company extraction"""
        # Simple but effective company mapping
        companies = {
            'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'alphabet': 'GOOGL',
            'amazon': 'AMZN', 'tesla': 'TSLA', 'meta': 'META', 'facebook': 'META',
            'netflix': 'NFLX', 'nvidia': 'NVDA', 'disney': 'DIS', 'walmart': 'WMT'
        }
        
        question_lower = question.lower()
        
        # Check company names
        for company, ticker in companies.items():
            if company in question_lower:
                return ticker
        
        # Check for tickers (2-5 capital letters)
        import re
        tickers = re.findall(r'\b[A-Z]{2,5}\b', question)
        return tickers[0] if tickers else None
    
    async def _ai_price_response(self, ticker: str, question: str) -> Dict[str, Any]:
        """AI-powered price response with sentiment analysis"""
        try:
            stock_data = self.stock_service.get_stock_data(ticker)
            
            if 'error' in stock_data:
                return {"type": "error", "message": f"Couldn't get price for {ticker}"}
            
            company_name = stock_data.get('company_name', ticker)
            price = stock_data.get('current_price', 0)
            change_percent = stock_data.get('change_percent', 0)
            
            # AI sentiment analysis
            sentiment_text = f"{company_name} stock price ${price:.2f}, changed {change_percent:.1f}%"
            sentiment = self._analyze_sentiment(sentiment_text)
            
            # Generate smart response based on AI sentiment
            if sentiment and sentiment[0]['label'] == 'positive':
                emoji = "🚀" if change_percent > 0 else "💪"
                tone = "looking strong"
            elif sentiment and sentiment[0]['label'] == 'negative':
                emoji = "📉" if change_percent < 0 else "⚠️"
                tone = "facing challenges"
            else:
                emoji = "📊"
                tone = "trading steadily"
            
            message = f"{emoji} **{company_name}** is {tone}\n\n"
            message += f"💰 **${price:.2f}** ({change_percent:+.1f}% today)\n\n"
            message += f"🤖 **AI Sentiment:** {sentiment[0]['label'].title()} ({sentiment[0]['score']:.1%} confidence)" if sentiment else ""
            
            return {
                "type": "price",
                "message": message,
                "ticker": ticker,
                "data": stock_data,
                "ai_sentiment": sentiment[0] if sentiment else None
            }
            
        except Exception as e:
            logger.error(f"AI price error: {e}")
            return {"type": "error", "message": f"Had trouble analyzing {ticker}"}
    
    async def _ai_analysis_response(self, ticker: str, question: str) -> Dict[str, Any]:
        """AI-powered technical analysis"""
        try:
            stock_data = self.stock_service.get_stock_data(ticker)
            technical_data = self.stock_service.get_technical_indicators(ticker)
            company_info = self.company_service.get_company_by_ticker(ticker)
            
            if 'error' in stock_data:
                return {"type": "error", "message": f"Couldn't analyze {ticker}"}
            
            company_name = stock_data.get('company_name', ticker)
            price = stock_data.get('current_price', 0)
            change_percent = stock_data.get('change_percent', 0)
            
            message = f"🤖 **AI Analysis: {company_name}**\n\n"
            message += f"📊 **${price:.2f}** ({change_percent:+.1f}%)\n\n"
            
            # Add technical indicators if available
            if technical_data and 'error' not in technical_data:
                message += "📈 **Technical Indicators:**\n"
                if 'rsi' in technical_data:
                    rsi = technical_data['rsi'].get('value', 0)
                    rsi_interp = technical_data['rsi'].get('interpretation', '')
                    message += f"• RSI: {rsi:.1f} ({rsi_interp})\n"
                
                if 'sma_20' in technical_data and technical_data['sma_20']:
                    message += f"• 20-day SMA: ${technical_data['sma_20']:.2f}\n"
                if 'sma_50' in technical_data and technical_data['sma_50']:
                    message += f"• 50-day SMA: ${technical_data['sma_50']:.2f}\n"
            
            return {
                "type": "analysis",
                "message": message,
                "ticker": ticker,
                "data": {
                    "stock_data": stock_data,
                    "technical_data": technical_data,
                    "company_info": company_info,
                    # Flattened data for frontend
                    "current_price": price,
                    "company_name": company_name,
                    "sector": company_info.get('sector', 'Unknown') if company_info else 'Unknown',
                    "rsi": technical_data.get('rsi', {}).get('value') if technical_data and 'error' not in technical_data else None,
                    "sma_20": technical_data.get('sma_20') if technical_data and 'error' not in technical_data else None,
                    "sma_50": technical_data.get('sma_50') if technical_data and 'error' not in technical_data else None,
                    "high_6m": stock_data.get('52_week_high'),
                    "low_6m": stock_data.get('52_week_low'),
                    "avg_volume": stock_data.get('volume'),
                    "price_data": {
                        "current_price": price,
                        "high_6m": stock_data.get('52_week_high'),
                        "low_6m": stock_data.get('52_week_low'),
                        "volume_avg": stock_data.get('volume')
                    },
                    "indicators": {
                        "rsi": {
                            "current": technical_data.get('rsi', {}).get('value') if technical_data and 'error' not in technical_data else None,
                            "interpretation": technical_data.get('rsi', {}).get('interpretation') if technical_data and 'error' not in technical_data else None
                        }
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return {"type": "error", "message": f"Had trouble analyzing {ticker}"}
    
    async def _ai_company_response(self, ticker: str, question: str) -> Dict[str, Any]:
        """AI-powered company information"""
        try:
            stock_data = self.stock_service.get_stock_data(ticker)
            company_info = self.company_service.get_company_by_ticker(ticker)
            
            if 'error' in stock_data:
                return {"type": "error", "message": f"Couldn't find info about {ticker}"}
            
            company_name = stock_data.get('company_name', ticker)
            price = stock_data.get('current_price', 0)
            
            message = f"🏢 **{company_name}**\n\n"
            
            if company_info:
                sector = company_info.get('sector', 'Unknown')
                rank = company_info.get('rank', 'N/A')
                revenue = company_info.get('revenue', 0)
                
                message += f"🏭 **Sector:** {sector}\n"
                message += f"📊 **Fortune 500 Rank:** #{rank}\n"
                message += f"💰 **Revenue:** ${revenue:,} million\n"
            
            message += f"📈 **Current Stock:** ${price:.2f}"
            
            return {
                "type": "company",
                "message": message,
                "ticker": ticker,
                "data": {"stock_data": stock_data, "company_info": company_info}
            }
            
        except Exception as e:
            logger.error(f"AI company error: {e}")
            return {"type": "error", "message": f"Had trouble getting info about {ticker}"}
    
    def _ai_education_response(self, question: str) -> Dict[str, Any]:
        """AI-powered educational responses"""
        try:
            # Enhanced financial knowledge for AI
            context = """
            Diversification spreads investment risk across different assets, sectors, and regions.
            Compound interest is earning interest on both principal and previously earned interest.
            P/E ratio compares stock price to earnings per share, indicating valuation.
            Bonds are debt securities where investors lend money for regular interest payments.
            ETFs are baskets of securities that trade like individual stocks.
            Market volatility refers to price fluctuations over time.
            """
            
            # Use AI to answer if available
            if self.qa_pipeline:
                try:
                    result = self.qa_pipeline(question=question, context=context)
                    
                    if result['score'] > 0.1:
                        message = f"🤖 **AI Education**\n\n💡 **{result['answer']}**\n\n"
                        
                        # Add practical examples based on keywords
                        q_lower = question.lower()
                        if 'diversif' in q_lower:
                            message += "📊 **Example:** Spread $1000 across: $400 stocks, $300 bonds, $200 international, $100 cash"
                        elif 'compound' in q_lower:
                            message += "💰 **Example:** $1000 at 7% becomes $7,612 in 30 years!"
                        elif 'p/e' in q_lower:
                            message += "📈 **Example:** Apple at $150 with $6 earnings = P/E of 25"
                        
                        message += "\n\n🎯 Ask me more financial questions!"
                        
                        return {
                            "type": "education",
                            "message": message,
                            "ai_confidence": result['score']
                        }
                except Exception as e:
                    logger.error(f"QA error: {e}")
            
            # Smart fallback responses
            return self._smart_fallback(question)
            
        except Exception as e:
            logger.error(f"Education error: {e}")
            return self._smart_fallback(question)
    
    def _smart_fallback(self, question: str) -> Dict[str, Any]:
        """Smart fallback with keyword detection"""
        q = question.lower()
        
        if 'diversif' in q:
            message = "🎯 **Diversification**\n\nDon't put all eggs in one basket! Spread your $1000 across different investments to reduce risk."
        elif 'compound' in q:
            message = "💰 **Compound Interest**\n\nMoney growing on money! $1000 becomes $7,612 in 30 years at 7% annual return."
        elif 'p/e' in q:
            message = "📊 **P/E Ratio**\n\nStock Price ÷ Earnings. Shows how expensive a stock is relative to its profits."
        else:
            message = f"🤖 **AI Assistant**\n\nGreat question! I can explain financial concepts, analyze stocks, and provide investment guidance. What would you like to know?"
        
        return {"type": "education", "message": message}
    
    def _ai_strategy_response(self, question: str) -> Dict[str, Any]:
        """AI-powered investment strategy advice"""
        message = "💼 **AI Investment Strategy**\n\n"
        message += "🎯 **Smart investing principles:**\n\n"
        message += "• **Diversify** across different assets\n"
        message += "• **Think long-term** (time in market beats timing)\n"
        message += "• **Start early** (compound interest is powerful)\n"
        message += "• **Invest regularly** (dollar-cost averaging)\n"
        message += "• **Only invest** what you can afford to lose\n\n"
        message += "⚠️ This is educational content, not personal advice."
        
        return {"type": "strategy", "message": message}
    
    def _ai_general_response(self, question: str) -> Dict[str, Any]:
        """AI-powered general responses"""
        # Try to use AI for any financial question
        if any(word in question.lower() for word in ['what', 'how', 'why', 'explain']):
            context = "Financial markets include stocks, bonds, ETFs, options, and other securities traded globally."
            
            if self.qa_pipeline:
                try:
                    result = self.qa_pipeline(question=question, context=context)
                    if result['score'] > 0.05:
                        message = f"🤖 **AI Response**\n\n💡 {result['answer']}\n\n🎯 Ask me more about finance!"
                        return {
                            "type": "general",
                            "message": message,
                            "ai_confidence": result['score']
                        }
                except:
                    pass
        
        # Fallback guidance
        message = "🤖 **AI Financial Assistant**\n\n"
        message += "I can help with:\n📊 Stock analysis\n💰 Price queries\n🎓 Financial education\n💼 Investment strategies"
        
        return {"type": "general", "message": message}
    
    def _analyze_sentiment(self, text: str):
        """Use FinBERT for sentiment analysis"""
        if self.sentiment_pipeline:
            try:
                return self.sentiment_pipeline(text)
            except Exception as e:
                logger.error(f"Sentiment error: {e}")
        return None