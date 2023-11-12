import requests
import os
import re

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
