
import os
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Set userName in localStorage to bypass the initial popup
    page.add_init_script("localStorage.setItem('userName', 'Jules');")

    # Navigate to the local index.html file
    page.goto(f"file://{os.getcwd()}/index.html")

    # Wait for the image to load and the first box to be added
    page.wait_for_selector('.resize-div')

    # Get the box and image elements
    box = page.locator('.resize-div').first
    image_container = page.locator('.image-container')

    # Get the bounding boxes
    box_bounds = box.bounding_box()
    image_bounds = image_container.bounding_box()

    # Calculate start and end points
    start_x = box_bounds['x'] + box_bounds['width'] / 2
    start_y = box_bounds['y'] + box_bounds['height'] / 2

    # Target the bottom-right corner of the image container
    end_x = image_bounds['x'] + image_bounds['width'] - 1
    end_y = image_bounds['y'] + image_bounds['height'] - 1

    # Perform the drag using mouse actions
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    page.mouse.move(end_x, end_y)
    page.mouse.up()

    # Take a screenshot
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
