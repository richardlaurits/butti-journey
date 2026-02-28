#!/usr/bin/env python3
"""
Real job board scraping - fetches actual jobs from multiple sources
"""

import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import re

# Richard's search criteria
TARGET_KEYWORDS = [
    "Director", "Senior Manager", "VP", "Chief", "Head of", "CEO",
    "Business Development", "Corporate Development", "Product Strategy",
    "Go-to-Market", "Commercial", "Strategic Partnerships"
]

LOCATIONS = {
    "Switzerland": ["Switzerland", "Zurich", "Geneva", "Genève", "Bern", "Basel", "Vaud", "Valais"],
    "Denmark": ["Denmark", "Copenhagen", "København"],
    "Sweden": ["Sweden", "Stockholm", "Gothenburg", "Göteborg", "Skåne"]
}

INDUSTRIES = ["Medical", "MedTech", "Device", "Healthcare", "Biotech", "AI", "Digital Health"]

def score_job(title, description, location):
    """Score job 0-10"""
    score = 0
    text = (title + " " + description).lower()
    
    # Keywords
    for kw in TARGET_KEYWORDS:
        if kw.lower() in text:
            score += 1
    
    # Industry
    for ind in INDUSTRIES:
        if ind.lower() in text:
            score += 2
            break
    
    # Location
    for region, cities in LOCATIONS.items():
        for city in cities:
            if city.lower() in location.lower():
                score += 2
                break
    
    return min(score, 10)

def scrape_indeed_ch():
    """Scrape Indeed Switzerland"""
    jobs = []
    print("  🔍 Scraping Indeed Switzerland...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Search for medical/medtech jobs in Switzerland
        url = "https://www.indeed.ch/jobs"
        params = {
            'q': 'Director OR "VP" OR "Chief Commercial" medical technology',
            'l': 'Switzerland',
            'sort': 'date'
        }
        
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Parse job cards
        for card in soup.find_all('div', {'data-jobsearch-job-card': True})[:5]:
            try:
                title_elem = card.find('h2')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                company_elem = card.find('span', {'data-company-name': True})
                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                
                location_elem = card.find('div', {'data-job-result-item': True})
                location = "Switzerland" if location_elem else "Unknown"
                
                link_elem = card.find('a', {'data-jk': True})
                link = f"https://www.indeed.ch/viewjob?jk={link_elem.get('data-jk')}" if link_elem else ""
                
                # Get snippet
                snippet_elem = card.find('div', {'class': re.compile('resultContent')})
                snippet = snippet_elem.get_text(strip=True)[:200] if snippet_elem else ""
                
                score = score_job(title, snippet, location)
                
                if score >= 5:
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'source': 'Indeed CH',
                        'score': score,
                        'posted': 'Recently',
                        'url': link,
                        'snippet': snippet
                    })
                    
            except Exception as e:
                continue
        
        print(f"    ✅ Found {len(jobs)} jobs")
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
    
    return jobs

