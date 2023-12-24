from automation_utilities.Mediafire import Folder


def allowed_users(folder: Folder = None, folder_id: str = None):
    for file in (folder if folder else Folder(folder_id)).children:
        if file.name == 'users.txt':
            file_content = file.text()
            return [line.split(':')[1].strip() for line in file_content.strip().split('\n')]
