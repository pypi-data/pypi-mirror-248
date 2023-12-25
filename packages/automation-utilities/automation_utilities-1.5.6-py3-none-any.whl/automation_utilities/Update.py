import sys

from automation_utilities.Mediafire import Folder


def update(script_name: str, current_version: str, folder: Folder):
    new_version = None
    up_to_date = True
    for child in folder.files:
        if child.name == 'version.txt':
            new_version = child.text()
            if new_version != current_version:
                up_to_date = False

    if not up_to_date:
        for child in folder.files:
            if child.name == script_name:
                print("Downloading update...")
                executable_name = sys.argv[0].split('\\')[-1].split('.')
                open(f'{script_name.split(".")[0]}_V{new_version}.{executable_name[-1]}', 'wb').write(child.content())
                return True
    return False
