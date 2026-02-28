#!/usr/bin/env python3
"""
Investment Agent - Daily Nordic Portfolio Tracker
Tracks Richard's dividend portfolio: price changes + news
"""

import json
import sys
from datetime import datetime, timedelta

# Import portfolio
sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace/agents/investment-agent')
from portfolio import PORTFOLIO, COMPANY_NAMES_FOR_SEARCH

def get_stock_data():
    """
    Get current stock prices and daily changes.
    Note: In a real implementation, this would call an API like:
    - Yahoo Finance API
    - OMX Nordic API
    - Alpha Vantage
    
    For now, we'll use web search to get approximate data.
    """
    # This is a placeholder - the actual implementation will use web_search
    # to get current prices from sources like Avanza, Nordnet, or Yahoo Finance
    return []

def format_portfolio_summary():
    """Generate a text summary of the portfolio for prompts"""
    lines = ["Richard's Nordic Dividend Portfolio:"]
    lines.append("")
    
    # Group by country
    by_country = {}
    for stock in PORTFOLIO:
        country = stock['country']
        if country not in by_country:
            by_country[country] = []
        by_country[country].append(stock)
    
    for country in ['SE', 'NO', 'FI', 'DK']:
        if country in by_country:
            flag = {'SE': '🇸🇪', 'NO': '🇳🇴', 'FI': '🇫🇮', 'DK': '🇩🇰'}[country]
            lines.append(f"{flag} {country}:")
            for stock in by_country[country]:
                lines.append(f"  • {stock['name']} ({stock['symbol']}) - {stock['weight']}%")
            lines.append("")
    
    return "\n".join(lines)

def get_prompt_for_daily_brief():
    """Generate the prompt for the morning brief sub-agent"""
    
    portfolio_text = format_portfolio_summary()
    company_list = ", ".join(COMPANY_NAMES_FOR_SEARCH[:7]) + "..."
    
    prompt = f"""
Get Richard's investment portfolio update for the morning brief.

PORTFOLIO:
{portfolio_text}

TASK:
1. Get today's price changes (%) for these Nordic stocks
   - Search: "[company name] stock price today" or "OMX Stockholm [ticker]"
   - Sources: Yahoo Finance, Avanza, Nordnet, OMX Nordic
   
2. Identify:
   - Top 3 winners (highest % gain)
   - Top 3 losers (biggest % drop)
   - Any stock with >3% move (notable)

3. Search for NEWS about these companies from last 24h:
   - Focus on: {company_list}
   - Look for: earnings, dividends, analyst ratings, M&A, regulatory news
   - Max 2-3 most important news items

4. Format as:

📈 PORTFÖLJEN IDAG
🇸🇪🇳🇴🇫🇮🇩🇰 Nordic Dividend Portfolio

Vinnare:
• [Namn] +X.XX%
• [Namn] +X.XX%

Förlorare:
• [Namn] -X.XX%
• [Namn] -X.XX%

📰 Nyheter:
• [Bolag]: [Nyhet i 10 ord] (källa)
• [Bolag]: [Nyhet i 10 ord] (källa)

If no significant news: "Inga stora nyheter senaste 24h."
If data unavailable: "Kursdata ej tillgänglig just nu."

Be concise. Use web_search for both prices and news.
"""
    return prompt

if __name__ == "__main__":
    print(get_prompt_for_daily_brief())
