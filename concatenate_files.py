import os
from pathlib import Path

#concatenate_files
def concatenate_files(source_folder, output_file):
    """
    Concatenate all files in the source folder into a single output file.
    
    Args:
        source_folder: Path to the folder containing files to concatenate
        output_file: Path to the output file
    """
    source_path = Path(source_folder)
    
    # Check if source folder exists
    if not source_path.exists():
        print(f"Error: Source folder '{source_folder}' does not exist!")
        return
    
    # Get all files and sort them
    files = sorted([f for f in source_path.iterdir() if f.is_file()])
    
    if not files:
        print(f"No files found in '{source_folder}'")
        return
    
    print(f"Found {len(files)} files to concatenate")
    print(f"Output file: {output_file}\n")
    
    # Open output file for writing
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, file_path in enumerate(files, 1):
            print(f"Processing {i}/{len(files)}: {file_path.name}")
            
            # Write a separator with filename
            outfile.write(f"\n{'='*80}\n")
            outfile.write(f"FILE: {file_path.name}\n")
            outfile.write(f"{'='*80}\n\n")
            
            try:
                # Read and write file content
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write("\n\n")
            except Exception as e:
                print(f"  Warning: Error reading {file_path.name}: {e}")
                outfile.write(f"[Error reading file: {e}]\n\n")
    
    print(f"\n✓ Successfully concatenated {len(files)} files into '{output_file}'")

if __name__  "__main__":
    # Define paths
    source_folder = r"D:\doc\aws\part-1\vn"
    output_file = r"D:\doc\aws\part-1\vn\combined_all_files.md"
    
    # Run concatenation
    concatenate_files(source_folder, output_file)
