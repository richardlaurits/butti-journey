#!/usr/bin/env python3
"""
Career Agent: Enhanced Job Crawler - V2 (Improved Selectors)
✅ Better job element detection
✅ Fallback selectors for different site structures
✅ Debug output to diagnose issues
✅ Lower initial threshold for testing
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import json
import os
from datetime import datetime
from pathlib import Path
import time
import re
from urllib.parse import urljoin

# Ensure output directories exist
Path("./job_screenshots").mkdir(exist_ok=True)
Path("./job_results").mkdir(exist_ok=True)

# Target companies with careers URLs
COMPANIES = {
    # Denmark
    "Novo Nordisk": "https://careers.novonordisk.com/",
    # Switzerland
    "Roche": "https://careers.roche.com/global/en",
}

# Richard's search criteria
TARGET_KEYWORDS = {
    "roles": [
        "director", "senior manager", "vp", "vice president", "chief", "head of",
        "business development", "corporate development", "product strategy",
        "go-to-market", "commercial", "strategic partnerships",
        "global marketing", "emea marketing", "general manager", "gm", "managing director"
    ],
    "industries": [
        "medical", "medtech", "healthcare", "diabetes", "device", "biotech", "health", "pharma"
    ],
}

TARGET_LOCATIONS = {
    "Switzerland": ["switzerland", "zurich", "geneva", "basel", "bern", "ch", "zug"],
    "Denmark": ["denmark", "copenhagen", "aarhus", "dk"],
    "Sweden": ["sweden", "stockholm", "gothenburg", "malmö", "lund", "se"],
}

def accept_cookies(page):
    """Try to accept cookies using common button selectors"""
    cookie_selectors = [
        'button:has-text("Accept")',
        'button:has-text("Accept All")',
        'button:has-text("Accept cookies")',
        'button:has-text("Accepter")',
        'button:has-text("Acceptera")',
        '[data-testid="cookie-accept"]',
        '.cookie-accept',
        '#cookie-accept',
        'button[aria-label*="Accept"]',
    ]
    
    for selector in cookie_selectors:
        try:
            button = page.query_selector(selector)
            if button:
                button.click()
                print(f"    ✓ Cookies accepted")
                time.sleep(1)
                return True
        except:
            pass
    return False

def wait_for_page_load(page, timeout=15000):
    """Wait for page to fully load"""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
        time.sleep(2)
        return True
    except PlaywrightTimeout:
        print(f"    ⚠ Page load timeout, proceeding anyway")
        time.sleep(2)
        return False

def score_job(title, description="", location=""):
    """Score job match 0-10"""
    score = 0
    text = f"{title} {description} {location}".lower()
    
    # Keywords (role + industry)
    keyword_matches = 0
    for kw in TARGET_KEYWORDS["roles"]:
        if kw in text:
            keyword_matches += 1
    
    for kw in TARGET_KEYWORDS["industries"]:
        if kw in text:
            keyword_matches += 1
    
    score += min(keyword_matches * 1.5, 6)  # Max 6 points from keywords
    
    # Location (bonus points)
    for country, locs in TARGET_LOCATIONS.items():
        for loc in locs:
            if loc in text:
                score += 2
                break
    
    return min(int(score), 10)

def find_job_elements(page):
    """Find job listings with multiple fallback selectors"""
    job_selectors = [
        "[data-testid*='job']",
        "[data-qa*='job']",
        ".job-card",
        ".job-listing",
        ".job-item",
        ".job-row",
        ".vacancy-card",
        ".position",
        ".opening",
        ".job",
        "li[data-testid*='job']",
        "li[data-qa*='job']",
        "li.job",
        "article.job",
        "article[data-testid*='job']",
        "div[role='link']",
        ".search-result-item",
        ".result-item",
    ]
    
    for selector in job_selectors:
        try:
            elements = page.query_selector_all(selector)
            # Only use if we find multiple job elements (3+)
            if elements and len(elements) >= 3:
                print(f"    ✓ Found {len(elements)} job elements using: {selector}")
                return elements, selector
        except:
            pass
    
    # If no specific selectors worked, try broader approach
    print(f"    ! Trying generic approach...")
    try:
        # Look for common job listing containers
        containers = page.query_selector_all("div, section, article, li")
        # Filter for ones that likely contain job listings
        job_like = []
        for elem in containers:
            try:
                text = elem.inner_text()
                # If it contains location/job keywords, might be a listing
                if any(kw in text.lower() for kw in ["director", "manager", "engineer", "location", "apply"]):
                    job_like.append(elem)
            except:
                pass
        
        if job_like:
            print(f"    ✓ Found {len(job_like)} potential job elements (generic)")
            return job_like[:20], "generic"
    except:
        pass
    
    return [], None

def extract_job_details(job_element, company_name):
    """Extract job details from element"""
    try:
        # Try to get title
        title_elem = job_element.query_selector("a, h2, h3, h4, [data-testid*='title'], [data-qa*='title']")
        title = title_elem.inner_text() if title_elem else "Unknown Title"
        
        # Try to get location
        location_elem = job_element.query_selector(
            "[data-testid*='location'], [data-qa*='location'], .location, .job-location, "
            "span:has-text('location'), .city, .region"
        )
        location = location_elem.inner_text() if location_elem else "Location not listed"
        
        # Try to get description
        description_elem = job_element.query_selector(
            "[data-testid*='description'], [data-qa*='description'], .description, p, [data-qa*='summary']"
        )
        description = description_elem.inner_text() if description_elem else ""
        
        # If no description, use inner text up to 200 chars
        if not description:
            description = job_element.inner_text()[:200]
        
        # Try to get link
        link_elem = job_element.query_selector("a")
        link = link_elem.get_attribute("href") if link_elem else None
        
        # Get full text for backup
        full_text = job_element.inner_text()[:500]
        
        return {
            "title": title.strip(),
            "location": location.strip(),
            "description": description[:200].strip(),
            "full_text": full_text,
            "link": link,
        }
    except Exception as e:
        return None

def scrape_company(company_name, url):
    """Scrape company careers page"""
    jobs = []
    screenshots_taken = []
    
    print(f"\n📄 {company_name}")
    print(f"   URL: {url}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(20000)
            
            # Navigate
            print(f"   ⏳ Loading...", end="", flush=True)
            page.goto(url, wait_until="domcontentloaded")
            print(f" ✓")
            
            # Accept cookies
            print(f"   🍪 Checking cookies...", end="", flush=True)
            accept_cookies(page)
            
            # Wait for load
            print(f"   ⏱ Waiting for page...", end="", flush=True)
            wait_for_page_load(page)
            print(f" ✓")
            
            # Find job elements
            print(f"   🔍 Finding jobs...", end="", flush=True)
            job_elements, selector_used = find_job_elements(page)
            
            if not job_elements:
                print(f" (none found)")
                # Save page content for debugging
                page_content = page.content()
                with open(f"./job_results/{company_name.replace(' ', '_')}_page.html", "w") as f:
                    f.write(page_content)
                print(f"   💾 Page saved to: {company_name.replace(' ', '_')}_page.html for inspection")
            else:
                print(f" ✓")
                
                # Process jobs
                print(f"   📋 Processing {len(job_elements)} jobs...")
                for idx, job_elem in enumerate(job_elements):
                    try:
                        details = extract_job_details(job_elem, company_name)
                        if not details:
                            continue
                        
                        # Score the job
                        score = score_job(details["title"], details["description"], details["location"])
                        
                        # Show all jobs, not just high-scoring (for testing)
                        if score >= 0:  # Temporary: show all
                            if score >= 5:
                                print(f"      ✓ [{score}/10] {details['title']}")
                            else:
                                print(f"      [{score}/10] {details['title'][:50]}")
                            
                            # Screenshot high-scoring jobs
                            if score >= 5:
                                try:
                                    job_elem.scroll_into_view_if_needed()
                                    time.sleep(0.3)
                                    screenshot_path = f"./job_screenshots/{company_name.replace(' ', '_')}_{idx}_{score}.png"
                                    job_elem.screenshot(path=screenshot_path)
                                    screenshots_taken.append(screenshot_path)
                                except:
                                    pass
                            
                            jobs.append({
                                "company": company_name,
                                "title": details["title"],
                                "location": details["location"],
                                "description": details["description"],
                                "link": details["link"],
                                "score": score,
                                "screenshot": screenshot_path if score >= 5 else None,
                            })
                    except Exception as e:
                        pass
            
            browser.close()
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
    
    return jobs, screenshots_taken

def main():
    """Main crawler process"""
    print("\n" + "="*70)
    print("🚀 CAREER AGENT - ENHANCED JOB CRAWLER v2")
    print("="*70)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Scanning: {len(COMPANIES)} companies")
    print(f"🗺 Countries: Switzerland, Denmark, Sweden")
    print(f"💼 Roles: Director, VP, Business Dev, General Manager, etc.")
    print("="*70)
    
    all_jobs = []
    all_screenshots = []
    start_time = time.time()
    
    for company_name, url in COMPANIES.items():
        jobs, screenshots = scrape_company(company_name, url)
        all_jobs.extend(jobs)
        all_screenshots.extend(screenshots)
        time.sleep(1)
    
    elapsed = time.time() - start_time
    
    # Save results
    results = {
        "scan_date": datetime.now().isoformat(),
        "scan_duration_seconds": int(elapsed),
        "companies_scanned": len(COMPANIES),
        "total_jobs_found": len(all_jobs),
        "high_scoring_jobs": len([j for j in all_jobs if j["score"] >= 5]),
        "screenshots_taken": len(all_screenshots),
        "jobs": all_jobs,
    }
    
    results_file = f"./job_results/jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"⏱ Scan took: {int(elapsed)}s")
    print(f"📍 Jobs found (all): {len(all_jobs)}")
    print(f"🎯 Jobs found (score ≥5): {results['high_scoring_jobs']}")
    print(f"📸 Screenshots saved: {len(all_screenshots)}")
    print(f"💾 Results saved: {results_file}")
    
    if all_jobs:
        print(f"\n🏆 TOP MATCHES:")
        for job in sorted(all_jobs, key=lambda x: x["score"], reverse=True)[:5]:
            print(f"   [{job['score']}/10] {job['company']} - {job['title']}")
            print(f"           {job['location']}")
            if job.get('link'):
                print(f"           🔗 {job['link']}")
    
    print("\n" + "="*70)
    print(f"✅ Done! Results and screenshots ready in ./job_results/ and ./job_screenshots/")
    print("="*70 + "\n")
    
    return results

if __name__ == "__main__":
    results = main()
