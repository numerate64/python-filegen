# Python File Generator

This project contains a Python script to generate a specified number of folders, each with a specified number of text files of random sizes between 4KB and 128KB. Each folder and file has a random name, and files are filled with random data.

## Usage

1. Make sure you have Python 3.7+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python generate_random_files.py
   ```
   You can optionally specify parameters:
   ```bash
   python generate_random_files.py --folders 10 --files-per-folder 10 --min-kb 4 --max-kb 128 --parallelism 64
   ```
   - `--folders`: Number of folders to create (default: 10)
   - `--files-per-folder`: Files per folder (default: 10)
   - `--min-kb`: Minimum file size in KB (default: 4)
   - `--max-kb`: Maximum file size in KB (default: 128)
   - `--parallelism`: Number of parallel folder jobs (default: 64)
   - `--help`, `-h`: Show help/usage information
4. The generated folders and files will be in the `files` directory.

## Help / Usage

You can view usage information at any time:
```bash
python generate_random_files.py --help
```

## Output Details

- A progress bar shows the folder creation progress in real time.
- As the script runs, it prints a colored message for each folder when it completes, and any errors encountered are displayed in red.
  ```
  [FolderName] Completed: 10 files (added 3), 12.19 MB written. Errors: 0
  Error writing /path/to/file.txt: [error details]
  ```
- At the end, a summary is displayed:
  ```
  Summary:
    Total folders: 10
    Total files: 100
    Total size: 1.19 GB (1219.92 MB)
    Time elapsed: 2.92 seconds
    Total errors: 0
  Done!
  ```
- Output from folders may appear in any order due to parallel execution.
- All output is cross-platform and colorized for clarity.

## Resumable Runs

- The script is fully resumable. If interrupted or re-run, it will:
  - Reuse previously generated folder names.
  - Skip folders that already exist and have the required number of files.
  - Only create missing files in incomplete folders.
  - No duplicate folders or files will be created if parameters are unchanged.
- This allows you to safely interrupt and resume large jobs without wasting time or disk space.

## Requirements
- Python 3.7 or later
- tqdm, colorama (see requirements.txt)

## Notes
- This script uses multi-threading for faster execution. The default is 64 parallel jobs, which is suitable for high-core-count systems. Adjust the `--parallelism` parameter based on your system's CPU and memory. Using too many threads on a low-resource machine may slow down execution or cause errors.
- The script may take significant time and disk space due to the large number and size of files generated. Adjust parameters as needed to fit your system's capabilities.
- Errors encountered during folder or file creation are reported, but the script will continue processing other folders/files.
