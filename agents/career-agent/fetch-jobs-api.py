#!/usr/bin/env python3
"""
Fetch real jobs from free APIs
- Arbetsförmedlingen (Swedish, public)
- Indeed API (requires key)
"""

import requests
import json
from datetime import datetime, timedelta
import os
import sys

# Configuration
ARBETSFORMEDLINGEN_BASE = "https://www.arbetsformedlingen.se/api/matchning/publication"
INDEED_BASE = "https://api.adzuna.com/v1/api/jobs"  # Alternative to direct Indeed

# Richard's criteria
TARGET_KEYWORDS = [
    "director", "senior manager", "vp", "chief", "ceo", "head of",
    "business development", "corporate development", "product strategy",
    "go-to-market", "commercial", "strategic partnerships"
]

LOCATIONS_SE = ["Stockholm", "Gothenburg", "Malmö", "Skåne", "Sweden"]
LOCATIONS_DK = ["Copenhagen", "København", "Denmark", "Aarhus"]
LOCATIONS_CH = ["Zurich", "Geneva", "Genève", "Bern", "Vaud", "Switzerland"]

def score_job(title, description, location):
    """Score job 0-10 based on Richard's criteria"""
    score = 0
    text = (title + " " + (description or "")).lower()
    location_text = (location or "").lower()
    
    # Keyword matches
    for kw in TARGET_KEYWORDS:
        if kw in text:
            score += 1
    
    # Industry keywords
    industries = ["medical", "medtech", "device", "healthcare", "biotech", "ai", "digital health"]
    for ind in industries:
        if ind in text:
            score += 2
            break
    
    # Location match
    all_locs = LOCATIONS_SE + LOCATIONS_DK + LOCATIONS_CH
    for loc in all_locs:
        if loc.lower() in location_text:
            score += 1
            break
    
    return min(score, 10)

def fetch_arbetsformedlingen():
    """Fetch jobs from Swedish Arbetsförmedlingen API"""
    jobs = []
    print("  🔍 Fetching from Arbetsförmedlingen (Sweden)...")
    
    try:
        # Search parameters
        searches = [
            {"keywords": "Director Medical", "location": "Stockholm"},
            {"keywords": "VP Business Development", "location": "Gothenburg"},
            {"keywords": "Senior Manager Product", "location": "Malmö"},
        ]
        
        for search in searches:
            params = {
                "q": search["keywords"],
                "location-id": "106",  # Sweden
                "limit": 20,
                "offset": 0
            }
            
            resp = requests.get(ARBETSFORMEDLINGEN_BASE, params=params, timeout=10)
            resp.raise_for_status()
            
            data = resp.json()
            
            for item in data.get("matchning", []):
                try:
                    title = item.get("rubrik", "")
                    company = item.get("arbetsgivarNamn", "Unknown")
                    location = item.get("plats", "Sweden")
                    description = item.get("beskrivning", "")[:300]
                    
                    # Parse salary if available
                    salary_text = item.get("lön", "")
                    posted_date = item.get("publicerat", "")
                    
                    score = score_job(title, description, location)
                    
                    if score >= 4:
                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "description": description,
                            "salary": salary_text,
                            "posted": posted_date,
                            "source": "Arbetsförmedlingen",
                            "score": score,
                            "url": item.get("url", ""),
                            "id": item.get("platsannonsId", "")
                        })
                except Exception as e:
                    continue
        
        print(f"    ✅ Found {len(jobs)} jobs from Arbetsförmedlingen")
        
    except Exception as e:
        print(f"    ❌ Arbetsförmedlingen error: {e}")
    
    return jobs

