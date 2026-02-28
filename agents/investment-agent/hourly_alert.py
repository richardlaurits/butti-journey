#!/usr/bin/env python3
"""
Investment Alert System - Hourly Price Monitoring
Checks for unusual price movements during market hours
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace')

try:
    import yfinance as yf
except ImportError:
    print("yfinance not available")
    sys.exit(1)

# Portfolio definition
PORTFOLIO = [
    {"symbol": "NDA-SE.ST", "name": "Nordea Bank", "weight": 15.11, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "SHB-A.ST", "name": "Handelsbanken A", "weight": 13.35, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "SWED-A.ST", "name": "Swedbank A", "weight": 11.79, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "TEL2-B.ST", "name": "Tele2 B", "weight": 11.63, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "VOLV-B.ST", "name": "Volvo B", "weight": 4.73, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "ESSITY-B.ST", "name": "Essity B", "weight": 3.89, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "SAND.ST", "name": "Sandvik", "weight": 3.88, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "INVE-B.ST", "name": "Investor B", "weight": 3.11, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "ABB.ST", "name": "ABB", "weight": 2.76, "country": "SE", "alert_threshold": 3.0},
    {"symbol": "EQNR.OL", "name": "Equinor", "weight": 7.11, "country": "NO", "alert_threshold": 4.0},
    {"symbol": "ORK.OL", "name": "Orkla", "weight": 6.25, "country": "NO", "alert_threshold": 4.0},
    {"symbol": "SAMPO.HE", "name": "Sampo A", "weight": 6.70, "country": "FI", "alert_threshold": 4.0},
    {"symbol": "UPM.HE", "name": "UPM-Kymmene", "weight": 4.84, "country": "FI", "alert_threshold": 4.0},
    {"symbol": "NOVO-B.CO", "name": "Novo Nordisk B", "weight": 4.86, "country": "DK", "alert_threshold": 5.0},  # Higher threshold - more volatile
]

FLAGS = {"SE": "🇸🇪", "NO": "🇳🇴", "FI": "🇫🇮", "DK": "🇩🇰"}
ALERT_LOG = Path('/home/richard-laurits/.openclaw/workspace/agents/investment-agent/data/alerts.json')

def load_previous_alerts():
    """Load previous alerts to avoid duplicates"""
    if ALERT_LOG.exists():
        with open(ALERT_LOG, 'r') as f:
            return json.load(f)
    return {"alerts": [], "last_check": None}

def save_alert(alert_data):
    """Save alert to log"""
    data = load_previous_alerts()
    data["alerts"].append({
        "timestamp": datetime.now().isoformat(),
        **alert_data
    })
    data["last_check"] = datetime.now().isoformat()
    
    # Keep only last 100 alerts
    data["alerts"] = data["alerts"][-100:]
    
    ALERT_LOG.parent.mkdir(exist_ok=True)
    with open(ALERT_LOG, 'w') as f:
        json.dump(data, f, indent=2)

def was_recently_alerted(symbol, minutes=60):
    """Check if we already alerted for this symbol recently"""
    data = load_previous_alerts()
    cutoff = datetime.now() - timedelta(minutes=minutes)
    
    for alert in reversed(data.get("alerts", [])):
        if alert.get("symbol") == symbol:
            alert_time = datetime.fromisoformat(alert["timestamp"])
            if alert_time > cutoff:
                return True
    return False

def get_intraday_data():
    """Fetch intraday price data"""
    results = []
    errors = []
    
    for stock in PORTFOLIO:
        try:
            ticker = yf.Ticker(stock['symbol'])
            # Get 5 days of data to calculate change from previous close
            hist = ticker.history(period="5d")
            
            if len(hist) >= 1:
                current = hist['Close'].iloc[-1]
                # Calculate change from previous trading day close
                if len(hist) >= 2:
                    prev_close = hist['Close'].iloc[-2]
                else:
                    prev_close = hist['Open'].iloc[-1]
                
                change_pct = ((current - prev_close) / prev_close) * 100
                
                results.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'weight': stock['weight'],
                    'country': stock['country'],
                    'threshold': stock['alert_threshold'],
                    'price': round(current, 2),
                    'change_pct': round(change_pct, 2),
                    'prev_close': round(prev_close, 2),
                    'success': True
                })
            else:
                errors.append(f"{stock['name']}: No data")
                
        except Exception as e:
            errors.append(f"{stock['name']}: {str(e)[:50]}")
    
    return results, errors

def detect_unusual_moves(data):
    """Detect unusual price movements"""
    alerts = []
    
    for stock in data:
        change = abs(stock['change_pct'])
        threshold = stock['threshold']
        
        # Alert if:
        # 1. Change exceeds threshold AND
        # 2. Not recently alerted for this stock
        if change >= threshold and not was_recently_alerted(stock['symbol']):
            alert_type = "🚀 UP" if stock['change_pct'] > 0 else "🔻 DOWN"
            
            alerts.append({
                'symbol': stock['symbol'],
                'name': stock['name'],
                'country': stock['country'],
                'price': stock['price'],
                'change_pct': stock['change_pct'],
                'threshold': threshold,
                'alert_type': alert_type,
                'severity': 'HIGH' if change >= 10 else 'MEDIUM' if change >= 5 else 'LOW'
            })
            
            # Save to log
            save_alert({
                'symbol': stock['symbol'],
                'name': stock['name'],
                'change_pct': stock['change_pct'],
                'severity': 'HIGH' if change >= 10 else 'MEDIUM' if change >= 5 else 'LOW'
            })
    
    return alerts

def format_alert_message(alerts, check_time):
    """Format alerts for Telegram"""
    if not alerts:
        return None  # No output if no alerts
    
    lines = []
    
    # Header
    high_severity = any(a['severity'] == 'HIGH' for a in alerts)
    if high_severity:
        lines.append("🚨 **PORTFÖLJ-ALERT**")
    else:
        lines.append("⚠️ Portfölj-notis")
    
    lines.append(f"📊 {check_time.strftime('%H:%M')} CET | Timme {check_time.hour - 9 + 1} av börsdagen")
    lines.append("")
    
    # Sort by severity and change magnitude
    alerts.sort(key=lambda x: (0 if x['severity'] == 'HIGH' else 1 if x['severity'] == 'MEDIUM' else 2, abs(x['change_pct'])), reverse=True)
    
    for alert in alerts:
        flag = FLAGS.get(alert['country'], '')
        emoji = "🚀" if alert['change_pct'] > 0 else "🔻"
        
        lines.append(f"{emoji} {flag} **{alert['name']}**")
        lines.append(f"   {alert['change_pct']:+.2f}% | {alert['price']:.2f}")
        
        # Add context for high severity
        if alert['severity'] == 'HIGH':
            if alert['change_pct'] > 0:
                lines.append(f"   💡 Kursen har rusat >10%!")
            else:
                lines.append(f"   💡 Kursen har fallit >10%!")
        
        lines.append("")
    
    lines.append("—")
    lines.append("📈 Detta är en automatisk bevakning.")
    lines.append("🕐 Nästa check om en timme (om börsen är öppen).")
    
    return "\n".join(lines)

def main():
    """Main function - check for alerts"""
    now = datetime.now()
    
    # Check if markets are open (Nordic: 09:00-17:30 CET)
    # Only run alerts if it's a weekday and between 09:00-17:30
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        print("Weekend - markets closed", file=sys.stderr)
        sys.exit(0)
    
    if now.hour < 9 or now.hour >= 18:
        print("Markets closed", file=sys.stderr)
        sys.exit(0)
    
    print(f"Checking portfolio at {now.strftime('%H:%M')}...", file=sys.stderr)
    
    # Get data
    data, errors = get_intraday_data()
    
    if errors:
        print(f"Warnings: {', '.join(errors[:3])}", file=sys.stderr)
    
    if not data:
        print("❌ Kunde inte hämta data", file=sys.stderr)
        sys.exit(1)
    
    # Detect unusual moves
    alerts = detect_unusual_moves(data)
    
    # Format output
    message = format_alert_message(alerts, now)
    
    if message:
        print(message)
        print(f"🚨 {len(alerts)} alert(s) generated", file=sys.stderr)
    else:
        print("✅ Inga ovanliga rörelser", file=sys.stderr)

if __name__ == "__main__":
    main()
