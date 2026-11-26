import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx", ".csv", ".md"},
    "Code": {".py", ".cpp", ".c", ".h", ".java", ".js", ".html", ".css", ".json"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov"},
    "Audio": {".mp3", ".wav", ".aac", ".flac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Installers": {".exe", ".msi", ".deb", ".apk"},
}


def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def get_unique_destination(dest_dir: Path, filename: str) -> Path:
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        new_candidate = dest_dir / f"{stem}_{counter}{suffix}"
        if not new_candidate.exists():
            return new_candidate
        counter += 1


def organize_folder(target_dir: Path, dry_run: bool = False) -> None:
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: '{target_dir}' is not a valid directory.")
        return

    moved_count = 0
    for item in target_dir.iterdir():
        if item.is_dir() or item.name.startswith("."):
            continue

        category = get_category(item.suffix)
        dest_folder = target_dir / category
        dest_path = get_unique_destination(dest_folder, item.name)

        if dry_run:
            print(f"[DRY RUN] Would move: {item.name} -> {category}/{dest_path.name}")
        else:
            dest_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_path))
            print(f"Moved: {item.name} -> {category}/{dest_path.name}")
        moved_count += 1

    action = "previewed" if dry_run else "organized"
    print(f"\nDone! {moved_count} file(s) {action}.")


def main():
    parser = argparse.ArgumentParser(
        description="Organize messy folders (like Downloads) into clean categories."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=str(Path.home() / "Downloads"),
        help="Path to the folder to organize (defaults to your Downloads folder)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without actually moving any files",
    )
    args = parser.parse_args()

    target = Path(args.folder).expanduser().resolve()
    print(f"Target folder: {target}\n")
    organize_folder(target, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
