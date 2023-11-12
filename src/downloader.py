import requests
import os
import re

import warnings
warnings.filterwarnings("ignore")

def download_images(images, product_id, is_desc=False):
    
    if is_desc:
        results = re.findall(r'"https:.+?alicdn.+?"', images)
        if results:
            for idx, result in enumerate(results):
                image_path = os.path.join("outputs", product_id, f"desc_{idx}.jpg")
                with open(image_path, "wb") as f:
                    f.write(requests.get(result[1:-1]).content)
        
    else:        
        for i, image in enumerate(images):
            image_path = os.path.join("outputs", product_id, f"{product_id}_{i}.jpg")
            with open(image_path, "wb") as f:
                f.write(requests.get(image).content)


def download_video(url, product_id):
    try:
        save_path = os.path.join("outputs", product_id, f"video.mp4")
        with requests.get(url, stream=True,verify=False) as response:
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")