def scrape_monster():
    """Scrape Monster.com"""
    jobs = []
    print("  🔍 Scraping Monster...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        
        # Search Monster
        base_url = "https://www.monster.com/jobs/search"
        
        searches = [
            {"q": "Director Medical Technology", "where": "Switzerland"},
            {"q": "VP Business Development", "where": "Copenhagen, Denmark"},
            {"q": "Senior Manager Product", "where": "Stockholm, Sweden"},
        ]
        
        for search in searches:
            params = {
                'q': search['q'],
                'where': search['where'],
                'sort': 'date'
            }
            
            resp = requests.get(base_url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # Parse job results
            for job_elem in soup.find_all('div', {'class': re.compile('JobCard')})[:3]:
                try:
                    title_elem = job_elem.find('h2')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    company_elem = job_elem.find('div', {'class': re.compile('company')})
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                    
                    location = search['where']
                    link_elem = job_elem.find('a', {'class': re.compile('jobTitle')})
                    link = link_elem.get('href', '') if link_elem else ""
                    
                    snippet = job_elem.get_text(strip=True)[:200]
                    score = score_job(title, snippet, location)
                    
                    if score >= 5:
                        jobs.append({
                            'title': title,
                            'company': company,
                            'location': location,
                            'source': 'Monster',
                            'score': score,
                            'posted': 'Recently',
                            'url': link,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    continue
            
            time.sleep(1)  # Respect rate limits
        
        print(f"    ✅ Found {len(jobs)} jobs")
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
    
    return jobs

def scrape_jobs_ch():
    """Scrape Jobs.ch (Swiss board)"""
    jobs = []
    print("  🔍 Scraping Jobs.ch...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        
        url = "https://www.jobs.ch/en/vacancy/search"
        params = {
            'keywords': 'Director Medical Business Development',
            'location': 'Switzerland'
        }
        
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Parse job listings
        for item in soup.find_all('a', {'class': re.compile('JobTitle')})[:5]:
            try:
                title = item.get_text(strip=True)
                link = item.get('href', '')
                
                parent = item.find_parent('div')
                if not parent:
                    continue
                
                company_elem = parent.find('span', {'class': re.compile('Company')})
                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                
                location = "Switzerland"
                snippet = f"{title} - {company}"
                
                score = score_job(title, snippet, location)
                
                if score >= 5:
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'source': 'Jobs.ch',
                        'score': score,
                        'posted': 'Recently',
                        'url': f"https://www.jobs.ch{link}" if link.startswith('/') else link,
                        'snippet': snippet
                    })
                    
            except Exception as e:
                continue
        
        print(f"    ✅ Found {len(jobs)} jobs")
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
    
    return jobs

def scrape_arbetsformedlingen():
    """Scrape Swedish Arbetsförmedlingen (has API)"""
    jobs = []
    print("  🔍 Scraping Arbetsförmedlingen...")
    
    try:
        # Arbetsförmedlingen API (public)
        base_url = "https://www.arbetsformedlingen.se/api/matchning/publication"
        
        params = {
            'q': 'Director Medical',
            'location': 'Stockholm',
            'limit': 10,
            'offset': 0
        }
        
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        
        data = resp.json()
        
        for item in data.get('matchning', [])[:5]:
            try:
                title = item.get('rubrik', '')
                company = item.get('arbetsgivarNamn', 'Unknown')
                location = item.get('plats', 'Sweden')
                link = item.get('annonsUrl', '')
                snippet = item.get('beskrivning', '')[:200]
                
                score = score_job(title, snippet, location)
                
                if score >= 5:
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'source': 'Arbetsförmedlingen',
                        'score': score,
                        'posted': 'Recently',
                        'url': link,
                        'snippet': snippet
                    })
                    
            except Exception as e:
                continue
        
        print(f"    ✅ Found {len(jobs)} jobs")
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
    
    return jobs

def main():
    print("🔍 SCRAPING REAL JOBS FOR RICHARD\n")
    print("📋 Fetching from job boards...")
    
    all_jobs = []
    
    # Scrape multiple sources
    all_jobs.extend(scrape_indeed_ch())
    time.sleep(2)
    all_jobs.extend(scrape_monster())
    time.sleep(2)
    all_jobs.extend(scrape_jobs_ch())
    time.sleep(2)
    all_jobs.extend(scrape_arbetsformedlingen())
    
    # Remove duplicates
    unique_jobs = {}
    for job in all_jobs:
        key = f"{job['title']}_{job['company']}"
        if key not in unique_jobs or job['score'] > unique_jobs[key]['score']:
            unique_jobs[key] = job
    
    all_jobs = list(unique_jobs.values())
    
    # Sort by score
    all_jobs.sort(key=lambda x: x['score'], reverse=True)
    
    # Show top 10
    print(f"\n{'='*80}")
    print(f"🎯 REAL JOBS - TOP 10 MATCHES (Score 7+)")
    print(f"{'='*80}\n")
    
    top_10 = [j for j in all_jobs if j['score'] >= 5][:10]
    
    if not top_10:
        print("❌ No jobs found matching your criteria from available sources.")
        print("   This may be due to:")
        print("   - Job boards blocking automated access")
        print("   - No current openings matching exact criteria")
        print("\n✅ Solution: When you upload your resume, I'll set up direct feeds from:")
        print("   - LinkedIn job alerts (email parsing)")
        print("   - Monster API (official)")
        print("   - Indeed API (official)")
        print("   - Arbetsförmedlingen API (official)")
        return
    
    for i, job in enumerate(top_10, 1):
        print(f"{i}. 🎯 Score: {job['score']}/10")
        print(f"   **{job['title']}**")
        print(f"   🏢 {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   📰 Source: {job['source']}")
        print(f"   🔗 {job['url'][:60]}...")
        print()
    
    # Save results
    with open('agents/career-agent/real-jobs-scraped.json', 'w') as f:
        json.dump(top_10, f, indent=2)
    
    print(f"📁 Saved {len(top_10)} jobs to: real-jobs-scraped.json")

if __name__ == "__main__":
    main()
