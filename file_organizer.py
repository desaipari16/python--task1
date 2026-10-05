import os
import shutil
import logging
import argparse

# --------------------------------
# File Categories
# --------------------------------

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],

    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".csv", ".pptx"],

    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],

    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],

    "Code": [".py", ".java", ".html", ".css", ".js", ".cpp", ".c", ".php"],

    "Others": []
}


# --------------------------------
# Logging Configuration
# --------------------------------

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# --------------------------------
# Get File Category
# --------------------------------

def get_category(filename):

    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            return category

    return "Others"


# --------------------------------
# Handle Duplicate Files
# --------------------------------

def get_unique_filename(destination):

    if not os.path.exists(destination):
        return destination

    folder = os.path.dirname(destination)

    filename = os.path.basename(destination)

    name, extension = os.path.splitext(filename)

    counter = 1

    while True:

        new_filename = f"{name}_{counter}{extension}"

        new_destination = os.path.join(
            folder, new_filename
        )

        if not os.path.exists(new_destination):
            return new_destination

        counter += 1


# --------------------------------
# Organize Files
# --------------------------------

def organize_files(source, dry_run=False):

    if not os.path.isdir(source):
        print("Error: Source directory does not exist.")
        return

    moved = 0
    skipped = 0
    planned_destinations = set()

    print("\n========== FILE ORGANIZER ==========")

    for filename in os.listdir(source):

        source_path = os.path.join(source, filename)

        # Skip hidden files and folders
        if filename.startswith("."):
            skipped += 1
            continue

        # Skip directories and symbolic links
        if not os.path.isfile(source_path):
            skipped += 1
            continue

        # Identify category
        category = get_category(filename)

        # Create category folder path
        category_folder = os.path.join(source, category)

        destination = os.path.join(
            category_folder, filename
        )

        # Handle duplicate filenames
        while (
            os.path.exists(destination)
            or destination in planned_destinations
        ):
            folder = os.path.dirname(destination)
            name, extension = os.path.splitext(
                os.path.basename(destination)
            )

            counter = 1

            while True:
                new_name = f"{name}_{counter}{extension}"
                new_destination = os.path.join(
                    folder, new_name
                )

                if (
                    not os.path.exists(new_destination)
                    and new_destination not in planned_destinations
                ):
                    destination = new_destination
                    break

                counter += 1

            break

        planned_destinations.add(destination)

        if dry_run:

            print(
                f"[PREVIEW] {filename} -> {category}/"
                f"{os.path.basename(destination)}"
            )

            moved += 1

        else:

            try:

                # Create folder if it does not exist
                os.makedirs(category_folder, exist_ok=True)

                # Move file
                shutil.move(source_path, destination)

                print(
                    f"[MOVED] {filename} -> {category}/"
                    f"{os.path.basename(destination)}"
                )

                logging.info(
                    f"Moved {filename} to {destination}"
                )

                moved += 1

            except OSError as error:

                print(f"Error moving {filename}: {error}")

                logging.error(
                    f"Failed to move {filename}: {error}"
                )

                skipped += 1

    # --------------------------------
    # Summary Report
    # --------------------------------

    print("\n========== SUMMARY REPORT ==========")

    print(f"Files organized : {moved}")
    print(f"Files skipped   : {skipped}")

    if dry_run:
        print("\nDry-run completed. No files were moved.")
    else:
        print("\nFile organization completed successfully.")

    print("Log file: organizer.log")
    print("====================================")


# --------------------------------
# Main Function
# --------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Automatic File Organizer"
    )

    parser.add_argument(
        "source",
        help="Path of the directory to organize"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files"
    )

    args = parser.parse_args()

    organize_files(
        args.source,
        args.dry_run
    )


# --------------------------------
# Start Program
# --------------------------------

if __name__ == "__main__":
    main()