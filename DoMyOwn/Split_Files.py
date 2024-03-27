#This was created to split all of the files into folders of 599 files each so that they can be uploaded to factotum

import os
import shutil

directory = r'C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\SDS Files'
target = r'C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\SDS Files'
backup = r'C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\Backup'

shutil.copytree(directory, backup)

directory = backup

files = os.listdir(directory)
files.sort()

for i in range(0, len(files), 599):
    new_directory = os.path.join(target, f'folder_{i // 599 + 1}')
    os.makedirs(new_directory, exist_ok=True)

    for j in range(i, min(i + 599, len(files))):
        shutil.move(os.path.join(directory, files[j]), new_directory)
