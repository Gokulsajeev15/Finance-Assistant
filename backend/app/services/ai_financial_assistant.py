"""
Financial AI Assistant - Easy to understand AI that helps with money questions

This is like having a smart friend who knows about:
- Stock prices (like Apple, Tesla, etc.)
- Financial concepts (compound interest, P/E ratios, etc.)
- Investment advice (how to invest, diversification, etc.)
- Market information (inflation, interest rates, etc.)

The AI is designed to be super simple and easy to understand!
"""
import logging
import random

logger = logging.getLogger(__name__)

class SimpleFinancialAI:
    """A friendly AI assistant that answers questions about money and investing"""
    
    def __init__(self, stock_service, company_service):
        # Store the services we need
        self.stock_service = stock_service
        self.company_service = company_service
        
        # Common company names people might ask about
        self.company_names = {
            # Tech companies
            'apple': 'AAPL', 'iphone': 'AAPL',
            'microsoft': 'MSFT', 'windows': 'MSFT',
            'google': 'GOOGL', 'alphabet': 'GOOGL',
            'amazon': 'AMZN', 'aws': 'AMZN',
            'tesla': 'TSLA', 'elon': 'TSLA',
            'meta': 'META', 'facebook': 'META',
            'netflix': 'NFLX', 'streaming': 'NFLX',
            'nvidia': 'NVDA', 'ai': 'NVDA',
            
            # Other big companies
            'walmart': 'WMT', 'disney': 'DIS',
            'coca cola': 'KO', 'coke': 'KO',
            'mcdonalds': 'MCD', 'nike': 'NKE'
        }
    
    async def answer_question(self, question):
        """Answer any question about money or stocks"""
        try:
            # Make the question lowercase for easier checking
            question = question.lower().strip()
            
            # Figure out what kind of question this is
            question_type = self._what_type_of_question(question)
            
            # Find any company mentioned in the question
            company_ticker = self._find_company_in_question(question)
            
            # Answer based on the type of question
            if question_type == 'price' and company_ticker:
                return await self._answer_price_question(company_ticker, question)
            elif question_type == 'company' and company_ticker:
                return await self._answer_company_question(company_ticker, question)
            elif question_type == 'analysis' and company_ticker:
                return await self._answer_analysis_question(company_ticker, question)
            elif question_type == 'education':
                return self._answer_education_question(question)
            elif question_type == 'strategy':
                return self._answer_strategy_question(question)
            elif question_type == 'market':
                return self._answer_market_question(question)
            else:
                return self._answer_general_question(question)
                
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                "type": "error",
                "message": "Sorry, I had trouble understanding your question. Try asking about a specific stock or financial topic!"
            }
    
    def _what_type_of_question(self, question):
        """Figure out what type of question someone is asking"""
        
        # Price questions
        if any(word in question for word in ['price', 'cost', 'worth', 'value', 'quote']):
            return 'price'
        
        # Company questions
        if any(word in question for word in ['company', 'about', 'tell me', 'information']):
            return 'company'
        
        # Analysis questions (including technical analysis)
        if any(word in question for word in ['analyze', 'analysis', 'technical', 'performance', 'how is', 'doing', 'rsi', 'indicators']):
            return 'analysis'
        
        # Education questions
        if any(word in question for word in ['what is', 'explain', 'how does', 'define']):
            return 'education'
        
        # Strategy questions
        if any(word in question for word in ['should i', 'invest', 'strategy', 'advice']):
            return 'strategy'
        
        # Market questions
        if any(word in question for word in ['market', 'economy', 'inflation', 'interest rate']):
            return 'market'
        
        return 'general'
    
    def _find_company_in_question(self, question):
        """Look for company names in the question"""
        
        # Convert question to lowercase for easier matching
        question_lower = question.lower()
        
        # First, look for company names in our mapping
        for company_name, ticker in self.company_names.items():
            if company_name in question_lower:
                return ticker
        
        # Then, look for stock symbols like AAPL, MSFT
        import re
        stock_symbols = re.findall(r'\b[A-Z]{2,5}\b', question.upper())
        if stock_symbols:
            return stock_symbols[0]
        
        return None
    
    async def _answer_price_question(self, ticker, question):
        """Answer questions about stock prices"""
        try:
            # Get the stock data
            stock_data = self.stock_service.get_stock_data(ticker)
            
            if 'error' in stock_data:
                return {
                    "type": "error",
                    "message": f"Sorry, I couldn't get the price for {ticker} right now."
                }
            
            # Get the important information
            price = stock_data.get('current_price', 0)
            change = stock_data.get('change', 0)
            change_percent = stock_data.get('change_percent', 0)
            company_name = stock_data.get('company_name', ticker)
            
            # Create a simple, friendly response
            if change_percent > 1:
                mood = "📈 Great news!"
                description = f"{company_name} is doing well today"
            elif change_percent > 0:
                mood = "📊 Good news!"
                description = f"{company_name} is up a little today"
            elif change_percent < -1:
                mood = "📉 Not so great today"
                description = f"{company_name} is down a bit"
            else:
                mood = "📊 Pretty steady"
                description = f"{company_name} hasn't moved much today"
            
            message = f"{mood} {description}!\n\n"
            message += f"💰 Current price: ${price:.2f}\n"
            message += f"📈 Change today: ${change:+.2f} ({change_percent:+.2f}%)"
            
            return {
                "type": "price",
                "message": message,
                "ticker": ticker,
                "data": stock_data
            }
            
        except Exception as e:
            return {
                "type": "error",
                "message": f"I had trouble getting the price for {ticker}. Try again in a moment!"
            }
    
    async def _answer_company_question(self, ticker, question):
        """Answer questions about companies"""
        try:
            # Get company info from Fortune 500 list
            company_info = self.company_service.get_company_by_ticker(ticker)
            stock_data = self.stock_service.get_stock_data(ticker)
            
            if not company_info:
                return {
                    "type": "error",
                    "message": f"I don't have detailed information about {ticker}, but I can help with stock analysis!"
                }
            
            # Create a simple response about the company
            name = company_info['company']
            sector = company_info.get('sector', 'Unknown')
            rank = company_info.get('rank', 'N/A')
            revenue = company_info.get('revenue', 0)
            
            message = f"🏢 Let me tell you about {name}!\n\n"
            
            if rank <= 10:
                message += f"🌟 This is a HUGE company - ranked #{rank} in the Fortune 500!\n"
            elif rank <= 50:
                message += f"💪 This is a big company - ranked #{rank} in the Fortune 500!\n"
            else:
                message += f"📈 This company is ranked #{rank} in the Fortune 500!\n"
            
            message += f"🏭 They work in: {sector}\n"
            message += f"💰 They make: ${revenue:,} million per year\n"
            
            # Add current stock price if we have it
            if stock_data and 'current_price' in stock_data:
                price = stock_data['current_price']
                message += f"📊 Stock price today: ${price:.2f}"
            
            return {
                "type": "company",
                "message": message,
                "ticker": ticker,
                "data": {"company_info": company_info, "stock_data": stock_data}
            }
            
        except Exception as e:
            return {
                "type": "error",
                "message": f"I had trouble getting information about {ticker}. Try asking again!"
            }
    
    async def _answer_analysis_question(self, ticker, question):
        """Answer questions about how a stock is performing (including technical analysis)"""
        try:
            # Get stock data, company data, and technical indicators
            stock_data = self.stock_service.get_stock_data(ticker)
            company_info = self.company_service.get_company_by_ticker(ticker)
            technical_data = self.stock_service.get_technical_indicators(ticker)
            
            if 'error' in stock_data:
                return {
                    "type": "error", 
                    "message": f"I couldn't analyze {ticker} right now. Try again later!"
                }
            
            # Get the key information
            company_name = stock_data.get('company_name', ticker)
            price = stock_data.get('current_price', 0)
            change_percent = stock_data.get('change_percent', 0)
            
            # Start with a friendly introduction
            message = f"📊 Here's how {company_name} is doing:\n\n"
            
            # Talk about the stock price performance
            if change_percent > 2:
                message += f"🚀 The stock is having a great day! Up {change_percent:.1f}% to ${price:.2f}\n"
            elif change_percent > 0:
                message += f"📈 The stock is doing well today, up {change_percent:.1f}% to ${price:.2f}\n"
            elif change_percent < -2:
                message += f"📉 The stock is having a tough day, down {abs(change_percent):.1f}% to ${price:.2f}\n"
            else:
                message += f"📊 The stock is pretty steady today at ${price:.2f}\n"
            
            # Add technical analysis if we have it
            if technical_data and 'error' not in technical_data:
                message += f"\n📈 **Technical Analysis:**\n"
                
                # RSI information
                if 'rsi' in technical_data:
                    rsi_value = technical_data['rsi'].get('value', 0)
                    rsi_interpretation = technical_data['rsi'].get('interpretation', '')
                    message += f"• RSI: {rsi_value:.1f} ({rsi_interpretation})\n"
                
                # Moving averages
                if 'sma_20' in technical_data and technical_data['sma_20']:
                    message += f"• 20-day average: ${technical_data['sma_20']:.2f}\n"
                if 'sma_50' in technical_data and technical_data['sma_50']:
                    message += f"• 50-day average: ${technical_data['sma_50']:.2f}\n"
                
                # Trend
                if 'trend' in technical_data:
                    trend_emoji = "📈" if technical_data['trend'] == "Up" else "📉"
                    message += f"• Trend: {trend_emoji} {technical_data['trend']}\n"
            
            # Add company information if we have it
            if company_info:
                rank = company_info.get('rank', 'N/A')
                revenue = company_info.get('revenue', 0)
                
                if rank <= 50:
                    message += f"\n💪 This is a strong company - Fortune 500 rank #{rank}"
                    message += f"\n💰 They make ${revenue:,} million per year"
            
            return {
                "type": "analysis",
                "message": message,
                "ticker": ticker,
                "data": {
                    "stock_data": stock_data, 
                    "company_info": company_info,
                    "company_name": company_name,
                    "sector": company_info.get('sector', 'Unknown') if company_info else 'Unknown',
                    # Format for frontend technical analysis component
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
                    },
                    "technical_data": {
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
                            },
                            "moving_averages": {
                                "sma_20": technical_data.get('sma_20') if technical_data and 'error' not in technical_data else None,
                                "sma_50": technical_data.get('sma_50') if technical_data and 'error' not in technical_data else None,
                                "ema_12": None,  # We don't calculate this yet
                                "ema_26": None   # We don't calculate this yet
                            }
                        }
                    }
                }
            }
            
        except Exception as e:
            return {
                "type": "error",
                "message": f"I had trouble analyzing {ticker}. Please try again!"
            }
    
    def _answer_education_question(self, question):
        """Answer questions about financial concepts"""
        
        # Simple explanations for common financial terms
        explanations = {
            'compound interest': {
                'title': 'Compound Interest - Money That Grows Money!',
                'explanation': "Imagine you plant a money tree with $100. Every year, it grows by 10%. After year 1, you have $110. But here's the magic - in year 2, you earn 10% on the WHOLE $110, not just the original $100! So you get $121. This keeps happening, and your money grows faster and faster. That's compound interest - your earnings start earning money too!"
            },
            'p/e ratio': {
                'title': 'P/E Ratio - How Expensive is a Stock?',
                'explanation': "Think of P/E ratio like this: If a stock costs $20 and the company earns $2 per year, the P/E is 10 (20÷2=10). This means you're paying $10 for every $1 the company earns. Lower P/E usually means cheaper stock, higher P/E means more expensive. It's like comparing price tags at different stores!"
            },
            'diversification': {
                'title': 'Diversification - Don\'t Put All Eggs in One Basket!',
                'explanation': "Imagine you have 10 eggs. If you put them all in one basket and drop it, you lose everything! But if you put eggs in 10 different baskets and drop one, you only lose 1 egg. Diversification means buying different types of stocks so if one goes down, others might go up. It's like having backup plans for your money!"
            },
            'dividend': {
                'title': 'Dividends - Getting Paid to Own Stock!',
                'explanation': "A dividend is like getting paid just for owning a piece of a company! Some companies share their profits with stockholders. If you own 100 shares of a company that pays $1 per share each year, you get $100 just for holding the stock. It's like rent money, but for owning stocks instead of houses!"
            },
            'inflation': {
                'title': 'Inflation - Why Things Get More Expensive',
                'explanation': "Remember when candy bars cost 50 cents? Now they cost $2! That's inflation - things get more expensive over time. If you hide $100 under your mattress for 10 years, it won't buy as much stuff as it does today. That's why people invest - to make their money grow faster than inflation!"
            }
        }
        
        # Find the best match for the question
        best_match = None
        for term, info in explanations.items():
            if term.replace(' ', '') in question.replace(' ', ''):
                best_match = info
                break
        
        if best_match:
            message = f"💡 **{best_match['title']}**\n\n{best_match['explanation']}\n\n🤔 Want to know about anything else?"
        else:
            message = "🤔 Great question! I love explaining money stuff!\n\nI can explain things like:\n• Compound interest (how money grows)\n• P/E ratios (if stocks are expensive)\n• Diversification (spreading risk)\n• Dividends (getting paid to own stocks)\n• Inflation (why things get pricier)\n\nWhat would you like to learn about?"
        
        return {
            "type": "education",
            "message": message,
            "suggestions": [
                "What is compound interest?",
                "Explain P/E ratios",
                "What is diversification?",
                "Tell me about dividends"
            ]
        }
    
    def _answer_strategy_question(self, question):
        """Answer questions about investing strategies"""
        
        tips = [
            "🎯 **Smart Investing Tips**\n\nHere are some simple rules:\n\n• Start early - time is your best friend!\n• Don't put all money in one stock\n• Only invest money you won't need soon\n• Learn before you invest\n• Stay calm when markets go up and down\n\n💡 Remember: I'm just a computer - talk to a real financial advisor for personal advice!",
            
            "📈 **Beginner's Investment Guide**\n\nGood rules to follow:\n\n• Save 3-6 months of expenses first\n• Start with index funds (they own many stocks)\n• Invest regularly, even small amounts\n• Don't try to time the market\n• Think long-term (years, not days)\n\n⚠️ Always do your own research and get professional advice!"
        ]
        
        message = random.choice(tips)
        
        return {
            "type": "strategy",
            "message": message,
            "suggestions": [
                "How to start investing?",
                "What is diversification?",
                "Analyze Apple stock",
                "What are index funds?"
            ]
        }
    
    def _answer_market_question(self, question):
        """Answer questions about markets and economy"""
        
        # Simple explanations for market topics
        if 'inflation' in question:
            message = "💰 **How Inflation Affects Your Money**\n\nInflation is like everything getting more expensive over time:\n\n• 🏪 Groceries cost more\n• ⛽ Gas prices go up\n• 🏠 Houses become pricier\n\nThis affects investments:\n• 📈 Stocks often do okay (companies can raise prices too)\n• 📉 Cash loses value (same dollars buy less stuff)\n• 🏦 Bonds can lose value\n\nThat's why many people invest - to beat inflation!"
            
        elif 'interest rate' in question:
            message = "📊 **Interest Rates and the Stock Market**\n\nInterest rates are like the 'price of money':\n\n• 📈 Higher rates: Banks pay more, bonds look better, stocks might go down\n• 📉 Lower rates: Cheaper to borrow, stocks often go up\n• 🏦 The Federal Reserve controls these rates\n\nThink of it like a seesaw - when rates go up, stocks often go down, and vice versa!"
            
        else:
            message = "📈 **Understanding Markets**\n\nThe stock market is like a giant auction where people buy and sell pieces of companies!\n\n• 📊 Prices go up when more people want to buy\n• 📉 Prices go down when more people want to sell\n• 🌍 News, economy, and company results affect prices\n• 📈 Over long periods, markets usually go up\n\nWhat specific market topic interests you?"
        
        return {
            "type": "market",
            "message": message,
            "suggestions": [
                "How does inflation affect stocks?",
                "What are interest rates?",
                "Why do stock prices change?",
                "Analyze Tesla performance"
            ]
        }
    
    def _answer_general_question(self, question):
        """Answer general questions when we're not sure what they're asking"""
        
        message = "🤔 I'd love to help you with your money question!\n\nI'm great at:\n• 📊 Stock prices and company info\n• 💡 Explaining financial concepts simply\n• 📈 Investment basics and strategies\n• 🌍 How markets and economy work\n\nTry asking me something like:\n• 'What is Apple's stock price?'\n• 'Explain compound interest'\n• 'How should I start investing?'\n• 'Tell me about Microsoft'"
        
        return {
            "type": "general",
            "message": message,
            "suggestions": [
                "Apple stock price",
                "What is compound interest?",
                "How to invest?",
                "Microsoft company info"
            ]
        }
