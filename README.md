# Python Based File Cleaner

A command-line tool written in Python to scan directories and classify files based on configurable rules, helping identify which files should be deleted and which should be retained.

## Overview

Python Based File Cleaner scans a given directory structure and evaluates files using criteria such as file type, size, age, and scan depth. The tool can perform a dry run to preview deletions before actually removing files, making it safe to use for cleanup tasks.

The project is designed to be modular and extensible, allowing additional rules or smarter classification logic to be added later.

## Features

- Scan directories at configurable depth levels
- Filter files by type (image, document, python, etc.)
- Filter files by size thresholds
- Filter files by age
- Dry-run mode to preview deletions
- CLI-based interface suitable for automation and scripting

## Requirements

- Python 3.10 or newer
- Standard Python library only

## Installation

Clone the repository:

```
git clone https://github.com/Subhams-GIT/python-based-file-cleaner-.git
cd python-based-file-cleaner-
```

(Optional) Create a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install in editable mode:

```
pip install -e .
```

Alternatively, for system-wide CLI usage, install using pipx:

```
pipx install -e .
```

## Usage

Run the tool from the command line:

```
filecleanup --foldername PATH [options]
```

Or run as a module:

```
python -m filecleanup.main
```

## Command Line Arguments

| Argument | Description |
|--------|-------------|
| `--foldername` | Directory to scan (default: current directory) |
| `--mimetype` | File category to filter (image, doc, python, or None) |
| `--depth` | Scan depth (1 or 2) |
| `--lgt` | Minimum file size in bytes |
| `--smt` | Maximum file size in bytes |
| `--ot` | Minimum file age in seconds |
| `--drymode` | Preview deletions without removing files |

## Examples

Dry run for Python files up to two levels deep:

```
filecleanup --mimetype python --depth 2 --drymode
```

Delete image files larger than 1MB and older than 7 days:

```
filecleanup   --foldername /path/to/images   --mimetype image   --lgt 1000000   --ot 604800
```

## Notes

- Dry mode is strongly recommended before actual deletion.
- The tool respects basic ignore patterns and avoids unsafe deletions when configured correctly.

## License

This project is open source. Refer to the repository for license details.