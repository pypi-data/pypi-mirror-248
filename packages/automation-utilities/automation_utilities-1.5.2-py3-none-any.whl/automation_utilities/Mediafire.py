import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class File:
    def __init__(self, file_id: str, file_name: str):
        self.id = file_id
        self.name = file_name

    def content(self):
        html = requests.get(f"https://www.mediafire.com/file/{self.id}/{self.name}").text
        soup = BeautifulSoup(html, 'html.parser')
        url = soup.find('a', attrs={'aria-label': "Download file"}).get('href')
        return requests.get(url).text


class Folder:
    def __init__(self, folder_id: str):
        self.children = []
        with sync_playwright() as playwright:
            page = playwright.firefox.launch(executable_path='c:/firefox/firefox.exe').new_page()
            page.goto(f'https://www.mediafire.com/folder/{folder_id}', wait_until='commit')
            while True:
                try:
                    list_items = page.query_selector('#main_list').query_selector_all('li')
                    if len(list_items) == 0:
                        continue
                    for item in list_items:
                        file_id = item.get_attribute('id').split('-')[1].strip()
                        file_name = item.query_selector('a.foldername').text_content().strip()
                        self.children.append(File(file_id, file_name))
                    break
                except AttributeError:
                    pass
