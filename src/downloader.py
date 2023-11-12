import requests
import os 

def download_images(images, product_id):
    for i, image in enumerate(images):
        image_path = os.path.join('outputs', product_id, f'{product_id}_{i}.jpg')
        with open(image_path, 'wb') as f:
            f.write(requests.get(image).content)