import os
import random
import string
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import init, Fore, Style
import sys

# --- Argument Parsing ---
def parse_args():
    parser = argparse.ArgumentParser(description="Generate random folders and files of varying sizes.")
    parser.add_argument('--folders', type=int, default=10, help='Number of folders to create (default: 10)')
    parser.add_argument('--files-per-folder', type=int, default=10, help='Files per folder (default: 10)')
    parser.add_argument('--min-kb', type=int, default=4, help='Minimum file size in KB (default: 4)')
    parser.add_argument('--max-kb', type=int, default=128, help='Maximum file size in KB (default: 128)')
    parser.add_argument('--parallelism', type=int, default=64, help='Number of parallel folder jobs (default: 64)')
    return parser.parse_args()

# --- Helpers ---
def random_string(length=12):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_file(file_path, min_kb, max_kb):
    size_kb = random.randint(min_kb, max_kb)
    try:
        with open(file_path, 'wb') as f:
            f.write(os.urandom(size_kb * 1024))
        return size_kb * 1024, None
    except Exception as e:
        return 0, f"Error writing {file_path}: {e}"

def generate_folder(base_path, files_per_folder, min_kb, max_kb, folder_name=None, progress=None):
    if folder_name is None:
        folder_name = random_string(12)
    folder_path = os.path.join(base_path, folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        if progress:
            progress.write(f"{Fore.RED}Error creating folder {folder_path}: {e}{Style.RESET_ALL}")
        return 0, 0, 1
    existing_files = set(os.listdir(folder_path)) if os.path.exists(folder_path) else set()
    files_needed = files_per_folder - len(existing_files)
    total_bytes = 0
    error_count = 0
    for i in range(files_needed):
        file_name = random_string(10) + '.txt'
        while file_name in existing_files:
            file_name = random_string(10) + '.txt'
        file_path = os.path.join(folder_path, file_name)
        bytes_written, err = generate_file(file_path, min_kb, max_kb)
        total_bytes += bytes_written
        if err:
            error_count += 1
            if progress:
                progress.write(f"{Fore.RED}{err}{Style.RESET_ALL}")
        existing_files.add(file_name)
    if progress:
        progress.write(f"{Fore.GREEN}[{folder_name}] Completed: {files_per_folder} files (added {files_needed}), {round(total_bytes / (1024*1024), 2)} MB written. Errors: {error_count}{Style.RESET_ALL}")
    return files_per_folder, total_bytes, error_count

# --- Main ---
def main():
    init(autoreset=True)  # colorama
    args = parse_args()
    if '-h' in sys.argv or '--help' in sys.argv:
        print("""
Python File Generator

Usage:
  python generate_random_files.py [--folders <int>] [--files-per-folder <int>] [--min-kb <int>] [--max-kb <int>] [--parallelism <int>] [--help|-h]

Parameters:
  --folders           Number of folders to create (default: 10)
  --files-per-folder  Files per folder (default: 10)
  --min-kb            Minimum file size in KB (default: 4)
  --max-kb            Maximum file size in KB (default: 128)
  --parallelism       Number of parallel folder jobs (default: 64)
  --help, -h          Show this help message
""")
        sys.exit(0)
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
    try:
        os.makedirs(base_path, exist_ok=True)
    except Exception as e:
        print(f"{Fore.RED}Error creating base directory: {e}{Style.RESET_ALL}")
        sys.exit(1)

    # Gather or create folder names for resumability
    folder_names = set()
    if os.path.exists(base_path):
        folder_names.update([name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))])
    while len(folder_names) < args.folders:
        folder_names.add(random_string(12))
    folder_names = list(folder_names)[:args.folders]

    print(f"Starting (resumable) generation of {args.folders} folders, each with {args.files_per_folder} files (sizes: {args.min_kb} KB to {args.max_kb} KB) using {args.parallelism} parallel jobs...")
    start = time.time()
    results = []
    errors = 0
    with ThreadPoolExecutor(max_workers=args.parallelism) as executor:
        with tqdm(total=args.folders, desc="Folders", unit="folder") as progress:
            futures = [executor.submit(generate_folder, base_path, args.files_per_folder, args.min_kb, args.max_kb, folder_name, progress) for folder_name in folder_names]
            for future in as_completed(futures):
                files, bytes_written, error_count = future.result()
                results.append((files, bytes_written))
                errors += error_count
                progress.update(1)
    end = time.time()

    total_files = sum(r[0] for r in results)
    total_bytes = sum(r[1] for r in results)
    print(f"\n{Fore.CYAN}Summary:{Style.RESET_ALL}")
    print(f"  Total folders: {args.folders}")
    print(f"  Total files: {total_files}")
    print(f"  Total size: {round(total_bytes / (1024*1024*1024), 2)} GB ({round(total_bytes / (1024*1024), 2)} MB)")
    print(f"  Time elapsed: {round(end-start, 2)} seconds")
    if errors:
        print(f"{Fore.RED}  Total errors: {errors}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
