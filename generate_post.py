import random
import os

# Define possible values for dynamic content
locations = [
    'Huỳnh Tấn Phát',
    'Nguyễn Thị Thập',
    'Trần Xuân Soạn'
]

dimension_options = {
    '5*20': '100m2',
    '5*30': '150m2',
    '4*20': '80m2',
    '4*25': '100m2',
    '4*15': '60m2',
    '5 x 20': '100m2',
    '5 x 30': '150m2',
    '4 x 20': '80m2',
    '4 x 25': '100m2',
    '4 x 15': '60m2',
    '5m x 20m': '100m2',
    '5m x 30m': '150m2',
    '4m x 20m': '80m2',
    '4m x 25m': '100m2',
    '4m x 15m': '60m2'
}

price_per_m2_range = (90, 120) # in triệu/m2

contact_prefixes = ['ibox:', 'liên hệ:', 'ib:', "phone: "]
phone_number_parts = ['0358', '965', '708']
separator_options = ['.', '-', '_', ' ']

base_posts_path = r"D:\job\study-every-thing\auto post fb\posts"

# Loop through folders 1 to 1000 to update content
for i in range(1, 50):
    folder_path = os.path.join(base_posts_path, str(i))
    content_file_path = os.path.join(folder_path, 'content.txt')

    # Ensure the folder exists (it should from previous steps, but good practice)
    os.makedirs(folder_path, exist_ok=True)

    # Randomly select values
    selected_location = random.choice(locations)
    selected_dimensions_key, selected_area_m2 = random.choice(list(dimension_options.items()))

    # Extract numerical part of area for calculation
    area_value = int(selected_area_m2.replace('m2', ''))

    # Random price per m2
    price_per_m2 = random.randint(price_per_m2_range[0], price_per_m2_range[1])
    total_price_billion = (area_value * price_per_m2) / 1000 # Convert to tỷ (billions)

    # Randomize contact prefix and phone number format
    selected_contact_prefix = random.choice(contact_prefixes)
    selected_separator = random.choice(separator_options)
    formatted_phone_number = selected_separator.join(phone_number_parts)

    # Construct the content string
    content = f"""
Q7 - {selected_location} - {total_price_billion:.1f} t.ỷ -  {selected_area_m2},
Diện tích: {selected_dimensions_key}
- S.ổ hồng r.iêng
- Gần chợ, trường học, nhiều tiện ích
{selected_contact_prefix} {formatted_phone_number}
#batdongsantanphat
"""

    try:
        with open(content_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content updated for: {content_file_path}")
    except Exception as e:
        print(f"Error writing to {content_file_path}: {e}")