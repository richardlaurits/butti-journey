#!/usr/bin/env python3
"""
Career Agent: Smart Playwright Job Search
Handles JavaScript-heavy job portals
Searches for director/VP/business development roles
"""

from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime
import time

# Search configurations for each company
SEARCHES = [
    {
        "company": "Novo Nordisk",
        "search_url": "https://careers.novonordisk.com/search/",
        "country_param": "?location=",
        "countries": ["Switzerland", "Denmark"],
        "search_terms": ["Director", "VP", "Business Development", "Commercial", "Strategic"],
    },
    {
        "company": "Roche",
        "search_url": "https://careers.roche.com/global/en/search-results",
        "country_param": "?location=",
        "countries": ["Switzerland"],
        "search_terms": ["Director", "VP", "Business Development"],
    },
    {
        "company": "BD",
        "search_url": "https://www.bd.com/careers/search",
        "country_param": "?location=",
        "countries": ["Switzerland", "Denmark"],
        "search_terms": ["Director", "VP", "Business Development"],
    },
]

def score_job(title, location=""):
    """Score job match 0-10"""
    score = 0
    text = f"{title} {location}".lower()
    
    # Keywords
    keywords = ["director", "vp", "business development", "commercial", "strategy", "product", "lead"]
    for kw in keywords:
        if kw in text:
            score += 2
    
    # Location
    if any(loc.lower() in text for loc in ["switzerland", "denmark", "zurich", "geneva", "copenhagen"]):
        score += 2
    
    # Industry
    for ind in ["medical", "medtech", "healthcare", "pharma", "diabetes", "device"]:
        if ind in text:
            score += 1
            break
    
    return min(score, 10)

def search_company_jobs(company_name, search_url, countries, search_terms):
    """Use Playwright to search company jobs"""
    jobs = []
    
    print(f"\n🔍 Searching {company_name}...")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(20000)
            
            # Navigate to search page
            page.goto(search_url, wait_until="domcontentloaded")
            time.sleep(3)  # Wait for JS rendering
            
            print(f"  ✅ Page loaded: {page.title()}")
            
            # Try to find search/filter inputs
            search_input = page.query_selector('input[placeholder*="search"], input[placeholder*="Search"], input[type="search"]')
            
            if search_input:
                print(f"  🔎 Found search input")
                # Search for director roles
                search_input.fill("Director")
                search_input.press("Enter")
                time.sleep(2)
            
            # Look for job listings
            job_selectors = [
                'div[class*="job-item"]',
                'div[class*="job-card"]',
                'div[class*="posting"]',
                'a[class*="job"]',
                'li[class*="job"]',
                'article',
            ]
            
            found_jobs = False
            for selector in job_selectors:
                job_elements = page.query_selector_all(selector)
                
                if len(job_elements) > 0:
                    print(f"  📋 Found {len(job_elements)} job elements")
                    found_jobs = True
                    
                    for elem in job_elements[:20]:  # First 20
                        try:
                            title_elem = elem.query_selector('h2, h3, h4, a, span[class*="title"]')
                            if not title_elem:
                                continue
                            
                            title = title_elem.text_content().strip()
                            if not title or len(title) < 5:
                                continue
                            
                            # Try to get location
                            location_elem = elem.query_selector('span[class*="location"], div[class*="location"], span[class*="place"]')
                            location = location_elem.text_content().strip() if location_elem else ""
                            
                            # Try to get link
                            link_elem = elem.query_selector('a')
                            link = link_elem.get_attribute('href') if link_elem else search_url
                            if link and not link.startswith('http'):
                                link = search_url.split('/search')[0] + link
                            
                            score = score_job(title, location)
                            
                            if score >= 6:
                                jobs.append({
                                    'company': company_name,
                                    'title': title[:150],
                                    'location': location[:100],
                                    'url': link,
                                    'score': score,
                                    'source': 'playwright-search',
                                    'found_at': datetime.now().isoformat()
                                })
                                
                                print(f"    ✅ {title} | Score: {score}/10 | {location}")
                        except:
                            continue
                    
                    if found_jobs:
                        break
            
            if not found_jobs:
                print(f"  ⏳ No job elements found (may need manual navigation)")
            
            browser.close()
        
        return jobs
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
        return []

def main():
    print(f"\n{'='*60}")
    print(f"🎯 CAREER AGENT - DIRECTOR/VP JOB SEARCH")
    print(f"Companies: Novo Nordisk, Roche, BD")
    print(f"{'='*60}")
    
    all_jobs = []
    
    for search in SEARCHES:
        company = search["company"]
        url = search["search_url"]
        countries = search["countries"]
        
        jobs = search_company_jobs(company, url, countries, search["search_terms"])
        all_jobs.extend(jobs)
        time.sleep(2)
    
    # Sort by score
    all_jobs.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTS: {len(all_jobs)} jobs found")
    print(f"{'='*60}")
    
    if all_jobs:
        print(f"\n🏆 TOP MATCHES:\n")
        for i, job in enumerate(all_jobs[:10], 1):
            print(f"{i}. 🎯 Score: {job['score']}/10")
            print(f"   **{job['title']}**")
            print(f"   🏢 {job['company']}")
            if job['location']:
                print(f"   📍 {job['location']}")
            print(f"   🔗 {job['url'][:60]}...")
            print()
    else:
        print("\n⏳ No matching jobs found (sites may require manual browsing)")
        print("\nNext steps:")
        print("  1. Visit https://careers.novonordisk.com/ directly")
        print("  2. Try advanced search/filters")
        print("  3. Or I can help with speculative outreach")
    
    # Save results
    os.makedirs("agents/career-agent/data", exist_ok=True)
    output_file = f"agents/career-agent/data/novo-nordisk-search-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(all_jobs[:20], f, indent=2)
    
    if all_jobs:
        print(f"\n📁 Saved to: {output_file}")
    
    return all_jobs

if __name__ == "__main__":
    main()
