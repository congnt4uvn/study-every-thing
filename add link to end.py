from pathlib import Path

# Input folder path
folder_path = r"D:\New folder\study-every-thing\aws"

folder = Path(folder_path)

# Get all .md files sorted by name
md_files = sorted(folder.glob("*.md"))

# Add next file link to each file
for i in range(len(md_files) - 1):
    current_file = md_files[i]
    next_file = md_files[i + 1]

    next_link = f"\n\n[Next]({next_file.name})\n"

    # Append next link
    with open(current_file, "a", encoding="utf-8") as f:
        f.write(next_link)

    print(f"Updated: {current_file.name} -> {next_file.name}")

print("Done!")