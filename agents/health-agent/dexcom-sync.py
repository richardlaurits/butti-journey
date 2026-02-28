#!/usr/bin/env python3
"""
Dexcom API + Trio AID Integration
Fetch real-time glucose data, TIR, and trends

Richard uses Trio (open-source DIY AID) which:
- Manages Omnipod DASH pump
- Integrates Dexcom G7 CGM
- Uses Fiasp insulin
- Can export data to Nightscout/APIs

This script handles both:
1. Direct Dexcom API (if configured)
2. Trio data export (preferred - already has all data)
"""

import os
import json
import requests
from datetime import datetime, timedelta

# Dexcom API endpoints
DEXCOM_API_BASE = "https://api.dexcom.com/v3"
DEXCOM_OAUTH_TOKEN_URL = "https://api.dexcom.com/v3/oauth/token"

class DexcomClient:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        """Initialize Dexcom API client"""
        self.client_id = client_id or os.environ.get("DEXCOM_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("DEXCOM_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or "http://localhost:8080/callback"
        self.access_token = None
        self.refresh_token = None
    
    def get_authorization_url(self):
        """Get OAuth authorization URL for user to approve"""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": "offline_access glucose activity",
            "redirect_uri": self.redirect_uri
        }
        
        url = f"{DEXCOM_API_BASE}/oauth/authorize"
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        
        return f"{url}?{query_string}"
    
    def exchange_auth_code(self, auth_code):
        """Exchange authorization code for tokens"""
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri
        }
        
        try:
            resp = requests.post(DEXCOM_OAUTH_TOKEN_URL, data=data, timeout=10)
            resp.raise_for_status()
            
            token_data = resp.json()
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            
            # Save tokens
            self.save_tokens()
            
            return True
        except Exception as e:
            print(f"❌ Token exchange failed: {e}")
            return False
    
    def save_tokens(self):
        """Save tokens to file"""
        tokens = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "saved_at": datetime.now().isoformat()
        }
        
        os.makedirs("agents/health-agent/config", exist_ok=True)
        
        with open("agents/health-agent/config/dexcom-tokens.json", 'w') as f:
            json.dump(tokens, f)
        
        print("✅ Dexcom tokens saved")
    
    def load_tokens(self):
        """Load saved tokens"""
        try:
            with open("agents/health-agent/config/dexcom-tokens.json", 'r') as f:
                tokens = json.load(f)
                self.access_token = tokens.get("access_token")
                self.refresh_token = tokens.get("refresh_token")
                return True
        except FileNotFoundError:
            return False
    
    def get_glucose_readings(self, days_back=7):
        """Fetch recent glucose readings"""
        if not self.access_token:
            if not self.load_tokens():
                print("❌ No Dexcom token available")
                return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Get readings from last N days
            start_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            url = f"{DEXCOM_API_BASE}/gluerecords"
            params = {
                "startDate": start_date
            }
            
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            
            data = resp.json()
            return data.get("records", [])
            
        except Exception as e:
            print(f"❌ Error fetching glucose: {e}")
            return None
    
    def calculate_tir(self, readings, target_low=70, target_high=180):
        """Calculate Time In Range from readings"""
        if not readings:
            return None
        
        in_range = sum(1 for r in readings 
                      if target_low <= r.get("value", 0) <= target_high)
        
        tir = (in_range / len(readings)) * 100 if readings else 0
        
        return {
            "tir_pct": tir,
            "readings_total": len(readings),
            "in_range": in_range,
            "target_low": target_low,
            "target_high": target_high,
            "avg_glucose": sum(r.get("value", 0) for r in readings) / len(readings) if readings else 0
        }
    
    def get_weekly_summary(self):
        """Get weekly TIR summary"""
        readings = self.get_glucose_readings(days_back=7)
        
        if not readings:
            return None
        
        return self.calculate_tir(readings)

def setup_dexcom():
    """Interactive setup for Dexcom OAuth"""
    print("\n🔐 Dexcom API Setup\n")
    
    client_id = input("Enter your Dexcom Client ID: ").strip()
    client_secret = input("Enter your Dexcom Client Secret: ").strip()
    redirect_uri = input("Enter redirect URI (default: http://localhost:8080/callback): ").strip()
    
    if not redirect_uri:
        redirect_uri = "http://localhost:8080/callback"
    
    client = DexcomClient(client_id, client_secret, redirect_uri)
    
    print(f"\n1. Visit this URL to authorize:\n")
    print(client.get_authorization_url())
    print(f"\n2. After authorizing, you'll get a code in the redirect URL")
    
    auth_code = input("\n3. Paste the authorization code here: ").strip()
    
    if client.exchange_auth_code(auth_code):
        print("✅ Dexcom API configured!")
        return client
    else:
        print("❌ Setup failed")
        return None

def fetch_trio_data(data_export_path=None):
    """
    Fetch glucose data from Trio AID export
    
    Trio can export data to:
    - Nightscout MongoDB
    - Local JSON files
    - Cloud storage
    
    This method is PREFERRED over Dexcom API because:
    1. Trio already has all the data
    2. No additional OAuth needed
    3. Includes insulin, carb, and activity data
    4. Open-source (full data access)
    """
    print("\n🏥 Trio AID Integration")
    print("\nOptions to get Trio data:")
    print("1. Nightscout: If Trio syncs to Nightscout instance")
    print("2. Direct export: Trio can export JSON locally")
    print("3. API: Check Trio's documentation for data API")
    print("\nAsk Richard: Where does your Trio export data?")
    return None

if __name__ == "__main__":
    # Test setup
    print("🩺 Dexcom/Trio Integration Setup\n")
    
    # Check for Trio first (preferred)
    print("1️⃣ Checking for Trio AID data...")
    trio_data = fetch_trio_data()
    
    if trio_data:
        print("✅ Found Trio data!")
    else:
        print("⏳ Trio not configured")
        print("\n2️⃣ Dexcom API as fallback...")
        
        client = DexcomClient()
        
        if client.load_tokens():
            print("✅ Found existing Dexcom tokens")
            summary = client.get_weekly_summary()
            if summary:
                print(f"\n📊 Weekly TIR: {summary['tir_pct']:.1f}%")
                print(f"Avg Glucose: {summary['avg_glucose']:.0f} mg/dL")
        else:
            print("⏳ Need to set up Dexcom OAuth")
            print("\nOr better: Configure Trio data export!")
            print("This gives access to carbs + insulin + activity data together.")
