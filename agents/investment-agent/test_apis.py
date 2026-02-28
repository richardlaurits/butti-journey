#!/usr/bin/env python3
"""
Investment Agent - Test Implementation
Tests both Yahoo Finance and Nasdaq Nordic APIs
"""

import sys
import json
from datetime import datetime, timedelta

# Portfolio data
PORTFOLIO = [
    {"symbol": "NDA-SE.ST", "name": "Nordea Bank", "weight": 15.11, "country": "SE", "sector": "Bank", "omx_id": "36581"},
    {"symbol": "SHB-A.ST", "name": "Handelsbanken A", "weight": 13.35, "country": "SE", "sector": "Bank", "omx_id": "9924"},
    {"symbol": "SWED-A.ST", "name": "Swedbank A", "weight": 11.79, "country": "SE", "sector": "Bank", "omx_id": "5247"},
    {"symbol": "TEL2-B.ST", "name": "Tele2 B", "weight": 11.63, "country": "SE", "sector": "Telecom", "omx_id": "18705"},
    {"symbol": "VOLV-B.ST", "name": "Volvo B", "weight": 4.73, "country": "SE", "sector": "Industrials", "omx_id": "5238"},
    {"symbol": "ESSITY-B.ST", "name": "Essity B", "weight": 3.89, "country": "SE", "sector": "Consumer Staples", "omx_id": "200163"},
    {"symbol": "SAND.ST", "name": "Sandvik", "weight": 3.88, "country": "SE", "sector": "Industrials", "omx_id": "5564"},
    {"symbol": "INVE-B.ST", "name": "Investor B", "weight": 3.11, "country": "SE", "sector": "Investment", "omx_id": "5241"},
    {"symbol": "ABB.ST", "name": "ABB", "weight": 2.76, "country": "SE", "sector": "Industrials", "omx_id": "5581"},
    {"symbol": "EQNR.OL", "name": "Equinor", "weight": 7.11, "country": "NO", "sector": "Energy", "omx_id": None},
    {"symbol": "ORK.OL", "name": "Orkla", "weight": 6.25, "country": "NO", "sector": "Consumer Goods", "omx_id": None},
    {"symbol": "SAMPO.HE", "name": "Sampo A", "weight": 6.70, "country": "FI", "sector": "Insurance", "omx_id": None},
    {"symbol": "UPM.HE", "name": "UPM-Kymmene", "weight": 4.84, "country": "FI", "sector": "Materials", "omx_id": None},
    {"symbol": "NOVO-B.CO", "name": "Novo Nordisk B", "weight": 4.86, "country": "DK", "sector": "Pharma", "omx_id": None},
]

