import json
import os
import re
import requests
from pathlib import Path

def sanitize_filename(filename):
    """Remove or replace characters that are invalid in Windows filenames"""
    # Replace invalid characters with underscore
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '_', filename)

def format_price(price_in_billions):
    """Format price in billions (ty) format"""
    if price_in_billions >= 1:
        return f"{price_in_billions}ty"
    else:
        # Convert to million (tr)
        return f"{int(price_in_billions * 1000)}tr"

def calculate_price_per_m2(total_price_billions, area_m2):
    """Calculate price per square meter in million dong (tr/m2)"""
    if area_m2 == 0:
        return 0
    price_per_m2 = (total_price_billions * 1000) / area_m2  # Convert billion to million, then divide
    return round(price_per_m2, 1)

def download_image(url, save_path):
    """Download image from URL and save to path"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def add_images_to_markdown(md_file_path, images_folder_path):
    """Add or update images section in markdown file"""
    
    images_folder = Path(images_folder_path)
    
    if not images_folder.exists():
        print(f"  Images folder not found: {images_folder}")
        return False
    
    # Get all image files
    image_files = sorted([f.name for f in images_folder.iterdir() if f.is_file()])
    
    if not image_files:
        print(f"  No images found in {images_folder}")
        return False
    
    # Read current markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create images section with actual image links
    images_section = "## Hình ảnh\n\n"
    for image_file in image_files:
        # Use relative path from markdown file to image
        image_path = f"images/{image_file}"
        images_section += f"![{image_file}]({image_path})\n\n"
    
    # Check if images section already exists and replace it
    if "## Hình ảnh" in content:
        # Replace existing section
        pattern = r'## Hình ảnh\n.*?(?=\n##|\Z)'
        new_content = re.sub(pattern, images_section.rstrip(), content, flags=re.DOTALL)
        action = "Updated"
    elif "## Images" in content:
        # Replace existing Images section
        pattern = r'## Images\n.*?(?=\n##|\Z)'
        new_content = re.sub(pattern, images_section.rstrip(), content, flags=re.DOTALL)
        action = "Updated"
    else:
        # Append images to markdown
        new_content = content.rstrip() + "\n\n" + images_section
        action = "Added"
    
    # Write back to file
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def update_all_markdown_images(data_folder='data'):
    """Update all markdown files in data folder with image links"""
    
    data_path = Path(data_folder)
    
    if not data_path.exists():
        print(f"Error: {data_folder} does not exist")
        return
    
    print(f"Scanning folder: {data_path.absolute()}")
    
    # Get all property folders
    property_folders = [f for f in data_path.iterdir() if f.is_dir()]
    
    print(f"Found {len(property_folders)} property folders\n")
    
    updated_count = 0
    for prop_folder in property_folders:
        # Find the markdown file (should have same name as folder)
        md_files = list(prop_folder.glob("*.md"))
        
        if not md_files:
            print(f"No markdown file found in {prop_folder.name}")
            continue
        
        md_file = md_files[0]
        images_folder = prop_folder / "images"
        
        print(f"Processing: {prop_folder.name}")
        if add_images_to_markdown(md_file, images_folder):
            updated_count += 1
    
    print(f"\n✓ Updated {updated_count} markdown files with images")

def create_markdown_content(property_data):
    """Create markdown content for property details"""
    street_name = (property_data.get('street') or {}).get('name', 'N/A')
    district_name = (property_data.get('district') or {}).get('name', 'N/A')
    ward_name = (property_data.get('ward') or {}).get('name', 'N/A')
    
    address = property_data.get('address', 'N/A')
    area = property_data.get('area', 0)
    actual_area = property_data.get('actualArea', 0)
    floors = property_data.get('floors', 0)
    wide = property_data.get('wide', 0)
    depth = property_data.get('depth', 0)
    offering_price = property_data.get('offeringPrice', 0)
    
    price_per_m2 = calculate_price_per_m2(offering_price, actual_area)
    
    full_address = f"{address} {street_name}, {ward_name}, {district_name}"
    
    md_content = f"""# Thông tin Bất Động Sản

