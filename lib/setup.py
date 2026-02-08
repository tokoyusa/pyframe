import os


CONTENT_FOLDERS = [
    'content/videos',
    'content/gifs',
    'content/compressed_gifs',
    'content/unpacked_gifs',
    'content/merged_images'
]


def setup_folders():
    for folder in CONTENT_FOLDERS:
        os.makedirs(folder, exist_ok=True)
    print("Content folders initialized")
