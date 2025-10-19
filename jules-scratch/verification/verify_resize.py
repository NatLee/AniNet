from playwright.sync_api import sync_playwright, expect
import os

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    # Set userName in localStorage to prevent the initial popup
    context.add_init_script("localStorage.setItem('userName', 'Jules')")

    page = context.new_page()

    # Get the absolute path to the HTML file
    file_path = os.path.abspath('index.html')
    page.goto(f'file://{file_path}')

    # Wait for the main image to be loaded and visible
    main_image = page.locator('.main-image')
    expect(main_image).to_be_visible(timeout=10000)

    # Add a bounding box
    page.locator('#add').click()

    # Locate the newly added bounding box and its resize handle
    new_box = page.locator('.resize-div').last
    expect(new_box).to_be_visible()

    # The resize handle is typically in the bottom-right corner
    resize_handle = new_box.locator('.ui-resizable-se')

    # Get the initial bounding box of the resizable div
    initial_box = new_box.bounding_box()

    # Perform the resize by dragging the handle
    if initial_box and resize_handle:
        # Start dragging from the center of the resize handle
        handle_box = resize_handle.bounding_box()
        if handle_box:
            page.mouse.move(handle_box['x'] + handle_box['width'] / 2, handle_box['y'] + handle_box['height'] / 2)
            page.mouse.down()
            # Drag to a new position to make it a rectangle
            page.mouse.move(handle_box['x'] + 100, handle_box['y'] + 50)
            page.mouse.up()

    # Take a screenshot to verify the resize
    page.screenshot(path='jules-scratch/verification/verification.png')

    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)
