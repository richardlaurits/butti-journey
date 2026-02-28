#!/usr/bin/env python3
"""
Career Agent: Daily Company Job Board Crawler
Checks target companies' careers pages for matching roles
Runs Mon-Fri, 8 AM CET
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from pathlib import Path

# Target companies with careers page URLs
COMPANIES = {
    # Denmark
    "Novo Nordisk": "https://www.novonordisk.com/careers",
    "Dawn Health": "https://www.dawnhealth.eu",
    "IQVIA": "https://www.iqvia.com/careers",
    "CapGemini": "https://www.capgemini.com/careers",
    
    # Sweden
    "Glooko": "https://www.glooko.com/careers",
    "Medicon Village": "https://mediconvillage.se",
    "Minc": "https://minc.se",
    "Lund University Innovation": "https://www.lunduniversity.lu.se/innovation",
    
    # Switzerland
    "Tandem Diabetes Care": "https://www.tandemdiabetes.com/careers",
    "BD (Becton Dickinson)": "https://www.bd.com/careers",
    "Haleon": "https://www.haleon.com/careers",
    "Roche": "https://www.roche.com/careers",
    "MyLife": "https://www.mylife.com/careers",
    "embecta": "https://www.embecta.com/careers",
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
    "medical", "medtech", "healthcare", "diabetes", "device", "biotech", "health tech", "ai"
]

def score_job(title, description, location):
    """Score job match 0-10"""
    score = 0
    text = f"{title} {description} {location}".lower()
    
    # Keywords
    for kw in TARGET_KEYWORDS:
        if kw in text:
            score += 2
    
    # Location
    for loc in TARGET_LOCATIONS:
        if loc in text:
            score += 2
            break
    
    # Industry
    for ind in TARGET_INDUSTRIES:
        if ind in text:
            score += 1
            break
    
    return min(score, 10)

def scrape_company(company_name, url):
    """Scrape company careers page"""
    jobs = []
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Look for job listings (varies by company)
        job_elements = soup.find_all(['a', 'div'], {'class': ['job', 'position', 'listing', 'vacancy']})
        
        for elem in job_elements[:20]:  # Check first 20
            title_elem = elem.find(['h2', 'h3', 'h4', 'span'])
            if title_elem:
                title = title_elem.get_text(strip=True)
                location = elem.get_text(strip=True)[:100]
                
                score = score_job(title, "", location)
                
                if score >= 5:
                    jobs.append({
                        'company': company_name,
                        'title': title,
                        'location': location,
                        'url': url,
                        'score': score,
                        'found_at': datetime.now().isoformat()
                    })
        
        return jobs
        
    except Exception as e:
        print(f"❌ {company_name}: {e}")
        return []

def main():
    print(f"\n🔍 CAREER AGENT - DAILY CRAWLER ({datetime.now().strftime('%A, %d %b %Y')})\n")
    
    all_jobs = []
    
    # Crawl each company
    for company, url in COMPANIES.items():
        print(f"  Checking {company}...", end=" ")
        jobs = scrape_company(company, url)
        
        if jobs:
            print(f"✅ Found {len(jobs)} matches")
            all_jobs.extend(jobs)
        else:
            print("⏳ No matches")
    
    # Sort by score
    all_jobs.sort(key=lambda x: x['score'], reverse=True)
    
    # Save results
    os.makedirs("agents/career-agent/data", exist_ok=True)
    output_file = f"agents/career-agent/data/jobs-{datetime.now().strftime('%Y-%m-%d')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(all_jobs[:20], f, indent=2)
    
    print(f"\n✅ Scan complete: {len(all_jobs)} jobs found")
    print(f"📁 Saved to: {output_file}")
    
    # Show top results
    if all_jobs:
        print(f"\n🏆 TOP 5 MATCHES:\n")
        for i, job in enumerate(all_jobs[:5], 1):
            print(f"{i}. {job['title']}")
            print(f"   🏢 {job['company']} | Score: {job['score']}/10\n")
    
    return all_jobs

if __name__ == "__main__":
    main()
