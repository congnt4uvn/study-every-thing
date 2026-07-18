from pathlib import Path

# Change this to your parent folder
parent_folder = Path(r"D:\job\study-every-thing\auto post fb\posts")

# Get all folders
folders = [f for f in parent_folder.iterdir() if f.is_dir()]

# Sort by current folder name (optional)
folders.sort(key=lambda x: x.name.lower())

# Step 1: Rename to temporary names to avoid conflicts
temp_folders = []
for i, folder in enumerate(folders):
    temp_name = parent_folder / f"__temp__{i}"
    folder.rename(temp_name)
    temp_folders.append(temp_name)

# Step 2: Rename to final names (1, 2, 3, ...)
for i, temp_folder in enumerate(temp_folders, start=1):
    new_name = parent_folder / str(i)
    temp_folder.rename(new_name)

print(f"Renamed {len(temp_folders)} folders successfully.")