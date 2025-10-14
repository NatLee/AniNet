import re
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("file:///app/index.html")

    # Dismiss the initial dialog
    try:
        page.locator("button.swal-button--confirm").click(timeout=5000)
    except Exception:
        pass  # Dialog may not appear if user is already set

    # Wait for the image to load
    image_locator = page.locator("img.main-image")
    expect(image_locator).to_have_attribute("src", re.compile(r"https://"), timeout=15000)
    expect(image_locator).to_be_visible()

    # Click the "add" button
    page.locator("#add").click()

    page.screenshot(path="jules-scratch/verification/verification.png")
    browser.close()