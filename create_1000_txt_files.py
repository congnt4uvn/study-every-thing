import pathlib

folder = pathlib.Path('files_txt')
folder.mkdir(parents=True, exist_ok=True)
for i in range(1, 1000):
    path = folder / f"{i:03}.txt"
    path.write_text("")  # create empty file
