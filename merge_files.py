from pathlib import Path


def merge_files(input_folder, output_file, file_pattern="*.txt", separator="\n\n" + "="*80 + "\n\n"):
    input_path = Path(input_folder)
    output_path = Path(output_file)
    
    files = sorted([f for f in input_path.glob(file_pattern) if f.is_file()])
    print(f"Merging {len(files)} files → {output_path.name}\n")
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for idx, file_path in enumerate(files, 1):
            print(f"[{idx}/{len(files)}] {file_path.name}")
            try:
                outfile.write(f"# FILE: {file_path.name}\n# Path: {file_path}\n\n")
                outfile.write(file_path.read_text(encoding='utf-8'))
                if idx < len(files):
                    outfile.write(separator)
            except Exception as e:
                print(f"✗ Error: {e}")
    
    print(f"\n✓ Done! Size: {output_path.stat().st_size:,} bytes")


def main():
    input_folder = r"C:\Temp\code\o_msa"
    output_file = r"C:\Temp\code\merge - split file\merged_output.txt"
    merge_files(input_folder, output_file, "*.md")


if __name__ == "__main__":
    main()