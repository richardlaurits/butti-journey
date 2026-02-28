#!/usr/bin/env python3
"""
Career Agent: Playwright-based Company Job Board Crawler
Handles JavaScript-rendered content + dynamic job listings
Runs Mon-Fri, 8 AM CET
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import json
import os
from datetime import datetime
from pathlib import Path
import time

# Target companies with careers page URLs
COMPANIES = {
    # Denmark
    "Novo Nordisk": "https://careers.novonordisk.com/",
    "IQVIA": "https://www.iqvia.com/careers",
    
    # Sweden  
    "Glooko": "https://www.glooko.com/careers",
    
    # Switzerland
    "Tandem Diabetes": "https://www.tandemdiabetes.com/careers",
    "BD": "https://www.bd.com/careers",
    "Haleon": "https://www.haleon.com/careers",
    "Roche": "https://careers.roche.com/global/en",
}

# Richard's search criteria
TARGET_KEYWORDS = [
    "director", "senior manager", "vp", "chief", "head of",
    "business development", "corporate development", "product strategy",
    "go-to-market", "commercial", "strategic partnerships",
    "global marketing", "emea marketing"
]

TARGET_LOCATIONS = [
    "switzerland", "denmark", "sweden", "zurich", "geneva", "copenhagen", "stockholm", "malmö", "lund"
]

TARGET_INDUSTRIES = [
    "medical", "medtech", "healthcare", "diabetes", "device", "biotech", "health", "pharma"
]

def score_job(title, description="", location=""):
    """Score job match 0-10"""
    score = 0
    text = f"{title} {description} {location}".lower()
    
    # Keywords (highest priority)
    keyword_matches = sum(1 for kw in TARGET_KEYWORDS if kw in text)
    score += min(keyword_matches * 2, 8)  # Max 8 points from keywords
    
    # Location
    for loc in TARGET_LOCATIONS:
        if loc in text:
            score += 1
            break
    
    # Industry
    for ind in TARGET_INDUSTRIES:
        if ind in text:
            score += 1
            break
    
    return min(score, 10)

def scrape_company_playwright(company_name, url):
    """Scrape company careers page using Playwright"""
    jobs = []
    
    print(f"  {company_name}... ", end="", flush=True)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(15000)
            
            # Navigate to careers page
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(2)  # Wait for JS rendering
            
            # Look for job listings (common selectors)
            selectors = [
                'a[href*="job"]',
                'div[class*="job"]',
                'div[class*="position"]',
                'div[class*="vacancy"]',
                'li[class*="posting"]',
            ]
            
            for selector in selectors:
                try:
                    job_elements = page.query_selector_all(selector)
                    
                    for elem in job_elements[:30]:  # Check first 30
                        try:
                            title_text = elem.text_content().strip()
                            
                            if not title_text or len(title_text) < 5:
                                continue
                            
                            # Get location if available
                            location_elem = elem.query_selector('[class*="location"], [class*="place"]')
                            location = location_elem.text_content() if location_elem else ""
                            
                            score = score_job(title_text, "", location)
                            
                            if score >= 6:
                                # Get link if available
                                link_elem = elem.query_selector('a')
                                link = link_elem.get_attribute('href') if link_elem else url
                                if link and not link.startswith('http'):
                                    link = url.rstrip('/') + link
                                
                                jobs.append({
                                    'company': company_name,
                                    'title': title_text[:150],
                                    'location': location[:100],
                                    'url': link,
                                    'score': score,
                                    'found_at': datetime.now().isoformat()
                                })
                        except:
                            continue
                    
                    if jobs:
                        break
                except:
                    continue
            
            browser.close()
        
        if jobs:
            print(f"✅ Found {len(jobs)}")
        else:
            print("⏳ No matches")
        
        return jobs
        
    except PlaywrightTimeout:
        print("⏱️ Timeout")
        return []
    except Exception as e:
        print(f"❌ Error: {str(e)[:40]}")
        return []

def main():
    print(f"\n🔍 CAREER AGENT - PLAYWRIGHT CRAWLER ({datetime.now().strftime('%A, %d %b %Y')})\n")
    
    all_jobs = []
    
    # Crawl each company
    for company, url in COMPANIES.items():
        jobs = scrape_company_playwright(company, url)
        all_jobs.extend(jobs)
        time.sleep(1)  # Polite delay between requests
    
    # Remove duplicates
    unique_jobs = {}
    for job in all_jobs:
        key = f"{job['title']}_{job['company']}"
        if key not in unique_jobs or job['score'] > unique_jobs[key]['score']:
            unique_jobs[key] = job
    
    all_jobs = list(unique_jobs.values())
    all_jobs.sort(key=lambda x: x['score'], reverse=True)
    
    # Save all results
    os.makedirs("agents/career-agent/data", exist_ok=True)
    output_file = f"agents/career-agent/data/jobs-{datetime.now().strftime('%Y-%m-%d')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(all_jobs, f, indent=2)
    
    print(f"\n✅ Scan complete: {len(all_jobs)} jobs found")
    print(f"📁 Saved to: {output_file}")
    
    # Show top 10
    if all_jobs:
        print(f"\n🏆 TOP 10 MATCHES:\n")
        for i, job in enumerate(all_jobs[:10], 1):
            print(f"{i}. 🎯 Score: {job['score']}/10")
            print(f"   **{job['title']}**")
            print(f"   🏢 {job['company']}")
            if job['location']:
                print(f"   📍 {job['location']}")
            print()
    else:
        print("\n❌ No jobs found matching criteria")
    
    return all_jobs[:10]

if __name__ == "__main__":
    main()
