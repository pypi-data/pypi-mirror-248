import requests
from bs4 import BeautifulSoup


class File:
    def __init__(self, file_id: str, normal_download_link: str):
        self.name = file_id
        self.normal_download_link = normal_download_link

    def content(self):
        soup = BeautifulSoup(requests.get(self.normal_download_link).text, 'html.parser')
        url = soup.find('a', attrs={'aria-label': "Download file"}).get('href')
        return requests.get(url).content

    def text(self):
        soup = BeautifulSoup(requests.get(self.normal_download_link).text, 'html.parser')
        url = soup.find('a', attrs={'aria-label': "Download file"}).get('href')
        return requests.get(url).text


class Folder:
    def __init__(self, folderkey):
        url = "https://www.mediafire.com/api/1.4/folder/get_content.php"
        params = {
            "r": "nnpu",
            "content_type": "files",
            "filter": "all",
            "order_by": "name",
            "order_direction": "asc",
            "chunk": 1,
            "version": 1.5,
            "folder_key": folderkey,
            "response_format": "json"
        }
        folder_content = requests.get(url, params=params).json()['response']['folder_content']
        self.files = [File(file['filename'], file['links']['normal_download']) for file in folder_content['files']]
