import sys
import argparse
import zipfile
import tarfile
import gzip
import shutil
import threading
import multiprocessing
from pathlib import Path

CATEGORIES = {
    "Image": [".jpeg", ".png", ".jpg", "svg"],
    "Video": [".avi", ".mp4", ".mov", "mkv"],
    "Docs": [".docx", ".txt", ".pdf", ".xlsx"],
    "Audio": [".mp3", ".ogg", ".wav", ".amr"],
    "Arhive": [".zip", ".gz", ".tar"]
}


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def move_file(file: Path, category: str, root_dir: Path) -> None:
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
        print(f"removed folder: {folder}")


def sort_folder(path: Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)


def unzip_archive(path: Path):
    for element in path.glob('**/*'):
        if element.is_file():
            ext = element.suffix.lower()
            if ext in [".zip", ".tar", ".gz"]:
                archive_name = element.stem
                shutil.unpack_archive(element, element.parent.joinpath(archive_name))


def process_directory(path: Path):
    print(f"Processing started in {multiprocessing.current_process().name} for directory {path}")
    sort_folder(path)
    unzip_archive(path)
    remove_empty_folders(path)
    print(f"Processing finished in {multiprocessing.current_process().name}")


def main(args) -> str:
    path = Path(args.folder)

    if not path.exists():
        return "Folder does not exist"

    # Создаем два потока для обработки директории
    thread1 = threading.Thread(target=process_directory, args=(path,))
    thread2 = threading.Thread(target=process_directory, args=(path,))

    # Запускаем потоки
    thread1.start()
    thread1.join()
    
    thread2.start()
    thread2.join()
    #--------------------------------------------
     # Создаем два процесса для обработки директории
    process1 = multiprocessing.Process(target=process_directory, args=(path,))
    process2 = multiprocessing.Process(target=process_directory, args=(path,))

    # Запускаем процессы + Ожидаем завершения обоих процессов
    process1.start()
    process1.join()
    
    process2.start()
    process2.join()

    
    
    
    

    return "All Ok"



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort files and extract archives in a directory.')
    parser.add_argument('folder', type=str, help='Path to the folder to be sorted')
    args = parser.parse_args()
    
    result = main(args)
    print(result)