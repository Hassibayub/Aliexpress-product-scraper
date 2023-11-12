from src.ali_express import AliexpressProductScraper
from src.downloader import download_images, download_video
import json
import os


def main():
    product_ids = ["1005006201952621"]
    
    for product_id in product_ids:
        result, data = AliexpressProductScraper(product_id, 10)

        download_images(result["images"], product_id)
        download_images(result["description"], product_id, is_desc=True)

        json_path = os.path.join("outputs", product_id, f"{product_id}.json")

        if 'videoComponent' in data:
            url = f"https://video.aliexpress-media.com/play/u/ae_sg_item/{data['videoComponent']['videoUid']}/p/1/e/6/t/10301/{data['videoComponent']['videoId']}.mp4"
            download_video(url, product_id)
    
        with open(json_path, "w") as f:
            json.dump(result, f, indent=4, default=str)
    
if __name__ == "__main__":
    main()
