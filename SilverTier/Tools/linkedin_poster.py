import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

LINKEDIN_USER = os.getenv("LINKEDIN_USER")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

async def post_to_linkedin(content):
    if not LINKEDIN_USER or not LINKEDIN_PASSWORD:
        print("Error: LinkedIn credentials not set.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Headed for visibility/login help
        page = await browser.new_page()
        
        await page.goto("https://www.linkedin.com/login")
        await page.fill("#username", LINKEDIN_USER)
        await page.fill("#password", LINKEDIN_PASSWORD)
        await page.click("button[type='submit']")
        
        await page.wait_for_selector(".share-box-feed-entry__trigger")
        await page.click(".share-box-feed-entry__trigger")
        
        await page.wait_for_selector(".ql-editor")
        await page.fill(".ql-editor", content)
        
        await page.click(".share-actions__primary-action")
        await asyncio.sleep(5)
        
        await browser.close()
        print("Successfully posted to LinkedIn")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        content = sys.argv[1]
        asyncio.run(post_to_linkedin(content))
    else:
        print("No content provided.")
