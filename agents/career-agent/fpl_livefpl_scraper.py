#!/usr/bin/env python3
"""
Scrape FPL team data from LiveFPL using Playwright
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

async def scrape_livefpl_team(team_id=17490):
    """Scrape FPL team from LiveFPL."""
    
    url = f"https://www.livefpl.net/teams/{team_id}"
    
    print("=" * 70)
    print(f"🏆 LIVEFPL SCRAPER - Team {team_id}")
    print("=" * 70)
    print(f"📄 URL: {url}")
    print()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Load page
            print("⏳ Loading page... ", end="", flush=True)
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            print("✓")
            
            # Wait for content
            await page.wait_for_timeout(3000)
            
            # Take screenshot
            screenshot_path = Path("job_screenshots/livefpl_team.png")
            await page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot: {screenshot_path}")
            
            # Get page content
            html = await page.content()
            
            # Try to find player table
            print("🔍 Searching for player data...")
            
            # Look for common FPL player selectors
            players = []
            
            # Try method 1: Look for table rows with player data
            rows = await page.locator("tr[data-player], tr.player-row").all()
            print(f"   Found {len(rows)} player rows (method 1)")
            
            if len(rows) == 0:
                # Try method 2: More generic approach
                rows = await page.locator("table tbody tr").all()
                print(f"   Found {len(rows)} table rows (method 2)")
            
            # Extract player data
            for i, row in enumerate(rows[:15]):  # First 15 players (starting 11 + subs)
                try:
                    # Get text content
                    text = await row.text_content()
                    
                    # Try to extract player name (usually in first column)
                    cells = await row.locator("td").all()
                    
                    if len(cells) > 0:
                        name_cell = await cells[0].text_content()
                        
                        player_data = {
                            "position": i + 1,
                            "name": name_cell.strip() if name_cell else "Unknown",
                            "full_row": text.strip()
                        }
                        
                        players.append(player_data)
                        print(f"   [{i+1}] {name_cell.strip() if name_cell else 'Unknown'}")
                
                except Exception as e:
                    print(f"   ⚠️  Row {i+1}: {e}")
            
            # Try alternative: Get all text and parse it
            if len(players) < 11:
                print("\n📊 Alternative extraction:")
                body_text = await page.locator("body").text_content()
                print("   (Page text extracted, see file)")
                
                # Save full page text
                with open("job_screenshots/livefpl_page_text.txt", "w") as f:
                    f.write(body_text if body_text else "No content")
            
            # Save results
            results = {
                "team_id": team_id,
                "url": url,
                "scraped_at": datetime.now().isoformat(),
                "players_found": len(players),
                "players": players,
                "screenshot": str(screenshot_path)
            }
            
            results_file = Path("job_results/livefpl_team.json")
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)
            
            print()
            print("=" * 70)
            print(f"✅ RESULTS")
            print("=" * 70)
            print(f"📍 Players extracted: {len(players)}")
            print(f"💾 Results saved: {results_file}")
            print(f"📸 Screenshot: {screenshot_path}")
            print()
            
            if len(players) > 0:
                print("👥 TEAM:")
                for p in players:
                    print(f"   [{p['position']}] {p['name']}")
            
            return results
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        finally:
            await browser.close()

async def main():
    await scrape_livefpl_team(team_id=17490)

if __name__ == "__main__":
    asyncio.run(main())