## Thông tin cơ bản
- **Địa chỉ**: {full_address}
- **Đường**: {street_name}
- **Phường**: {ward_name}
- **Quận**: {district_name}

## Thông tin diện tích
- **Diện tích**: {area} m²
- **Diện tích thực tế**: {actual_area} m²
- **Số tầng**: {floors}
- **Chiều ngang**: {wide} m
- **Chiều dài**: {depth} m

## Thông tin giá cả
- **Giá rao bán**: {offering_price} tỷ ({format_price(offering_price)})
- **Giá/m²**: {price_per_m2} triệu/m²

## Thông tin pháp lý
- **Loại hợp đồng**: {property_data.get('contractType', 'N/A')}
- **Số sổ**: {property_data.get('certificateSeries', 'N/A')}
- **Trạng thái**: {property_data.get('status', 'N/A')}

## Thông tin liên hệ
"""
    
    # Add owner info if available
    if 'ownerSideUser' in property_data:
        owner = property_data['ownerSideUser']
        md_content += f"""
### Người bán
- **Tên**: {owner.get('name', 'N/A')}
- **Vị trí**: {owner.get('position', 'N/A')}
- **Số điện thoại**: {owner.get('phone', 'N/A')}
- **Facebook**: {owner.get('fbLink', 'N/A')}
"""
    
    # Add criteria information
    if 'criteria' in property_data and property_data['criteria']:
        md_content += "\n## Đặc điểm\n"
        criteria_by_group = {}
        for criterion in property_data['criteria']:
            group_name = criterion.get('groupName', 'Khác')
            if group_name not in criteria_by_group:
                criteria_by_group[group_name] = []
            criteria_by_group[group_name].append(criterion.get('name', ''))
        
        for group_name, criteria in criteria_by_group.items():
            md_content += f"\n### {group_name}\n"
            for criterion in criteria:
                md_content += f"- {criterion}\n"
    
    # Add location info
    md_content += f"""
## Vị trí
- **Tọa độ**: {property_data.get('latitude', 'N/A')}, {property_data.get('longitude', 'N/A')}
- **Place ID**: {property_data.get('placeId', 'N/A')}
- **Tên địa điểm**: {property_data.get('placeName', 'N/A')}

