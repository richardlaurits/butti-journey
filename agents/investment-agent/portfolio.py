# Richard's Nordic Dividend Portfolio
# Created: 2026-02-24
# Total positions: 14 stocks across SE, NO, FI, DK

PORTFOLIO = [
    # Swedish Banks (core holding ~40%)
    {"symbol": "NDA SE", "name": "Nordea Bank", "weight": 15.11, "country": "SE", "sector": "Bank"},
    {"symbol": "SHB A", "name": "Handelsbanken A", "weight": 13.35, "country": "SE", "sector": "Bank"},
    {"symbol": "SWED A", "name": "Swedbank A", "weight": 11.79, "country": "SE", "sector": "Bank"},
    
    # Swedish Telecom & Industrials
    {"symbol": "TEL2 B", "name": "Tele2 B", "weight": 11.63, "country": "SE", "sector": "Telecom"},
    {"symbol": "VOLV B", "name": "Volvo B", "weight": 4.73, "country": "SE", "sector": "Industrials"},
    {"symbol": "ESSITY B", "name": "Essity B", "weight": 3.89, "country": "SE", "sector": "Consumer Staples"},
    {"symbol": "SAND", "name": "Sandvik", "weight": 3.88, "country": "SE", "sector": "Industrials"},
    {"symbol": "INVE B", "name": "Investor B", "weight": 3.11, "country": "SE", "sector": "Investment"},
    {"symbol": "ABB", "name": "ABB", "weight": 2.76, "country": "SE", "sector": "Industrials"},
    
    # Norwegian
    {"symbol": "EQNR", "name": "Equinor", "weight": 7.11, "country": "NO", "sector": "Energy"},
    {"symbol": "ORK", "name": "Orkla", "weight": 6.25, "country": "NO", "sector": "Consumer Goods"},
    
    # Finnish
    {"symbol": "SAMPO", "name": "Sampo A", "weight": 6.70, "country": "FI", "sector": "Insurance"},
    {"symbol": "UPM", "name": "UPM-Kymmene", "weight": 4.84, "country": "FI", "sector": "Materials"},
    
    # Danish
    {"symbol": "NOVO B", "name": "Novo Nordisk B", "weight": 4.86, "country": "DK", "sector": "Pharma"},
]

# For reference when searching news
COMPANY_NAMES_FOR_SEARCH = [
    "Nordea", "Handelsbanken", "Swedbank", "Tele2", "Equinor", 
    "Sampo", "Orkla", "Novo Nordisk", "UPM", "Volvo", 
    "Essity", "Sandvik", "Investor", "ABB"
]

# Stockholm OMX tickers (for price lookup)
OMX_TICKERS = {
    "NDA SE": "NDA-SE",
    "SHB A": "SHB-A", 
    "SWED A": "SWEDA",
    "TEL2 B": "TEL2-B",
    "VOLV B": "VOLV-B",
    "ESSITY B": "ESSITY-B",
    "SAND": "SAND",
    "INVE B": "INVE-B",
    "ABB": "ABB"
}
