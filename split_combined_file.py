import os
from pathlib import Path
import re

def split_combined_file(combined_file, output_folder):
    """
    Split a combined file back into individual files based on separators.
    
    Args:
        combined_file: Path to the combined file
        output_folder: Path to the folder where individual files will be saved
    """
    combined_path = Path(combined_file)
    output_path = Path(output_folder)
    
    # Check if combined file exists
    if not combined_path.exists():
        print(f"Error: Combined file '{combined_file}' does not exist!")
        return
    
    # Create output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Reading combined file: {combined_file}")
    print(f"Output folder: {output_folder}\n")
    
    # Read the combined file
    with open(combined_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by the separator pattern
    # Pattern: \n...\nFILE: filename\n...\n\n
    separator_pattern = r'\n={80}\nFILE: (.+?)\n={80}\n\n'
    
    # Split content and get filenames
    parts = re.split(separator_pattern, content)
    
    # The first part is usually empty or contains text before first separator
    if parts[0].strip()  '':
        parts = parts[1:]
    
    # Process pairs: filename, content, filename, content, ...
    file_count = 0
    for i in range(0, len(parts) - 1, 2):
        filename = parts[i].strip()
        file_content = parts[i + 1].strip()
        
        if filename:
            output_file_path = output_path / filename
            
            try:
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                
                file_count += 1
                print(f"Created {file_count}: {filename}")
            except Exception as e:
                print(f"  Error writing {filename}: {e}")
    
    print(f"\n✓ Successfully split into {file_count} files in '{output_folder}'")

if __name__  "__main__":
    # Define paths
    combined_file = r"D:\doc\msa\part-1\vn\combined_all_files.md"
    output_folder = r"D:\doc\msa\part-1\vn\split_files"
    
    # Run split
    split_combined_file(combined_file, output_folder)
