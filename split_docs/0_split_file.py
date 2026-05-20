
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


def main(input_file):
    # Set default values
    output_folder = Path(__file__).parent  # Same folder as this Python script
    files_per_folder = 100
    lines_per_file = 1000
    use_separator = False
    
    if not input_file:
        print("Error: input_file is not set. Please set the input_file variable in the main() function.")
        return
    
    try:
        if use_separator:
            count, folders, output_path = split_file_by_separator(input_file, output_folder=output_folder, files_per_folder=files_per_folder)
            print(f"\n✓ Created {count} files in {folders} folder(s): {output_path}")
        else:
            count, folders, output_path, total_lines = split_file_by_lines(input_file, output_folder, files_per_folder, lines_per_file)
            print(f"\n✓ Split {total_lines:,} lines into {count} files in {folders} folder(s): {output_path}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main("")

