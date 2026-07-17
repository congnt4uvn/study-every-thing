import requests
import os
from pathlib import Path
import time


# Create images directory
IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)


# Curated list of Unsplash photo IDs for houses
HOUSE_PHOTO_IDS = [
    "1568605114967-8130f3a36994", "1512917774080-9991f1c4c750", "1605146769289-440113cc3d00",
    "1564013799919-ab600027ffc6", "1600585154340-be6161a56a0c", "1600607687939-ce8a6c25118c",
    "1600566753190-17f0baa2a6c3", "1570129477492-45c003edd2be", "1600047908359-ce3e4782a1a2",
    "1600585154526-990dced4db0d", "1600047908084-b9dad4e2b82c", "1576941089067-2de3c901e126",
    "1600585154084-c7b1bc85f9d3", "1600585154084-c7b1bc85f9d3", "1600047907808-71c32c5b8f70",
    "1600047908082-44c39c4dde22", "1600047908082-44c39c4dde22", "1600047908082-44c39c4dde22",
    "1598228723193-274e1ee14b54", "1600566752355-7f3e85aae1fd", "1600573472550-94bb0e65c05b",
    "1600596542815-ffad4c1539a9", "1600047907728-36c03f8abe1e", "1565008576549-57569a049c20",
    "1600047908227-da0e15868a2f", "1600047908358-417b8878c73e", "1600047908554-4a1ed8e5e1a2",
    "1600047908715-3e1e0cf5dd7f", "1600585154084-c7b1bc85f9d3", "1600047908227-da0e15868a2f",
    "1513584684374-8bab748fbf90", "1600047908358-417b8878c73e", "1576941089067-2de3c901e126",
    "1605276374104-804a0e53bddd", "1600047909807-3e4605f70c3b", "1600607687920-4e2a09cf159d",
    "1600047909827-e3b1fc0f2b54", "1600566753086-00dc30992259", "1600573472550-94bb0e65c05b",
    "1600047909807-3e4605f70c3b", "1600585154340-be6161a56a0c", "1600047908082-44c39c4dde22",
    "1572120360610-d971b9d7767c", "1600047908715-3e1e0cf5dd7f", "1600566753190-17f0baa2a6c3",
    "1600047908554-4a1ed8e5e1a2", "1600607687920-4e2a09cf159d", "1600047908084-b9dad4e2b82c",
    "1572120360906-15a4a2e1e52f", "1600566752413-2a67d7972d45", "1600047908227-da0e15868a2f",
    "1586461404398-e8d27e6e5d3b", "1600047908358-417b8878c73e", "1600047909827-e3b1fc0f2b54",
    "1598228723193-274e1ee14b54", "1600047907728-36c03f8abe1e", "1600047908082-44c39c4dde22",
    "1600585154526-990dced4db0d", "1600596542815-ffad4c1539a9", "1600047907808-71c32c5b8f70",
    "1600047908715-3e1e0cf5dd7f", "1600566753086-00dc30992259", "1580587948550-64d9e2e5e7c5",
    "1600573472550-94bb0e65c05b", "1600047909807-3e4605f70c3b", "1600585154084-c7b1bc85f9d3",
    "1605146769289-440113cc3d00", "1600566752355-7f3e85aae1fd", "1600047908358-417b8878c73e",
    "1599809275671-ec5cf9c8c1d4", "1600047908227-da0e15868a2f", "1600047908084-b9dad4e2b82c",
    "1600566752413-2a67d7972d45", "1600047908554-4a1ed8e5e1a2", "1600607687920-4e2a09cf159d",
    "1605276374104-804a0e53bddd", "1600047909827-e3b1fc0f2b54", "1572120360610-d971b9d7767c",
    "1600047907728-36c03f8abe1e", "1600596542815-ffad4c1539a9", "1600047907808-71c32c5b8f70",
    "1572120360906-15a4a2e1e52f", "1600585154526-990dced4db0d", "1598228723193-274e1ee14b54",
    "1586461404398-e8d27e6e5d3b", "1600566753086-00dc30992259", "1580587948550-64d9e2e5e7c5",
    "1599809275671-ec5cf9c8c1d4", "1600566752355-7f3e85aae1fd", "1600573472550-94bb0e65c05b",
    "1600585154340-be6161a56a0c", "1600047909807-3e4605f70c3b", "1565008576549-57569a049c20",
    "1512917774080-9991f1c4c750", "1576941089067-2de3c901e126", "1600047908715-3e1e0cf5dd7f",
    "1513584684374-8bab748fbf90", "1600607687939-ce8a6c25118c", "1605276374104-804a0e53bddd",
    "1600566752413-2a67d7972d45", "1598228723193-274e1ee14b54", "1600047908358-417b8878c73e",
]


def download_from_unsplash(num_images=100):
    """
    Download images from Unsplash using public direct URLs (no API key required)
    Example URL: https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800
    """
    print(f"Downloading {num_images} house images from Unsplash...")
    print("Using public URLs - no API key required!")
   
    successful_downloads = 0
    images_to_download = min(num_images, len(HOUSE_PHOTO_IDS))
   
    for i in range(images_to_download):
        try:
            photo_id = HOUSE_PHOTO_IDS[i]
            # Direct Unsplash image URL (public, no API key needed)
            url = f"https://images.unsplash.com/photo-{photo_id}?w=800"
           
            print(f"Downloading image {i+1}/{images_to_download}...", end=" ")
           
            response = requests.get(url, timeout=15)
           
            if response.status_code == 200:
                # Save image
                image_path = IMAGES_DIR / f"house_{i+1:03d}.jpg"
                with open(image_path, 'wb') as f:
                    f.write(response.content)
               
                successful_downloads += 1
                print(f"✓ Saved to {image_path}")
            else:
                print(f"✗ Failed (status code: {response.status_code})")
           
            # Small delay to be respectful to the server
            time.sleep(0.3)
           
        except Exception as e:
            print(f"✗ Error: {e}")
            continue
   
    print(f"\n{'='*50}")
    print(f"Completed! Successfully downloaded {successful_downloads}/{images_to_download} images")
    print(f"Images saved in: {IMAGES_DIR.absolute()}")
    print(f"{'='*50}")




if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("House Image Downloader - Unsplash Public URLs")
    print("=" * 50 + "\n")


   
    # Download 100 house images from public Unsplash URLs (no API key required)
    download_from_unsplash(num_images=100)
