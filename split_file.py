import os
from pathlib import Path


def split_file_by_lines(input_file, output_folder=None, files_per_folder=100, lines_per_file=1000):
    input_path = Path(input_file)
    if not input_path.is_file():
        raise ValueError(f"Not a file: {input_file}")
    
    output_folder = Path(output_folder) if output_folder else input_path.parent / f"{input_path.stem}_split"
    output_folder.mkdir(exist_ok=True)
    
    print(f"Splitting: {input_path.name} ({lines_per_file} lines/file, {files_per_folder} files/folder)\n")
    
    file_count = folder_count = line_count = total_lines = 0
    current_folder = current_file = None
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
        for line in infile:
            if current_file is None or line_count >= lines_per_file:
                if current_file:
                    current_file.close()
                
                file_count += 1
                line_count = 0
                
                if (file_count - 1) % files_per_folder == 0:
                    folder_count += 1
                    current_folder = output_folder / f"folder_{folder_count:03d}"
                    current_folder.mkdir(exist_ok=True)
                    print(f"Created: {current_folder.name}")
                
                file_path = current_folder / f"part_{file_count:05d}.txt"
                current_file = open(file_path, 'w', encoding='utf-8')
                print(f"  [{file_count}] {current_folder.name}/{file_path.name}")
            
            current_file.write(line)
            line_count += 1
            total_lines += 1
    
    if current_file:
        current_file.close()
    
    return file_count, folder_count, output_folder, total_lines


def split_file_by_separator(input_file, separator="="*80, output_folder=None, files_per_folder=100):
    input_path = Path(input_file)
    if not input_path.is_file():
        raise ValueError(f"Not a file: {input_file}")
    
    output_folder = Path(output_folder) if output_folder else input_path.parent / f"{input_path.stem}_split"
    output_folder.mkdir(exist_ok=True)
    
    print(f"Splitting by separator: {input_path.name}\n")
    
    file_count = folder_count = 0
    current_folder = current_content = None
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
        current_content = []
        for line in infile:
            if separator in line and current_content:
                file_count += 1
                
                if (file_count - 1) % files_per_folder == 0:
                    folder_count += 1
                    current_folder = output_folder / f"folder_{folder_count:03d}"
                    current_folder.mkdir(exist_ok=True)
                    print(f"Created: {current_folder.name}")
                
                file_path = current_folder / f"part_{file_count:05d}.txt"
                file_path.write_text(''.join(current_content), encoding='utf-8')
                print(f"  [{file_count}] {current_folder.name}/{file_path.name}")
                current_content = []
            
            current_content.append(line)
        
        if current_content:
            file_count += 1
            if (file_count - 1) % files_per_folder == 0:
                folder_count += 1
                current_folder = output_folder / f"folder_{folder_count:03d}"
                current_folder.mkdir(exist_ok=True)
                print(f"Created: {current_folder.name}")
            
            file_path = current_folder / f"part_{file_count:05d}.txt"
            file_path.write_text(''.join(current_content), encoding='utf-8')
            print(f"  [{file_count}] {current_folder.name}/{file_path.name}")
    
    return file_count, folder_count, output_folder


def split_merged_docs(input_file, separator="="*80, output_folder=None):
    import re
    
    input_path = Path(input_file)
    if not input_path.is_file():
        raise ValueError(f"Not a file: {input_file}")
    
    output_folder = Path(output_folder) if output_folder else input_path.parent / "split_docs"
    output_folder.mkdir(exist_ok=True)
    
    print(f"Splitting merged docs: {input_path.name}\n")
    
    file_count = 0
    current_content = []
    current_file_info = None
    
    # Pattern to match: "File X/Y: folder\filename.md"
    pattern = re.compile(r'File\s+\d+/\d+:\s+(.+)$')
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
        line_iter = iter(infile)
        for line in line_iter:
            # Check if this is a separator line followed by file info
            if separator in line:
                next_line = next(line_iter, None)
                if next_line is None:
                    break

                match = pattern.search(next_line.strip())
                if match:
                    # Save previous file if exists
                    if current_file_info and current_content:
                        save_file(output_folder, current_file_info, current_content, file_count)
                        file_count += 1

                    # Parse new file info
                    file_path_str = match.group(1).strip()
                    current_file_info = file_path_str
                    current_content = []

                    # Skip the next separator line if present
                    _ = next(line_iter, None)
                    continue

                # Not a file marker: keep separator and next line as regular content
                if current_file_info:
                    current_content.append(line)
                    current_content.append(next_line)
                continue

            # Add content (skip separator lines)
            if current_file_info:
                current_content.append(line)
        
        # Save last file
        if current_file_info and current_content:
            save_file(output_folder, current_file_info, current_content, file_count)
            file_count += 1
    
    print(f"\n✓ Created {file_count} files in: {output_folder}")
    return file_count, output_folder


def save_file(base_folder, file_path_str, content, count):
    """Save content to the appropriate folder and filename"""
    # Parse path like "java - en\doc_001.md"
    if '\\' in file_path_str:
        parts = file_path_str.split('\\')
    elif '/' in file_path_str:
        parts = file_path_str.split('/')
    else:
        parts = [file_path_str]
    
    # Create folder structure
    if len(parts) > 1:
        folder_name = parts[0].strip()
        file_name = parts[-1].strip()
        target_folder = base_folder / folder_name
    else:
        file_name = parts[0].strip()
        target_folder = base_folder
    
    target_folder.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_path = target_folder / file_name
    file_path.write_text(''.join(content), encoding='utf-8')
    print(f"  [{count + 1}] {target_folder.name}/{file_name}")


def main(input_file):
    # Set default values - CONFIGURE THESE:
    if not input_file:
        input_file = r"D:\New folder\study-every-thing\a.txt"
    
    output_folder = Path(__file__).parent / "split_docs"
    use_merged_docs_splitter = True  # Set to True to split merged docs with folder/filename extraction
    
    # For regular splitting:
    files_per_folder = 100
    lines_per_file = 1000
    use_separator = False
    
    if not input_file:
        print("Error: input_file is not set. Please set the input_file variable in the main() function.")
        return
    
    try:
        if use_merged_docs_splitter:
            count, output_path = split_merged_docs(input_file, output_folder=output_folder)
            print(f"\n✓ Split into {count} files: {output_path}")
        elif use_separator:
            count, folders, output_path = split_file_by_separator(input_file, output_folder=output_folder, files_per_folder=files_per_folder)
            print(f"\n✓ Created {count} files in {folders} folder(s): {output_path}")
        else:
            count, folders, output_path, total_lines = split_file_by_lines(input_file, output_folder, files_per_folder, lines_per_file)
            print(f"\n✓ Split {total_lines:,} lines into {count} files in {folders} folder(s): {output_path}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main("")