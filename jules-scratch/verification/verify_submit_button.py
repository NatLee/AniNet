import os
from playwright.sync_api import sync_playwright, expect

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = browser.new_page()

    # Construct the absolute path to index.html
    file_path = os.path.abspath('index.html')
    url = f'file://{file_path}'

    # Set a username in localStorage to bypass the initial popup
    page.goto(url)
    page.evaluate("localStorage.setItem('userName', 'test-user')")

    # Reload the page to ensure the username is recognized
    page.goto(url)

    # Wait for the page to load
    page.wait_for_selector('.main-image')

    # Click the "Submit Annotation" button
    page.on('dialog', lambda dialog: dialog.accept())
    page.get_by_role("button", name="Submit Annotation").click()

    # Take a screenshot
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)
