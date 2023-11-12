from src.ali_express import AliexpressProductScraper
from src.downloader import download_images
import json
import os


def main():
    product_ids = ["1005006201952621"]
    
    for product_id in product_ids:
        result = AliexpressProductScraper(product_id, 10)

        download_images(result["images"], product_id)
        download_images(result["description"], product_id, is_desc=True)

        json_path = os.path.join("outputs", product_id, f"{product_id}.json")
        with open(json_path, "w") as f:
            json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()
