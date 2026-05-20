
import os
from pathlib import Path


def merge_files(parent_folder, output_file=None):
    parent_path = Path(parent_folder)
    if not parent_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {parent_folder}")
    
    output_file = Path(output_file) if output_file else parent_path / "merged_output.txt"
    
    all_files = sorted([
        Path(root) / file
        for root, _, files in os.walk(parent_path)
        for file in files
        if (Path(root) / file).resolve() != output_file.resolve()
    ])
    
    print(f"Found {len(all_files)} files to merge")
    
    merged_count = 0
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
        for idx, file_path in enumerate(all_files, 1):
            try:
                rel_path = file_path.relative_to(parent_path)
                outfile.write(f"\n{'='*80}\nFile {idx}/{len(all_files)}: {rel_path}\n{'='*80}\n\n")
                outfile.write(file_path.read_text(encoding='utf-8', errors='ignore'))
                outfile.write("\n\n")
                merged_count += 1
                print(f"[{idx}/{len(all_files)}] Merged: {rel_path}")
            except Exception as e:
                print(f"[{idx}/{len(all_files)}] Error: {e}")
    
    return merged_count, output_file


def main(parent_folder):
    try:
        output_file = Path(__file__).parent / "merged_output.txt"
        print(f"Merging files from: {parent_folder}\n")
        
        count, output_path = merge_files(parent_folder, output_file)
        print(f"\n✓ Success! Merged {count} files into: {output_path}")
        print(f"Total size: {output_path.stat().st_size:,} bytes")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main(r"C:\Temp\code\generate doc i .md")



