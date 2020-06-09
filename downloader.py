import urllib.request
import threading
import json
import os
import patoolib
from pathlib import Path
import shutil

thread_list = []
path = Path(r'comics').resolve()
img_files = []

def download_img(json_img_object, img):
    img_link = json_img_object.get(f'{img}')
    urllib.request.urlretrieve(img_link, f'{path}' + f'\\{img}.jpg')


with open('img_urls_file.json', 'r') as images:
    json_img_object = json.load(images)

img_count = int(json_img_object.get('count'))

print("Downloading comic pages...")
for img in range(1, img_count):
    thread = threading.Thread(target=download_img, args=[json_img_object, img])
    thread.start()
    thread_list.append(thread)

for threads in thread_list:
    threads.join()

print("Download Complete")

for r, d, f in os.walk(path):
    for file in f:
        if '.jpg' in file:
            img_files.append(os.path.join(r, file))

with open('user_input.json') as inputs:
    json_inputs_object = json.load(inputs)

print("Converting images into cbr format...")
images = tuple(img_files)

comic_name = json_inputs_object.get('f_comic_name')
comic_url = json_inputs_object.get('f_comic_url')
issue_number = json_inputs_object.get('f_issue_number')
delete_image = json_inputs_object.get('f_delete_image')


if comic_url == 'None':
    patoolib.create_archive(f"{path}\\" + f"#{issue_number}.cbr", images, verbosity=-1)
else:
    patoolib.create_archive(f"{path}\\" + "comic.cbr", images, verbosity=-1)

os.remove('img_urls_file.json')
os.remove('user_input.json')

if delete_image == 'yes':
    print("Deleting the images...")
    for f in img_files:
        os.remove(f)
else:
    print(f"Creating folder '{issue_number}' inside the pages folder...\nMoving downloaded images to newly created folder '{issue_number}'...")
    pages_folder_path = Path('pages').resolve()
    new_page_folder_path = str(pages_folder_path) + f'\\{issue_number}'
    os.mkdir(new_page_folder_path)
    for f in img_files:
        shutil.move(f, new_page_folder_path)
    # add funtion to move images here


print(f"{comic_name} #{issue_number} has been downloaded successfully!")