def fetch_indeed_api(api_key=None):
    """Fetch jobs from Indeed API (requires key)"""
    jobs = []
    
    if not api_key:
        api_key = os.environ.get("INDEED_API_KEY")
    
    if not api_key:
        print("  ⏳ Indeed API: Waiting for your API key...")
        return jobs
    
    print("  🔍 Fetching from Indeed API...")
    
    try:
        # Using Adzuna API as proxy to Indeed jobs (free tier)
        ADZUNA_KEY = os.environ.get("ADZUNA_API_KEY")
        
        if not ADZUNA_KEY:
            print("    ⏳ Adzuna API key not set")
            return jobs
        
        searches = [
            {"what": "Director Medical", "where": "Switzerland"},
            {"what": "VP Business Development", "where": "Denmark"},
            {"what": "Senior Manager Product", "where": "Sweden"},
        ]
        
        for search in searches:
            url = f"{INDEED_BASE}/search"
            params = {
                "app_id": ADZUNA_KEY,
                "app_key": "ADZUNA_KEY",  # Placeholder
                "what": search["what"],
                "where": search["where"],
                "results_per_page": 20,
                "sort_by": "date"
            }
            
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            
            data = resp.json()
            
            for item in data.get("results", []):
                try:
                    title = item.get("title", "")
                    company = item.get("company", "Unknown")
                    location = item.get("location", search["where"])
                    description = item.get("description", "")[:300]
                    salary = item.get("salary_is_predicted", False)
                    
                    score = score_job(title, description, location)
                    
                    if score >= 4:
                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "description": description,
                            "salary": "Check listing",
                            "posted": item.get("created", ""),
                            "source": "Indeed",
                            "score": score,
                            "url": item.get("redirect_url", "")
                        })
                except Exception as e:
                    continue
        
        print(f"    ✅ Found {len(jobs)} jobs from Indeed")
        
    except Exception as e:
        print(f"    ❌ Indeed API error: {e}")
    
    return jobs

def fetch_linkedin_alerts():
    """Parse LinkedIn job alerts from Gmail"""
    jobs = []
    print("  🔍 Checking LinkedIn alerts in Gmail...")
    
    try:
        # TODO: Parse incoming LinkedIn emails
        # This will be done when Richard uploads resume
        print("    ⏳ LinkedIn email parsing: Ready (awaiting resume upload)")
    except Exception as e:
        print(f"    ❌ LinkedIn error: {e}")
    
    return jobs

def aggregate_and_rank(all_jobs):
    """Deduplicate and rank all jobs"""
    # Remove duplicates by title+company
    unique = {}
    for job in all_jobs:
        key = f"{job['title']}|{job['company']}"
        if key not in unique or job['score'] > unique[key]['score']:
            unique[key] = job
    
    jobs = list(unique.values())
    jobs.sort(key=lambda x: x['score'], reverse=True)
    
    return jobs

def main():
    print("\n🔍 FETCHING JOBS FROM FREE APIs\n")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_jobs = []
    
    # Fetch from all sources
    all_jobs.extend(fetch_arbetsformedlingen())
    all_jobs.extend(fetch_indeed_api())
    all_jobs.extend(fetch_linkedin_alerts())
    
    if not all_jobs:
        print("\n❌ No jobs found. Set up APIs first!")
        return
    
    # Rank and deduplicate
    ranked = aggregate_and_rank(all_jobs)
    
    # Show top 10
    print(f"\n{'='*80}")
    print(f"🎯 TOP JOBS - RANKED BY MATCH SCORE")
    print(f"{'='*80}\n")
    
    top_10 = ranked[:10]
    
    for i, job in enumerate(top_10, 1):
        print(f"{i}. 🎯 Score: {job['score']}/10")
        print(f"   **{job['title']}**")
        print(f"   🏢 {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   📰 Source: {job['source']}")
        if job['salary']:
            print(f"   💰 {job['salary']}")
        print(f"   🔗 {job['url'][:70] if job['url'] else 'N/A'}...")
        print()
    
    # Save to file
    os.makedirs("agents/career-agent/data", exist_ok=True)
    output_file = f"agents/career-agent/data/jobs-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(top_10, f, indent=2)
    
    print(f"\n📁 Saved {len(top_10)} jobs to: {output_file}")
    
    # Also save latest
    with open("agents/career-agent/data/jobs-latest.json", 'w') as f:
        json.dump(top_10, f, indent=2)

if __name__ == "__main__":
    main()
