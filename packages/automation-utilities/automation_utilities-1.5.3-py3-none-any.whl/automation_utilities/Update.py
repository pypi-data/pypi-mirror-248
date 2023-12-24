import sys

from automation_utilities.Mediafire import Folder


def update(script_name: str, current_version: str, folder: Folder):
    up_to_date = True
    for child in folder.children:
        if child.name == 'version.txt':
            new_version = child.text()
            if new_version != current_version:
                up_to_date = False

    if not up_to_date:
        for child in folder.children:
            if child.name == script_name:
                executable_name = sys.argv[0].split('\\')[-1]
                open(f'_{executable_name}', 'wb').write(child.content())
                # shutil.move('temp_' + executable_name, executable_name)
                return True
    return False
