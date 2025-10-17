import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        await page.goto(f'file://{file_path}')

        # Set userName in local storage to prevent the sweet alert from appearing
        await page.evaluate("() => { localStorage.setItem('userName', 'Jules'); }")

        # Reload the page to apply the local storage change
        await page.reload()

        # Wait for the page to load
        await page.wait_for_load_state('networkidle')

        # Add a new frame
        await page.click('#add', force=True)

        # Take a screenshot of the desktop view
        await page.screenshot(path='jules-scratch/verification/desktop_view.png')

        # Resize the window to a mobile size
        await page.set_viewport_size({"width": 375, "height": 667})

        # Take a screenshot of the mobile view
        await page.screenshot(path='jules-scratch/verification/mobile_view.png')

        # Add some dummy rank data to local storage
        await page.evaluate("() => { window.localStorage.setItem('rankData', JSON.stringify({'Jules': 10, 'Agent': 5})); }")

        # Click the leaderboard button
        await page.click('#rank', force=True)

        # Wait for the leaderboard to be visible
        await page.wait_for_selector('#rank-container.active')

        # Take a screenshot of the leaderboard
        await page.screenshot(path='jules-scratch/verification/leaderboard_view.png')

        await browser.close()

asyncio.run(main())