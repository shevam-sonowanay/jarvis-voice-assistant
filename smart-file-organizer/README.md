# 🗂️ Smart File Organizer CLI

A lightweight Python command-line utility that automatically sorts messy folders (such as `Downloads`) into clean, categorized subfolders.

## ✨ Features
- **Automatic Categorization:** Sorts files into `Documents`, `Code`, `Images`, `Videos`, `Audio`, `Archives`, `Installers`, and `Others`.
- **Safe Dry-Run Preview (`--dry-run`):** Preview every file move before anything is touched on disk.
- **Duplicate Filename Protection:** Automatically renames duplicate files (`file_1.pdf`, `file_2.pdf`) instead of overwriting existing files.
- **Zero External Dependencies:** Built 100% with Python's standard library (`pathlib`, `shutil`, `argparse`).

## 🚀 How to Run

1. **Preview changes safely first (recommended):**
   ```bash
   python organizer.py --dry-run
   ```

2. **Organize your Downloads folder:**
   ```bash
   python organizer.py
   ```

3. **Organize any custom folder path:**
   ```bash
   python organizer.py "C:\Path\To\Your\Folder"
   ```
