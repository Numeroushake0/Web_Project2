import os
import shutil
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
import time  

def sort_files_by_extension(source_dir, target_dir="dist"):
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    def process_directory(directory):
        with ThreadPoolExecutor() as executor:
            for item in directory.iterdir():
                if item.is_dir():
                    executor.submit(process_directory, item)
                elif item.is_file():
                    executor.submit(copy_file, item, target_path)
    
    def copy_file(file, target_path):
        ext = file.suffix[1:] if file.suffix else "unknown"
        ext_dir = target_path / ext
        ext_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, ext_dir / file.name)
    
    process_directory(source_path)

def factorize_number(n):
    return [i for i in range(1, n + 1) if n % i == 0]

def factorize_sync(*numbers):
    return [factorize_number(n) for n in numbers]

def factorize_parallel(*numbers):
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        return list(executor.map(factorize_number, numbers))

if __name__ == "__main__":
    source_directory = "picture"
    target_directory = "dist"
    sort_files_by_extension(source_directory, target_directory)
    

    numbers = [128, 255, 99999, 10651060]
    
    start = time.time()  
    result_sync = factorize_sync(*numbers)
    print("Sync time:", time.time() - start)  
    
    start = time.time()  
    result_parallel = factorize_parallel(*numbers)
    print("Parallel time:", time.time() - start)  
    
    assert result_sync == result_parallel
