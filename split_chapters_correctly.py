import re
import os

# Define the input file and output directory
source_file = '/Users/ajing/Documents/git_repos/story_of_stone/raw.txt'
output_dir = '/Users/ajing/Documents/git_repos/story_of_stone/chapters'

# Ensure the output directory exists and is empty
if os.path.exists(output_dir):
    for f in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, f))
else:
    os.makedirs(output_dir)

# Read the entire content of the source file
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# This pattern finds chapter titles that start at the beginning of a line
pattern = re.compile(r'^第[\u4e00-\u9fa5]+回\s.*$', re.MULTILINE)

# Find all chapter titles and their start/end positions
matches = list(pattern.finditer(content))

if not matches:
    print("No chapters found. Please check the pattern.")
else:
    # Iterate through the matches to extract content for each chapter
    for i, match in enumerate(matches):
        # The start of the current chapter's content is the start of its title
        start_pos = match.start()

        # The end of the chapter's content is the start of the next chapter's title
        # If it's the last chapter, the end is the end of the file
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)

        # Extract the full chapter content
        chapter_full_content = content[start_pos:end_pos].strip()

        # The title is the first line of the chapter content
        chapter_title = chapter_full_content.splitlines()[0].strip()
        
        # Sanitize the title to create a valid filename
        # Replace spaces and special characters
        safe_title = re.sub(r'[\s\\/:"*?<>|]+', '_', chapter_title)
        
        # Format the filename with a chapter number
        filename = f"{i+1:03d}_{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)

        # Write the chapter content to the new file
        try:
            with open(filepath, 'w', encoding='utf-8') as chapter_file:
                chapter_file.write(chapter_full_content)
            print(f"Created file: {filename}")
        except OSError as e:
            print(f"Error creating file {filename}: {e}")

print(f"Successfully split the book into {len(matches)} chapters.")
