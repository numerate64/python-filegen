# Python File Generator

Python utility for generating random folders and binary files for storage, copy, and performance testing.

## Files

- `generate_random_files.py` - concurrent file generator.
- `requirements.txt` - Python dependencies.

## Setup

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```sh
python generate_random_files.py --folders 10 --files-per-folder 10 --min-kb 4 --max-kb 128 --parallelism 64
```

The script creates or resumes a `files/` directory beside the script.