def test_yahoo_finance():
    """Test Yahoo Finance API via yfinance"""
    print("=" * 60)
    print("TEST 1: YAHOO FINANCE (yfinance)")
    print("=" * 60)
    
    try:
        import yfinance as yf
        print("✅ yfinance is available")
    except ImportError:
        print("❌ yfinance not installed")
        print("Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
        import yfinance as yf
        print("✅ yfinance installed successfully")
    
    results = []
    print("\n📊 Fetching data for portfolio...")
    
    for stock in PORTFOLIO[:5]:  # Test first 5 only
        try:
            ticker = yf.Ticker(stock['symbol'])
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[-2]
                change_pct = ((current - previous) / previous) * 100
                
                result = {
                    'source': 'Yahoo Finance',
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'price': round(current, 2),
                    'change_pct': round(change_pct, 2),
                    'currency': info.get('currency', 'Unknown'),
                    'success': True
                }
                results.append(result)
                print(f"  ✅ {stock['name']}: {current:.2f} ({change_pct:+.2f}%)")
            else:
                print(f"  ⚠️  {stock['name']}: Insufficient data")
                
        except Exception as e:
            print(f"  ❌ {stock['name']}: {str(e)[:50]}")
            results.append({
                'source': 'Yahoo Finance',
                'symbol': stock['symbol'],
                'name': stock['name'],
                'success': False,
                'error': str(e)[:100]
            })
    
    return results

def test_nasdaq_nordic():
    """Test Nasdaq Nordic XML API"""
    print("\n" + "=" * 60)
    print("TEST 2: NASDAQ NORDIC XML API")
    print("=" * 60)
    
    try:
        import requests
        print("✅ requests is available")
    except ImportError:
        print("❌ requests not available")
        return []
    
    results = []
    print("\n📊 Fetching data from Nasdaq Nordic...")
    
    # Test with Nordea as example
    # Nasdaq Nordic uses specific instrument IDs
    test_stocks = [
        {'omx_id': '36581', 'name': 'Nordea Bank', 'symbol': 'NDA-SE.ST'},
        {'omx_id': '9924', 'name': 'Handelsbanken A', 'symbol': 'SHB-A.ST'},
    ]
    
    for stock in test_stocks:
        try:
            # Nasdaq Nordic API endpoint for instrument info
            url = f"https://www.nasdaqomxnordic.com/webproxy/DataFeedProxy.aspx?SubSystem=Prices&Action=GetInstrument&Instrument={stock['omx_id']}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Parse XML response (simplified)
                content = response.text[:500]
                print(f"  ✅ {stock['name']}: API responding")
                print(f"     Response preview: {content[:200]}...")
                
                results.append({
                    'source': 'Nasdaq Nordic',
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'success': True,
                    'response_preview': content[:200]
                })
            else:
                print(f"  ⚠️  {stock['name']}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {stock['name']}: {str(e)[:50]}")
            results.append({
                'source': 'Nasdaq Nordic',
                'symbol': stock['symbol'],
                'name': stock['name'],
                'success': False,
                'error': str(e)[:100]
            })
    
    return results

def test_nasdaq_csv_export():
    """Test Nasdaq Nordic CSV export (alternative method)"""
    print("\n" + "=" * 60)
    print("TEST 3: NASDAQ NORDIC CSV EXPORT")
    print("=" * 60)
    
    try:
        import requests
        import pandas as pd
        print("✅ pandas is available")
    except ImportError:
        print("⚠️  pandas not available, trying without...")
        import requests
        pd = None
    
    results = []
    print("\n📊 Testing CSV download...")
    
    try:
        # Nasdaq Nordic provides CSV exports for historical data
        # Format: https://www.nasdaqomxnordic.com/webproxy/DataFeedProxy.aspx?
        # SubSystem=Prices&Action=GetHistoricQuote&Instrument=36581&FromDate=2026-02-23&ToDate=2026-02-24
        
        url = "https://www.nasdaqomxnordic.com/webproxy/DataFeedProxy.aspx?SubSystem=Prices&Action=GetHistoricQuote&Instrument=36581&FromDate=2026-02-20&ToDate=2026-02-24"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            print(f"  ✅ CSV data retrieved ({len(response.text)} chars)")
            print(f"  Preview: {response.text[:300]}...")
            
            results.append({
                'source': 'Nasdaq Nordic CSV',
                'success': True,
                'data_size': len(response.text),
                'preview': response.text[:300]
            })
        else:
            print(f"  ⚠️  HTTP {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")
        results.append({
            'source': 'Nasdaq Nordic CSV',
            'success': False,
            'error': str(e)[:100]
        })
    
    return results

def compare_results(yahoo_results, nasdaq_results):
    """Compare both APIs"""
    print("\n" + "=" * 60)
    print("📊 COMPARISON SUMMARY")
    print("=" * 60)
    
    yahoo_success = sum(1 for r in yahoo_results if r.get('success'))
    nasdaq_success = sum(1 for r in nasdaq_results if r.get('success'))
    
    print(f"\nYahoo Finance:")
    print(f"  ✅ Successful: {yahoo_success}/{len(yahoo_results)}")
    print(f"  📈 Data: Real-time prices, changes, volume")
    print(f"  💰 Cost: Free")
    print(f"  ⚡ Speed: Fast")
    print(f"  🌍 Coverage: Global (all your holdings)")
    
    print(f"\nNasdaq Nordic:")
    print(f"  ✅ Successful: {nasdaq_success}/{len(nasdaq_results)}")
    print(f"  📈 Data: Exchange official data")
    print(f"  💰 Cost: Free (undocumented)")
    print(f"  ⚡ Speed: Moderate")
    print(f"  🌍 Coverage: Nordic only")
    
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDATION")
    print("=" * 60)
    
    if yahoo_success >= nasdaq_success:
        print("""
✅ Use YAHOO FINANCE as PRIMARY source
   - Best coverage for your portfolio (SE, NO, FI, DK)
   - Simple Python library
   - Reliable for daily prices

⚠️  Use Nasdaq Nordic as FALLBACK
   - For OMX-specific data
   - When Yahoo has issues
   - For verification
""")
    else:
        print("""
✅ Use NASDAQ NORDIC as PRIMARY source
   - Official exchange data
   - More reliable for Nordic stocks

⚠️  Use Yahoo Finance for international holdings
""")

if __name__ == "__main__":
    print("🚀 INVESTMENT AGENT - API TEST")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Portfolio: {len(PORTFOLIO)} stocks (SE, NO, FI, DK)")
    
    # Run tests
    yahoo_results = test_yahoo_finance()
    nasdaq_results = test_nasdaq_nordic()
    csv_results = test_nasdaq_csv_export()
    
    # Compare
    compare_results(yahoo_results, nasdaq_results + csv_results)
    
    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'yahoo_finance': yahoo_results,
        'nasdaq_nordic': nasdaq_results,
        'nasdaq_csv': csv_results
    }
    
    with open('/home/richard-laurits/.openclaw/workspace/agents/investment-agent/api_test_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Results saved to: api_test_results.json")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
