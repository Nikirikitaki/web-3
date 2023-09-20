import sys
import zipfile
import tarfile
import gzip
import shutil
from pathlib import Path
CATEGORIES ={"Image":[".jpeg",".png",".jpg","svg"],
             "Video":[".avi",".mp4",".mov","mkv"],
             "Docs": [".docx", ".txt", ".pdf",".xlsx"],
             "Audio": [".mp3", ".ogg", ".wav", ".amr"],
             "Arhive": [".zip", ".gz", ".tar"]}
def get_categories(file:Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def move_file(file:Path, category:str, root_dir:Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_path = target_dir.joinpath(file.name)
    file.replace(new_path)

    
        
def remove_empty_folders(path: Path):
    deleted_folders = []
    for folder in path.glob('**/*'):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
            deleted_folders.append(folder)
    for folder in deleted_folders:
        print ( f"removed folder: {folder}")
                
def sort_folder(path:Path) -> None:
    # for item in path.iterdir():
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
 
def unzip_arkhive(path:Path):
    for element in path.glob('**/*'):
        if element.is_file():
            ext = element.suffix.lower()
            if ext in [".zip",".tar",".gz"]:
                archive_name = element.stem 
                shutil.unpack_archive(element, element.parent.joinpath(archive_name))   
     
                
def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    if not path.exists():
        return "Folder dos not exists"
    sort_folder(path)
    
    unzip_arkhive(path)
    
    remove_empty_folders(path)
    
    return "All Ok"
if __name__ == '__main__':
    
    main()