## Thông tin bổ sung
- **ID**: {property_data.get('id', 'N/A')}
- **Ngày tạo**: {property_data.get('createdAt', 'N/A')}
- **Cập nhật lần cuối**: {property_data.get('updatedAt', 'N/A')}
- **Ngày niêm yết**: {property_data.get('listedAt', 'N/A')}
"""
    
    return md_content

def get_price_category(price_in_billions):
    """Determine price category folder based on price"""
    if price_in_billions >= 20:
        return "Tren_20ty"
    elif price_in_billions >= 10:
        return "Tren_10ty"
    elif price_in_billions >= 6:
        return "Tren_6ty"
    else:
        return "Duoi_6ty"

def extract_price_from_folder_name(folder_name):
    """Extract price from folder name (e.g., '1.6ty' or '4.65ty')"""
    import re
    # Look for pattern like "1.6ty" or "15ty" or "500tr"
    match = re.search(r'- (\d+\.?\d*)ty', folder_name)
    if match:
        return float(match.group(1))
    
    # Check for price in millions (tr)
    match = re.search(r'- (\d+)tr', folder_name)
    if match:
        return float(match.group(1)) / 1000  # Convert million to billion
    
    return None

def reorganize_existing_folders(data_folder='data'):
    """Reorganize existing property folders into price categories"""
    
    data_path = Path(data_folder)
    
    if not data_path.exists():
        print(f"Error: {data_folder} does not exist")
        return
    
    # Get all property folders (not category folders)
    all_items = [f for f in data_path.iterdir() if f.is_dir()]
    
    # Identify category folders
    category_names = {"Duoi_6ty", "Tren_6ty", "Tren_10ty", "Tren_20ty"}
    property_folders = [f for f in all_items if f.name not in category_names]
    
    if not property_folders:
        print("No property folders found to reorganize")
        # Check if properties are already in category folders
        for category in category_names:
            cat_path = data_path / category
            if cat_path.exists():
                props_in_cat = list(cat_path.glob("*"))
                if props_in_cat:
                    print(f"  {category}: {len(props_in_cat)} properties already organized")
        return
    
    print(f"Found {len(property_folders)} property folders to organize\n")
    
    moved_count = 0
    for prop_folder in property_folders:
        folder_name = prop_folder.name
        
        # Extract price from folder name
        price = extract_price_from_folder_name(folder_name)
        
        if price is None:
            print(f"⚠ Could not extract price from: {folder_name}")
            continue
        
        # Determine category
        category = get_price_category(price)
        
        # Create category folder if it doesn't exist
        category_path = data_path / category
        category_path.mkdir(exist_ok=True)
        
        # Move property folder to category
        new_path = category_path / folder_name
        
        try:
            prop_folder.rename(new_path)
            print(f"✓ Moved {folder_name[:60]}... → {category} ({price} tỷ)")
            moved_count += 1
        except Exception as e:
            print(f"✗ Failed to move {folder_name}: {e}")
    
    print(f"\n✓ Reorganized {moved_count} properties into price categories")
    
    # Show summary
    print("\nSummary:")
    for category in ["Duoi_6ty", "Tren_6ty", "Tren_10ty", "Tren_20ty"]:
        cat_path = data_path / category
        if cat_path.exists():
            count = len(list(cat_path.iterdir()))
            print(f"  {category}: {count} properties")

def process_property_data(json_file_path, output_base_dir='data', group_by_price=True):
    """Process property data from JSON file"""
    
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Extract properties from the data
    properties = data.get('data', {}).get('data', [])
    
    if not properties:
        print("No properties found in the JSON file")
        return
    
    # Create base output directory
    Path(output_base_dir).mkdir(exist_ok=True)
    
    # Statistics tracking
    processed_count = 0
    skipped_count = 0
    
    # Process each property
    for idx, property_data in enumerate(properties, 1):
        print(f"\nProcessing property {idx}/{len(properties)}...")
        
        # Extract data for folder name
        address = property_data.get('address', 'N/A')
        street_name = (property_data.get('street') or {}).get('name', 'N/A')
        ward_name = (property_data.get('ward') or {}).get('name', 'N/A')
        actual_area = property_data.get('actualArea', 0)
        floors = property_data.get('floors', 0)
        offering_price = property_data.get('offeringPrice', 0)
        
        price_per_m2 = calculate_price_per_m2(offering_price, actual_area)
        
        # Determine price category if grouping is enabled
        if group_by_price:
            price_category = get_price_category(offering_price)
            category_folder = Path(output_base_dir) / price_category
            category_folder.mkdir(exist_ok=True)
            print(f"Price category: {price_category} ({offering_price} tỷ)")
            base_path = category_folder
        else:
            base_path = Path(output_base_dir)
        
        # Create folder name: "2 tang - 45m2 - 1ty6 - 435.47.25 Huỳnh Tấn Phát, Tân Thuận - 35.5tr/m2"
        folder_name = f"{floors} tang - {actual_area}m2 - {format_price(offering_price)} - {address} {street_name}, {ward_name} - {price_per_m2}tr_m2"

        folder_name = sanitize_filename(folder_name)
        
        # Create property folder path
        property_folder = base_path / folder_name
        
        # Check if property folder already exists - skip if it does
        if property_folder.exists():
            print(f"⏭ Skipping (already exists): {folder_name[:70]}...")
            skipped_count += 1
            continue
        
        # Create property folder
        property_folder.mkdir(exist_ok=True)
        print(f"Created folder: {folder_name}")
        
        # Create markdown file
        md_filename = f"{folder_name}.md"
        md_path = property_folder / md_filename
        md_content = create_markdown_content(property_data)
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # Create images folder
        images_folder = property_folder / 'images'
        images_folder.mkdir(exist_ok=True)
        
        # Download images
        media_items = property_data.get('media', [])
        if media_items:
            print(f"Downloading {len(media_items)} images...")
            for media_idx, media in enumerate(media_items, 1):
                url = media.get('url', '')
                if not url:
                    continue
                
                # Get filename from media data or generate one
                filename = media.get('fileName', f'image_{media_idx}.jpg')
                filename = sanitize_filename(filename)
                
                image_path = images_folder / filename
                
                download_image(url, image_path)
                
        else:
            print("No images to download")
        
        # Add images to markdown file
        add_images_to_markdown(md_path, images_folder)
        
        processed_count += 1
    
    # Show summary
    print(f"  ⏭ Skipped: {skipped_count}")
    
    # Show category breakdown if grouping is enabled
    if group_by_price:
        print("\nProperties by price category:")
        for category in ["Duoi_6ty", "Tren_6ty", "Tren_10ty", "Tren_20ty"]:
            cat_path = Path(output_base_dir) / category
            if cat_path.exists():
                count = len(list(cat_path.iterdir()))
                print(f"  {category}: {count} properties")

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "update-images":
            # Update existing markdown files with images
            print("Updating all markdown files with images...")
            update_all_markdown_images()
        elif command == "reorganize":
            # Reorganize existing folders into price categories
            print("Reorganizing folders by price categories...")
            reorganize_existing_folders()
        elif command == "help":
            print("Usage:")
            print("  python process_property.py              - Process JSON and create properties")
            print("  python process_property.py update-images - Update markdown files with images")
            print("  python process_property.py reorganize   - Reorganize folders by price")
        else:
            print(f"Unknown command: {command}")
            print("Run 'python process_property.py help' for usage")
    else:
        # Process all JSON files in data_json folder
        json_folder = r"D:\myhouse\tt-20260715T104536Z-1-001\tt\data_json"
        
        if not os.path.exists(json_folder):
            print(f"Error: Folder {json_folder} not found!")
        else:
            # Get all JSON files
            json_files = sorted([f for f in os.listdir(json_folder) if f.endswith('.json')])
            
            if not json_files:
                print(f"No JSON files found in {json_folder}")
            else:
                print(f"Found {len(json_files)} JSON file(s) to process")
                print("Properties will be organized into price categories:")
                print("  - Duoi_6ty: Under 6 billion")
                print("  - Tren_6ty: 6-10 billion")
                print("  - Tren_10ty: 10-20 billion")
                print("  - Tren_20ty: Above 20 billion\n")
                
                total_processed = 0
                total_skipped = 0
                
                for json_file in json_files:
                    json_path = os.path.join(json_folder, json_file)
                    print(f"\n{'='*70}")
                    print(f"Processing file: {json_file}")
                    print(f"{'='*70}")
                    
                    process_property_data(json_path, output_base_dir='data', group_by_price=True)
                
                print(f"\n{'='*70}")
                print(f"✓ All {len(json_files)} JSON files processed successfully!")
                print(f"{'='*70}")
                
                # Show final summary
                print("\nFinal Property Distribution:")
                for category in ["Duoi_6ty", "Tren_6ty", "Tren_10ty", "Tren_20ty"]:
                    cat_path = Path("data") / category
                    if cat_path.exists():
                        count = len(list(cat_path.iterdir()))
                        print(f"  {category}: {count} properties")
                
                print("\nAvailable commands:")
                print("  python process_property.py update-images - Update markdown files with images")
                print("  python process_property.py reorganize   - Reorganize existing folders by price")
