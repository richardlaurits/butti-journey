#!/usr/bin/env python3
"""
Career Agent - Commercial Roles in CH/DK/SE
Focus: Marketing, BD, Strategy, Commercial, Director-level roles
Approach: Direct job page access without login
"""

import json
from datetime import datetime
from pathlib import Path

# Target: Commercial roles in Switzerland, Denmark, Sweden
TARGET_ROLES = [
    "marketing", "director", "manager", "strategy", "commercial", 
    "business development", "bd", "head of", "vp", "vice president",
    "general manager", "managing director", "sales", "product manager"
]

TARGET_COUNTRIES = ["switzerland", "swiss", "schweiz", "denmark", "danmark", 
                    "sweden", "sverige", "geneva", "zurich", "basel", 
                    "copenhagen", "stockholm", "gothenburg", "malmö"]

COMPANIES = {
    "Novo Nordisk": {
        "career_url": "https://www.novonordisk.com/careers/find-a-job.html",
        "jobs_url": "https://www.novonordisk.com/careers/find-a-job.html",
        "method": "HTTP + search params"
    },
    "Roche": {
        "career_url": "https://careers.roche.com/global/en",
        "jobs_url": "https://careers.roche.com/global/en/listjobs",
        "method": "HTTP + search params"
    },
    "IQVIA": {
        "career_url": "https://jobs.iqvia.com/en/jobs",
        "jobs_url": "https://jobs.iqvia.com/en/jobs",
        "method": "HTTP + filters"
    },
    "Glooko": {
        "career_url": "https://glooko.com/careers/",
        "method": "Direct page scrape"
    },
    "Ypsomed": {
        "career_url": "https://www.ypsomed.com/en/careers",
        "method": "Direct page scrape"
    },
    "Rubin Medical": {
        "career_url": "https://rubinmedical.com/careers",
        "method": "Direct page scrape"
    },
    "BD": {
        "career_url": "https://jobs.bd.com/",
        "method": "Search with keywords"
    },
    "Eitan Medical": {
        "career_url": "https://www.eitanmedical.com/careers",
        "method": "Direct page scrape"
    },
    "Micrel Medical": {
        "career_url": "https://www.micrelmedical.com/careers",
        "method": "Direct page scrape"
    },
    "Medtronic": {
        "career_url": "https://www.medtronic.com/us-en/careers.html",
        "method": "Search with filters"
    },
    "Insulet": {
        "career_url": "https://www.insulet.com/careers",
        "method": "Direct page scrape"
    },
    "Ideon": {
        "career_url": "https://www.ideon.ai/careers",
        "method": "Direct page scrape"
    }
}

def search_company_jobs(company_name, company_data):
    """
    Search for commercial roles at specific company
    Focus on CH/DK/SE locations
    """
    import requests
    from bs4 import BeautifulSoup
    
    jobs_found = []
    url = company_data.get("jobs_url") or company_data.get("career_url")
    
    print(f"\n🔍 {company_name}")
    print(f"   URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for job listings - various selectors
            job_selectors = [
                '.job-listing', '.job-title', '[data-automation-id="jobListing"]',
                '.position-title', '.job-name', '.opening', '.career-item'
            ]
            
            jobs = []
            for selector in job_selectors:
                elements = soup.select(selector)
                if elements:
                    jobs.extend(elements)
            
            print(f"   Found {len(jobs)} potential job elements")
            
            # Extract job info
            for job in jobs[:20]:  # Check first 20
                text = job.get_text(strip=True).lower()
                
                # Check if it matches target roles
                role_match = any(role in text for role in TARGET_ROLES)
                
                # Check if it's in target countries
                location_match = any(country in text for country in TARGET_COUNTRIES)
                
                if role_match and location_match:
                    jobs_found.append({
                        'title': job.get_text(strip=True)[:100],
                        'company': company_name,
                        'url': url,
                        'matched_roles': [r for r in TARGET_ROLES if r in text][:2],
                        'matched_countries': [c for c in TARGET_COUNTRIES if c in text][:2]
                    })
        else:
            print(f"   HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   Error: {str(e)[:60]}")
    
    print(f"   ✅ Relevant jobs: {len(jobs_found)}")
    return jobs_found

def main():
    """Main function - search all companies"""
    print("=" * 70)
    print("CAREER AGENT - Commercial Roles in CH/DK/SE")
    print("=" * 70)
    print(f"Target roles: {', '.join(TARGET_ROLES[:5])}...")
    print(f"Target countries: Switzerland, Denmark, Sweden")
    print()
    
    all_jobs = []
    
    # Test 3-4 companies per run (to not overwhelm)
    test_companies = ["Novo Nordisk", "Roche", "IQVIA", "BD"]
    
    for company in test_companies:
        if company in COMPANIES:
            jobs = search_company_jobs(company, COMPANIES[company])
            all_jobs.extend(jobs)
    
    # Results
    print("\n" + "=" * 70)
    print(f"RESULTS: {len(all_jobs)} commercial jobs found in CH/DK/SE")
    print("=" * 70)
    
    if all_jobs:
        print("\n🎯 TOP MATCHES:")
        for i, job in enumerate(all_jobs[:10], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   URL: {job['url']}")
            if job.get('matched_roles'):
                print(f"   Role match: {', '.join(job['matched_roles'])}")
            if job.get('matched_countries'):
                print(f"   Location: {', '.join(job['matched_countries'])}")
    else:
        print("\n⚠️  No matching jobs found via HTTP scraping")
        print("\n💡 RECOMMENDATION:")
        print("   - Sites may require JavaScript (Playwright)")
        print("   - Try API-based search instead")
        print("   - Or use email-parsing from LinkedIn/Indeed")
    
    # Save results
    result = {
        "timestamp": datetime.now().isoformat(),
        "target": "Commercial roles in CH/DK/SE",
        "jobs_found": len(all_jobs),
        "jobs": all_jobs
    }
    
    with open("/tmp/career_commercial_scan.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Saved to: /tmp/career_commercial_scan.json")

if __name__ == "__main__":
    main()
