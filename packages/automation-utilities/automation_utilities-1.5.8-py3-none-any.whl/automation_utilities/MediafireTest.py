import requests


def __init__():
    global response
    url = "https://www.mediafire.com/api/1.4/folder/get_content.php"
    params = {
        "r": "nnpu",
        "content_type": "files",
        "filter": "all",
        "order_by": "name",
        "order_direction": "asc",
        "chunk": 1,
        "version": 1.5,
        "folder_key": "hcy8vshstj1mp",
        "response_format": "json"
    }
    response = requests.get(url, params=params).json()


__init__()

print("Response status code:", response.status_code)
print("Response content:")
print(response.text)
