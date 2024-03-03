import json
import os
from logger import logger

def reset_directory(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    # Delete existing files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)

def save_post_to_file(url: str, post_title: str, post_content: str, post_comments: list[str], directory: str) -> None:
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    post_data = {
        "url": url,
        "post_title": post_title,
        "post_content": post_content,
        "post_comments": post_comments
    }

    post_id = url.split('/')[-3]

    file_path = os.path.join(directory, f'post_{post_id}_{post_title}.json')
    with open(file_path, 'w') as f:
        json.dump(post_data, f)

    logger.debug(f'Saved post to: post_{post_id}_{post_title}.json')
