import os
import re

def cleanup_chapters():
    """
    Cleans up the chapters directory by removing duplicate and malformed files,
    and renames the remaining files to have sequential chapter numbers.
    """
    chapters_dir = '/Users/ajing/Documents/git_repos/story_of_stone/chapters'
    try:
        files = os.listdir(chapters_dir)
    except FileNotFoundError:
        print(f"Error: Directory not found at {chapters_dir}")
        return
        
    files.sort()

    unique_chapters = {}
    files_to_delete = []
    
    # Regex to match the standard chapter file format, e.g., "001_title.txt"
    chapter_pattern = re.compile(r'^\d{3}_(.*)\.txt$')
    # Regex to match malformed files that should be deleted
    malformed_pattern = re.compile(r'^\d{3,}_\D+.*\.txt$')


    for filename in files:
        # Ignore non-text files
        if not filename.endswith('.txt'):
            continue

        match = chapter_pattern.match(filename)
        if match:
            title = match.group(1)
            if title not in unique_chapters:
                # Store the first occurrence of a chapter title
                unique_chapters[title] = filename
            else:
                # If title is already seen, this is a duplicate
                files_to_delete.append(filename)
        else:
            # If the filename does not match the standard chapter format, delete it
            files_to_delete.append(filename)

    # Sort the unique chapters by their original file number to maintain order
    sorted_unique_files = sorted(unique_chapters.values(), key=lambda f: int(f.split('_')[0]))

    # Rename the unique files sequentially
    for i, filename in enumerate(sorted_unique_files):
        new_number = i + 1
        # Reconstruct the title part of the filename
        title = '_'.join(filename.split('_')[1:])
        new_filename = f"{new_number:03d}_{title}"
        
        old_path = os.path.join(chapters_dir, filename)
        new_path = os.path.join(chapters_dir, new_filename)

        if old_path != new_path:
            print(f"Renaming '{filename}' to '{new_filename}'")
            os.rename(old_path, new_path)

    # Delete all identified duplicate and malformed files
    for filename in files_to_delete:
        path_to_delete = os.path.join(chapters_dir, filename)
        print(f"Deleting '{filename}'")
        try:
            os.remove(path_to_delete)
        except OSError as e:
            print(f"Error deleting file {filename}: {e}")

if __name__ == '__main__':
    cleanup_chapters()
    print("Cleanup complete.")
