from playwright.sync_api import sync_playwright
import os

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Get the absolute path to the index.html file
    file_path = os.path.abspath('index.html')
    page.goto(f'file://{file_path}')

    # Wait for the main image to be loaded
    page.wait_for_selector('.main-image', state='visible')

    # Give the image a moment to render fully
    page.wait_for_timeout(2000)

    # Take a screenshot of the initial state
    page.screenshot(path='jules-scratch/verification/verification_no_grid.png')

    # Press the 'd' key to toggle the validation grid
    page.press('body', 'd')

    # Wait for the grid to appear
    page.wait_for_selector('.grid-overlay', state='visible')
    page.wait_for_timeout(500)

    # Take a screenshot with the validation grid
    page.screenshot(path='jules-scratch/verification/verification_with_grid.png')

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
