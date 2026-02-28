#!/usr/bin/env python3
"""
Career Agent - Brave Search Job Finder
Searches for commercial roles at target companies in CH/DK/SE
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Load API key
BRAVE_API_KEY = os.getenv('BRAVE_SEARCH_API_KEY', 'BSAI8QbrhfyRgz5CgfX-SKgV4a5j8T8')

# Configuration
COMPANIES = [
    "Novo Nordisk",
    "Roche", 
    "IQVIA",
    "Glooko",
    "Ypsomed",
    "Rubin Medical",
    "BD",
    "Eitan Medical",
    "Micrel Medical",
    "Minimed",
    "Medtronic",
    "Insulet",
    "Ideon"
]

ROLES = [
    "marketing director",
    "commercial manager", 
    "business development",
    "strategy manager",
    "product manager",
    "sales director",
    "general manager",
    "head of marketing"
]

LOCATIONS = ["Switzerland", "Denmark", "Sweden"]

def search_brave(query):
    """Search using Brave Search API"""
    url = "https://api.search.brave.com/res/v1/web/search"
    
    headers = {
        "X-Subscription-Token": BRAVE_API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "q": query,
        "count": 10,
        "offset": 0,
        "mkt": "en-US",
        "safesearch": "off",
        "freshness": "week"  # Last week only
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"   Request Error: {str(e)[:60]}")
        return None

def find_jobs():
    """Find jobs using Brave Search"""
    print("=" * 70)
    print("CAREER AGENT - Brave Search Job Finder")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Target: {len(COMPANIES)} companies")
    print(f"Roles: {len(ROLES)} role types")
    print(f"Locations: {', '.join(LOCATIONS)}")
    print()
    
    all_jobs = []
    
    # Search each company-location combination
    for company in COMPANIES[:5]:  # Test with first 5 companies
        for location in LOCATIONS[:2]:  # Test with CH and DK first
            
            query = f'"{company}" "{location}" jobs careers "marketing" OR "director" OR "manager" site:{company.lower().replace(" ", "")}.com'
            
            print(f"🔍 Searching: {company} in {location}")
            print(f"   Query: {query[:70]}...")
            
            result = search_brave(query)
            
            if result and 'web' in result and 'results' in result['web']:
                results = result['web']['results']
                print(f"   Found {len(results)} results")
                
                for item in results[:5]:  # Top 5 results
                    title = item.get('title', '')
                    url = item.get('url', '')
                    desc = item.get('description', '')
                    
                    # Check if it looks like a job posting
                    if any(word in title.lower() for word in ['job', 'career', 'position', 'opening']):
                        all_jobs.append({
                            'title': title[:100],
                            'company': company,
                            'location': location,
                            'url': url,
                            'description': desc[:200] if desc else ''
                        })
                        print(f"   ✅ Job: {title[:60]}")
            else:
                print(f"   No results or API error")
            
            print()
    
    # Summary
    print("=" * 70)
    print(f"RESULTS: {len(all_jobs)} jobs found via Brave Search")
    print("=" * 70)
    
    if all_jobs:
        print("\n🎯 TOP MATCHES:")
        for i, job in enumerate(all_jobs[:15], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   URL: {job['url']}")
    else:
        print("\n⚠️  No jobs found via Brave Search")
        print("\n💡 Possible reasons:")
        print("   - Brave Search API limits (1 request/second)")
        print("   - Job postings not indexed by search engines")
        print("   - Need more specific queries")
    
    # Save results
    result_data = {
        "timestamp": datetime.now().isoformat(),
        "method": "Brave Search API",
        "jobs_found": len(all_jobs),
        "jobs": all_jobs
    }
    
    with open("/tmp/brave_job_search.json", "w") as f:
        json.dump(result_data, f, indent=2)
    
    print(f"\n💾 Results saved: /tmp/brave_job_search.json")
    
    return all_jobs

if __name__ == "__main__":
    jobs = find_jobs()
