import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_suggestions():
    html = requests.get("https://email-fake.com/").text
    soup = BeautifulSoup(html, "html.parser")
    return [child.text for child in soup.find('div', class_="tt-suggestions").children]


def get_message(email: str, timeout: int = 30):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(executable_path="C:\\firefox\\firefox.exe")
        context = browser.new_context()
        page = context.new_page()
        start = time.time()
        while time.time() - start < timeout:
            try:
                page.goto(f"https://email-fake.com/{email}")
                return page.inner_html('.mess_bodiyy')
            except Exception as e:
                print(e)
