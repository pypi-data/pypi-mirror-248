from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        context = browser.new_context()
        page = context.new_page()
