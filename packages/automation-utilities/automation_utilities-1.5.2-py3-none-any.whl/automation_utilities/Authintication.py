from automation_utilities.Mediafire import Folder


def allowed_users(folder_id: str):
    for file in Folder(folder_id).children:
        if file.name == 'users.txt':
            return [line.split(':')[1].strip() for line in file.content()]
