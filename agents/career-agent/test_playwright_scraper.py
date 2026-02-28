#!/usr/bin/env python3
"""
Career Agent - Playwright Job Scraper
Tests specific companies with browser automation
"""

import json
from datetime import datetime
from pathlib import Path

# Companies to scrape
COMPANIES = {
    "Novo Nordisk": {
        "url": "https://www.novonordisk.com/careers/find-a-job.html",
        "search_terms": ["marketing", "director", "manager", "switzerland", "denmark"],
        "selectors": {
            "job_list": "[data-automation-id='jobList']",
            "job_title": ".job-title",
            "job_location": ".job-location"
        }
    },
    "Roche": {
        "url": "https://careers.roche.com/global/en",
        "search_terms": ["marketing", "director", "manager", "switzerland"],
        "selectors": {
            "search_box": "#keyword-search",
            "search_button": "[data-test-id='search-button']",
            "job_list": "[data-test-id='job-list']"
        }
    },
    "IQVIA": {
        "url": "https://jobs.iqvia.com/en/jobs",
        "search_terms": ["marketing", "director", "switzerland", "denmark"],
        "selectors": {
            "search_box": "input[placeholder*='Search']",
            "job_list": ".job-listing"
        }
    }
}

def scrape_with_playwright(company_name, company_data):
    """
    Attempt to scrape jobs using Playwright
    This requires Playwright to be installed and browsers set up
    """
    print(f"\n🔍 Testing: {company_name}")
    print(f"   URL: {company_data['url']}")
    
    try:
        from playwright.sync_api import sync_playwright
        
        jobs_found = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            # Navigate to site
            print(f"   Loading page...")
            page.goto(company_data['url'], timeout=30000)
            
            # Wait for content to load
            page.wait_for_load_state('networkidle', timeout=10000)
            
            # Take screenshot for debugging
            screenshot_path = f"/tmp/career_screenshot_{company_name.replace(' ', '_')}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"   📸 Screenshot saved: {screenshot_path}")
            
            # Try to find job elements
            selectors = company_data.get('selectors', {})
            
            for selector_name, selector in selectors.items():
                try:
                    elements = page.query_selector_all(selector)
                    print(f"   Found {len(elements)} elements with '{selector_name}': {selector}")
                    
                    if elements:
                        for i, elem in enumerate(elements[:5]):  # First 5 only
                            text = elem.inner_text() if elem else ""
                            if text:
                                jobs_found.append({
                                    'title': text[:100],
                                    'source': company_name
                                })
                except Exception as e:
                    print(f"   Selector failed: {e}")
            
            browser.close()
        
        return jobs_found
        
    except ImportError:
        print(f"   ❌ Playwright not installed")
        print(f"   💡 Install with: pip install playwright && playwright install chromium")
        return []
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return []

def test_all_companies():
    """Test all three companies"""
    print("=" * 60)
    print("CAREER AGENT - Playwright Test Run")
    print("=" * 60)
    
    all_jobs = []
    
    for company_name, company_data in COMPANIES.items():
        jobs = scrape_with_playwright(company_name, company_data)
        all_jobs.extend(jobs)
    
    print("\n" + "=" * 60)
    print(f"RESULT: {len(all_jobs)} jobs found from Playwright scraping")
    print("=" * 60)
    
    if all_jobs:
        print("\nJobs found:")
        for i, job in enumerate(all_jobs[:10], 1):
            print(f"{i}. [{job['source']}] {job['title']}")
    else:
        print("\n⚠️  No jobs found via Playwright")
        print("💡 Possible reasons:")
        print("   - Site structure changed")
        print("   - Anti-bot protection")
        print("   - Selectors need adjustment")
        print("   - Playwright not properly configured")
    
    return all_jobs

if __name__ == "__main__":
    jobs = test_all_companies()
    
    # Save results
    result = {
        "timestamp": datetime.now().isoformat(),
        "jobs_found": len(jobs),
        "jobs": jobs
    }
    
    with open("/tmp/playwright_test_result.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Results saved to: /tmp/playwright_test_result.json")
