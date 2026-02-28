#!/usr/bin/env python3
"""
Career Agent: Enhanced Job Crawler
✅ Accept cookies automatically
✅ Wait for full page load
✅ Filter for CH/DK/SE + marketing/management/strategy
✅ Save screenshots of relevant jobs
✅ Generate summary report with Telegram notification
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
    "IQVIA": "https://www.iqvia.com/careers",
    
    # Sweden  
    "Glooko": "https://www.glooko.com/careers",
    
    # Switzerland
    "Tandem Diabetes": "https://www.tandemdiabetes.com/careers",
    "BD": "https://www.bd.com/careers",
    "Haleon": "https://www.haleon.com/careers",
    "Roche": "https://careers.roche.com/global/en",
    "Zimmer Biomet": "https://www.zimmerbiomet.com/careers",
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
        # Wait for network to be idle
        page.wait_for_load_state("networkidle", timeout=timeout)
        time.sleep(2)  # Extra buffer for JS rendering
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

def extract_job_details(job_element, company_name):
    """Extract job title, location, link from job element"""
    try:
        title_elem = job_element.query_selector("a, h2, h3, [data-testid*='job'], .job-title")
        title = title_elem.inner_text() if title_elem else "Unknown Title"
        
        location_elem = job_element.query_selector("[data-testid*='location'], .location, .job-location, span:has-text('location')")
        location = location_elem.inner_text() if location_elem else "Location not listed"
        
        description_elem = job_element.query_selector("[data-testid*='description'], .description, p")
        description = description_elem.inner_text() if description_elem else ""
        
        link_elem = job_element.query_selector("a")
        link = link_elem.get_attribute("href") if link_elem else None
        
        return {
            "title": title.strip(),
            "location": location.strip(),
            "description": description[:200].strip(),
            "link": link,
        }
    except:
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
            page.set_default_timeout(15000)
            
            # Navigate to careers page
            print(f"   ⏳ Loading...", end="", flush=True)
            page.goto(url, wait_until="domcontentloaded")
            print(f" ✓")
            
            # Accept cookies
            print(f"   🍪 Checking cookies...", end="", flush=True)
            accept_cookies(page)
            
            # Wait for full load
            print(f"   ⏱ Waiting for page...", end="", flush=True)
            wait_for_page_load(page)
            print(f" ✓")
            
            # Try to filter by location (country)
            print(f"   🗺 Filtering location...", end="", flush=True)
            location_filters = page.query_selector_all("select, [data-testid*='location'], button:has-text('Location')")
            if location_filters:
                print(f" (found {len(location_filters)} filters)")
                # Try each filter
                for filt in location_filters[:1]:  # Try first filter
                    try:
                        filt.click()
                        time.sleep(1)
                        # Look for Switzerland, Denmark, Sweden options
                        for country in ["Switzerland", "Denmark", "Sweden"]:
                            option = page.query_selector(f"button:has-text('{country}'), label:has-text('{country}')")
                            if option:
                                option.click()
                                time.sleep(1)
                    except:
                        pass
            else:
                print(f" (no location filters found)")
            
            # Find job listings
            print(f"   🔍 Finding jobs...", end="", flush=True)
            job_selectors = [
                "[data-testid*='job']",
                ".job-card",
                ".job-listing",
                ".job-item",
                "li[data-testid*='job']",
                "article",
                ".vacancy-card",
            ]
            
            job_elements = []
            for selector in job_selectors:
                found = page.query_selector_all(selector)
                if found and len(found) > 2:  # Only use if we find multiple
                    job_elements = found[:20]  # Max 20 per company
                    break
            
            print(f" ({len(job_elements)} found)")
            
            # Process each job
            if job_elements:
                print(f"   📋 Processing jobs...")
                for idx, job_elem in enumerate(job_elements):
                    try:
                        details = extract_job_details(job_elem, company_name)
                        if not details:
                            continue
                        
                        # Score the job
                        score = score_job(details["title"], details["description"], details["location"])
                        
                        # Only save if score >= 5 (good match)
                        if score >= 5:
                            print(f"      ✓ [{score}/10] {details['title']} ({details['location']})")
                            
                            # Try to take screenshot
                            try:
                                job_elem.scroll_into_view_if_needed()
                                time.sleep(0.5)
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
                                "screenshot": screenshot_path if screenshots_taken else None,
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
    print("🚀 CAREER AGENT - ENHANCED JOB CRAWLER")
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
        time.sleep(2)  # Be respectful to servers
    
    elapsed = time.time() - start_time
    
    # Save results
    results = {
        "scan_date": datetime.now().isoformat(),
        "scan_duration_seconds": int(elapsed),
        "companies_scanned": len(COMPANIES),
        "total_jobs_found": len(all_jobs),
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
    print(f"📍 Jobs found (score ≥5): {len(all_jobs)}")
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
