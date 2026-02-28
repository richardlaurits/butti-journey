#!/usr/bin/env python3
"""
🚀 CAREER AGENT - ENHANCED JOB CRAWLER v3 (INTERACTIVE)
========================================================

This version INTERACTS with job sites:
1. Loads the page
2. Enters search criteria (location + keyword)
3. Waits for jobs to load
4. Extracts actual job listings
5. Saves results + screenshots

Much more effective than passive page scraping.
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Configuration
COMPANIES = {
    "roche": {
        "url": "https://careers.roche.com/global/en",
        "search_location": "Switzerland",
        "search_keywords": ["Marketing", "Strategy", "Director", "Manager"],
        "location_input": 'input[placeholder*="location" i]',
        "keyword_input": 'input[placeholder*="keyword" i], input[placeholder*="title" i]',
        "search_button": 'button:has-text("Search"), button[type="submit"]',
        "job_card": "div[data-testid*='job'], li[class*='job'], div[class*='job-item']",
        "job_title": ".job-title, h2, [class*='title']",
        "job_location": ".job-location, [class*='location']",
        "job_link": "a[href*='/job/'], a[class*='job']",
    },
    "novo_nordisk": {
        "url": "https://careers.novonordisk.com/",
        "search_location": "Switzerland",
        "search_keywords": ["Marketing", "Strategy"],
        "location_input": 'input[placeholder*="location" i]',
        "keyword_input": 'input[placeholder*="keyword" i]',
        "search_button": 'button:has-text("Search")',
        "job_card": "[class*='job-card'], article[class*='job']",
        "job_title": "h2, .job-title, a[class*='title']",
        "job_location": ".location, [class*='location']",
        "job_link": "a[href*='/job/'], a[role='link']",
    }
}

# Output directories
RESULTS_DIR = Path("job_results")
SCREENSHOTS_DIR = Path("job_screenshots")
RESULTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)


class JobCrawler:
    def __init__(self, headless=True):
        self.headless = headless
        self.results = {
            "scan_date": datetime.now().isoformat(),
            "companies": {},
            "total_jobs": 0,
        }

    async def search_jobs(self, company_name, config):
        """Search for jobs with specific location and keywords."""
        print(f"\n📄 {company_name.upper()}")
        print(f"   URL: {config['url']}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()

            try:
                # Load page
                print(f"   ⏳ Loading... ", end="", flush=True)
                await page.goto(config["url"], wait_until="domcontentloaded", timeout=30000)
                print("✓")

                # Accept cookies
                print(f"   🍪 Checking cookies... ", end="", flush=True)
                try:
                    await page.click('button:has-text("Accept"), button:has-text("Agree")', timeout=2000)
                    print("✓ Accepted")
                except:
                    print("(none found)")

                # Wait for page to settle
                await page.wait_for_timeout(2000)

                # Take screenshot of search area
                await page.screenshot(path=SCREENSHOTS_DIR / f"{company_name}_01_home.png")

                jobs = []

                # Try each keyword
                for keyword in config["search_keywords"]:
                    print(f"   🔍 Searching for: {config['search_location']} + '{keyword}'")

                    # Clear and fill location
                    try:
                        location_input = page.locator(config["location_input"])
                        if await location_input.count() > 0:
                            await location_input.first.fill("")
                            await location_input.first.type(config["search_location"], delay=50)
                            print(f"      ✓ Location entered")
                    except Exception as e:
                        print(f"      ✗ Location field error: {e}")

                    # Clear and fill keyword
                    try:
                        keyword_input = page.locator(config["keyword_input"])
                        if await keyword_input.count() > 0:
                            await keyword_input.first.fill("")
                            await keyword_input.first.type(keyword, delay=50)
                            print(f"      ✓ Keyword entered")
                    except Exception as e:
                        print(f"      ✗ Keyword field error: {e}")

                    # Click search
                    try:
                        search_btn = page.locator(config["search_button"])
                        if await search_btn.count() > 0:
                            await search_btn.first.click()
                            print(f"      ✓ Search clicked")
                            await page.wait_for_timeout(3000)  # Wait for results
                        else:
                            print(f"      ✗ Search button not found")
                    except Exception as e:
                        print(f"      ✗ Search click error: {e}")

                    # Take screenshot of results
                    await page.screenshot(path=SCREENSHOTS_DIR / f"{company_name}_02_{keyword}.png")

                    # Extract jobs
                    try:
                        job_cards = page.locator(config["job_card"])
                        count = await job_cards.count()
                        print(f"      📋 Found {count} job cards")

                        for i in range(min(count, 10)):  # Limit to 10 per keyword
                            card = job_cards.nth(i)

                            try:
                                title_elem = card.locator(config["job_title"])
                                title = (
                                    await title_elem.first.text_content()
                                    if await title_elem.count() > 0
                                    else "Unknown"
                                ).strip()

                                location_elem = card.locator(config["job_location"])
                                location = (
                                    await location_elem.first.text_content()
                                    if await location_elem.count() > 0
                                    else "Not specified"
                                ).strip()

                                link_elem = card.locator(config["job_link"])
                                link = (
                                    await link_elem.first.get_attribute("href")
                                    if await link_elem.count() > 0
                                    else ""
                                )

                                # Skip duplicates and irrelevant results
                                if any(j["title"] == title for j in jobs):
                                    continue

                                job = {
                                    "title": title,
                                    "location": location,
                                    "link": link or config["url"],
                                    "keyword": keyword,
                                    "company": company_name,
                                }

                                if len(title) > 3 and title not in ["Search", "Filter", "Clear"]:
                                    jobs.append(job)
                                    print(f"         ✓ {title} ({location})")

                            except Exception as e:
                                print(f"         ⚠️  Error processing card: {e}")

                    except Exception as e:
                        print(f"      ✗ Job extraction error: {e}")

                # Save results
                self.results["companies"][company_name] = {
                    "url": config["url"],
                    "jobs_found": len(jobs),
                    "jobs": jobs,
                }
                self.results["total_jobs"] += len(jobs)

                print(f"   ✅ {len(jobs)} jobs extracted for {company_name}")

            except PlaywrightTimeout:
                print(f"   ✗ Timeout loading page")
            except Exception as e:
                print(f"   ✗ Error: {e}")
            finally:
                await browser.close()

    async def run(self):
        """Run the crawler on all companies."""
        print("=" * 70)
        print("🚀 CAREER AGENT - ENHANCED JOB CRAWLER v3 (INTERACTIVE)")
        print("=" * 70)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Companies: {', '.join(COMPANIES.keys())}")
        print("=" * 70)

        start_time = datetime.now()

        for company_name, config in COMPANIES.items():
            await self.search_jobs(company_name, config)

        duration = (datetime.now() - start_time).total_seconds()

        # Save JSON results
        output_file = RESULTS_DIR / f"jobs_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        # Print summary
        print("\n" + "=" * 70)
        print("📊 SUMMARY")
        print("=" * 70)
        print(f"⏱  Scan took: {duration:.1f}s")
        print(f"📍 Total jobs found: {self.results['total_jobs']}")
        print(f"📸 Screenshots saved: {list(SCREENSHOTS_DIR.glob('*.png')).__len__()}")
        print(f"💾 Results: {output_file}")
        print("\n🏆 JOBS BY COMPANY:")
        for company, data in self.results["companies"].items():
            print(f"   {company}: {data['jobs_found']} jobs")
            for job in data["jobs"][:5]:  # Show first 5
                print(f"      • {job['title']} ({job['location']})")
            if len(data["jobs"]) > 5:
                print(f"      ... and {len(data['jobs']) - 5} more")

        print("\n" + "=" * 70)
        print("✅ Done!")
        print("=" * 70)


async def main():
    crawler = JobCrawler(headless=True)
    await crawler.run()


if __name__ == "__main__":
    asyncio.run(main())
