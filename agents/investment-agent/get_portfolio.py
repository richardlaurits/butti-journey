#!/usr/bin/env python3
"""
Investment Agent - Daily Portfolio Tracker
Uses Yahoo Finance for Nordic stock prices
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add workspace to path
sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace')

try:
    import yfinance as yf
except ImportError:
    print("yfinance not available")
    sys.exit(1)

# Portfolio definition
PORTFOLIO = [
    {"symbol": "NDA-SE.ST", "name": "Nordea Bank", "weight": 15.11, "country": "SE", "sector": "Bank"},
    {"symbol": "SHB-A.ST", "name": "Handelsbanken A", "weight": 13.35, "country": "SE", "sector": "Bank"},
    {"symbol": "SWED-A.ST", "name": "Swedbank A", "weight": 11.79, "country": "SE", "sector": "Bank"},
    {"symbol": "TEL2-B.ST", "name": "Tele2 B", "weight": 11.63, "country": "SE", "sector": "Telecom"},
    {"symbol": "VOLV-B.ST", "name": "Volvo B", "weight": 4.73, "country": "SE", "sector": "Industrials"},
    {"symbol": "ESSITY-B.ST", "name": "Essity B", "weight": 3.89, "country": "SE", "sector": "Consumer Staples"},
    {"symbol": "SAND.ST", "name": "Sandvik", "weight": 3.88, "country": "SE", "sector": "Industrials"},
    {"symbol": "INVE-B.ST", "name": "Investor B", "weight": 3.11, "country": "SE", "sector": "Investment"},
    {"symbol": "ABB.ST", "name": "ABB", "weight": 2.76, "country": "SE", "sector": "Industrials"},
    {"symbol": "EQNR.OL", "name": "Equinor", "weight": 7.11, "country": "NO", "sector": "Energy"},
    {"symbol": "ORK.OL", "name": "Orkla", "weight": 6.25, "country": "NO", "sector": "Consumer Goods"},
    {"symbol": "SAMPO.HE", "name": "Sampo A", "weight": 6.70, "country": "FI", "sector": "Insurance"},
    {"symbol": "UPM.HE", "name": "UPM-Kymmene", "weight": 4.84, "country": "FI", "sector": "Materials"},
    {"symbol": "NOVO-B.CO", "name": "Novo Nordisk B", "weight": 4.86, "country": "DK", "sector": "Pharma"},
]

# Flag emojis
FLAGS = {"SE": "🇸🇪", "NO": "🇳🇴", "FI": "🇫🇮", "DK": "🇩🇰"}

def get_stock_data():
    """Fetch current prices and daily changes for all holdings"""
    results = []
    errors = []
    
    for stock in PORTFOLIO:
        try:
            ticker = yf.Ticker(stock['symbol'])
            hist = ticker.history(period="5d")
            info = ticker.info
            
            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[-2]
                change_pct = ((current - previous) / previous) * 100
                
                results.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'weight': stock['weight'],
                    'country': stock['country'],
                    'sector': stock['sector'],
                    'price': round(current, 2),
                    'currency': info.get('currency', 'SEK'),
                    'change_pct': round(change_pct, 2),
                    'success': True
                })
            else:
                errors.append(f"{stock['name']}: Insufficient data")
                
        except Exception as e:
            errors.append(f"{stock['name']}: {str(e)[:50]}")
    
    return results, errors

def analyze_portfolio(data):
    """Analyze portfolio performance"""
    if not data:
        return None
    
    # Sort by change
    sorted_by_change = sorted(data, key=lambda x: x['change_pct'], reverse=True)
    
    winners = [s for s in sorted_by_change if s['change_pct'] > 0][:3]
    losers = [s for s in sorted_by_change if s['change_pct'] < 0][-3:]
    losers.reverse()  # Most negative first
    
    # Calculate weighted portfolio change
    total_change = sum(s['change_pct'] * s['weight'] for s in data) / 100
    
    # Count by country
    by_country = {}
    for s in data:
        country = s['country']
        if country not in by_country:
            by_country[country] = {'count': 0, 'avg_change': 0}
        by_country[country]['count'] += 1
        by_country[country]['avg_change'] += s['change_pct']
    
    for country in by_country:
        by_country[country]['avg_change'] = round(
            by_country[country]['avg_change'] / by_country[country]['count'], 2
        )
    
    return {
        'winners': winners,
        'losers': losers,
        'portfolio_change': round(total_change, 2),
        'by_country': by_country,
        'total_stocks': len(data),
        'timestamp': datetime.now().isoformat()
    }

def format_telegram_output(analysis, data):
    """Format output for Telegram morning brief"""
    if not analysis:
        return "📈 PORTFÖLJEN\nKunde inte hämta data just nu."
    
    lines = []
    lines.append("📈 PORTFÖLJEN IDAG")
    lines.append("🇸🇪🇳🇴🇫🇮🇩🇰 Nordic Dividend Portfolio")
    lines.append("")
    
    # Portfolio summary
    change_emoji = "📈" if analysis['portfolio_change'] >= 0 else "📉"
    lines.append(f"{change_emoji} Portföljvärde: {analysis['portfolio_change']:+.2f}% (viktat)")
    lines.append("")
    
    # Winners
    if analysis['winners']:
        lines.append("🏆 Vinnare:")
        for stock in analysis['winners']:
            flag = FLAGS.get(stock['country'], '')
            lines.append(f"  {flag} {stock['name']}: {stock['change_pct']:+.2f}%")
        lines.append("")
    
    # Losers
    if analysis['losers']:
        lines.append("🔻 Förlorare:")
        for stock in analysis['losers']:
            flag = FLAGS.get(stock['country'], '')
            lines.append(f"  {flag} {stock['name']}: {stock['change_pct']:+.2f}%")
        lines.append("")
    
    # Notable moves (>3%)
    notable = [s for s in data if abs(s['change_pct']) >= 3.0]
    if notable:
        lines.append("⚠️ Noterbara rörelser (>3%):")
        for stock in notable:
            flag = FLAGS.get(stock['country'], '')
            lines.append(f"  {flag} {stock['name']}: {stock['change_pct']:+.2f}%")
        lines.append("")
    
    # Country breakdown
    lines.append("🌍 Per marknad:")
    for country, stats in analysis['by_country'].items():
        flag = FLAGS.get(country, '')
        change_emoji = "📈" if stats['avg_change'] >= 0 else "📉"
        lines.append(f"  {flag} {country}: {stats['avg_change']:+.2f}% ({stats['count']} aktier)")
    
    return "\n".join(lines)

def save_to_json(data, analysis):
    """Save results for future reference"""
    output_dir = Path('/home/richard-laurits/.openclaw/workspace/agents/investment-agent/data')
    output_dir.mkdir(exist_ok=True)
    
    filename = f"portfolio_{datetime.now().strftime('%Y-%m-%d')}.json"
    filepath = output_dir / filename
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'holdings': data,
        'analysis': analysis
    }
    
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)
    
    return filepath

def main():
    """Main function - fetch and analyze portfolio"""
    print("Fetching portfolio data...", file=sys.stderr)
    
    # Get data
    data, errors = get_stock_data()
    
    if errors:
        print(f"Warnings: {', '.join(errors[:3])}", file=sys.stderr)
    
    if not data:
        print("❌ Kunde inte hämta portföljdata")
        sys.exit(1)
    
    # Analyze
    analysis = analyze_portfolio(data)
    
    # Save
    filepath = save_to_json(data, analysis)
    print(f"💾 Data saved to: {filepath}", file=sys.stderr)
    
    # Output for Telegram
    output = format_telegram_output(analysis, data)
    print(output)

if __name__ == "__main__":
    main()
