import re
from pathlib import Path


def split_file_by_separator(input_file, output_folder, separator_pattern=r"^={80}$", 
                            file_prefix="part", file_extension=".txt"):
    input_path = Path(input_file)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    content = input_path.read_text(encoding='utf-8')
    parts = [p.strip() for p in re.split(separator_pattern, content, flags=re.MULTILINE) if p.strip()]
    
    print(f"Splitting into {len(parts)} files\n")
    for idx, part in enumerate(parts, 1):
        output_file = output_path / f"{file_prefix}_{idx:03d}{file_extension}"
        output_file.write_text(part, encoding='utf-8')
        print(f"[{idx}/{len(parts)}] {output_file.name} ({len(part):,} chars)")
    
    print(f"\n✓ Done! {len(parts)} files in: {output_path}")


def split_file_by_lines(input_file, output_folder, lines_per_file=100, 
                        file_prefix="part", file_extension=".txt"):
    input_path = Path(input_file)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    lines = input_path.read_text(encoding='utf-8').splitlines(keepends=True)
    num_files = (len(lines) + lines_per_file - 1) // lines_per_file
    
    print(f"Splitting {len(lines)} lines into {num_files} files\n")
    for idx in range(num_files):
        start = idx * lines_per_file
        end = min(start + lines_per_file, len(lines))
        output_file = output_path / f"{file_prefix}_{idx+1:03d}{file_extension}"
        output_file.write_text(''.join(lines[start:end]), encoding='utf-8')
        print(f"[{idx+1}/{num_files}] {output_file.name} ({end-start} lines)")
    
    print(f"\n✓ Done! {num_files} files in: {output_path}")


def split_file_by_size(input_file, output_folder, max_size_mb=1, 
                       file_prefix="part", file_extension=".txt"):
    input_path = Path(input_file)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    content = input_path.read_text(encoding='utf-8')
    max_bytes = max_size_mb * 1024 * 1024
    chunk_chars = int(max_bytes * len(content) / len(content.encode('utf-8')))
    
    print(f"Splitting file ({len(content):,} chars) into ~{max_size_mb}MB chunks\n")
    file_idx = 1
    for pos in range(0, len(content), chunk_chars):
        chunk = content[pos:pos + chunk_chars]
        output_file = output_path / f"{file_prefix}_{file_idx:03d}{file_extension}"
        output_file.write_text(chunk, encoding='utf-8')
        print(f"[{file_idx}] {output_file.name} ({len(chunk.encode('utf-8')):,} bytes)")
        file_idx += 1
    
    print(f"\n✓ Done! {file_idx-1} files in: {output_path}")


def main():
    input_file = r"D:\New folder\a.txt"
    output_folder = r"D:\New folder\merge - split file\split_output"
    split_file_by_separator(input_file, output_folder, r"^={80}$", "doc", ".md")


if __name__ == "__main__":
    main()