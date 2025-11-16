import re
import os

file_path = '/Users/ajing/Documents/git_repos/story_of_stone/433.txt'
output_dir = '/Users/ajing/Documents/git_repos/story_of_stone/chapters'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all chapter titles and their start positions
    pattern = re.compile(r'^(第[\u4e00-\u9fa5]+回.*)', re.MULTILINE)
    matches = list(pattern.finditer(content))

    for i, match in enumerate(matches):
        chapter_title = match.group(1).strip()
        start_pos = match.start()
        
        # The end position is the start of the next chapter, or the end of the file
        end_pos = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        chapter_content = content[start_pos:end_pos].strip()
        
        # Create a clean filename from the chapter title
        clean_title = chapter_title.replace('\u3000', ' ').strip()
        title_match = re.match(r'第.*?回\s+(.*)', clean_title)
        
        if title_match:
            filename_title = title_match.group(1).replace(' ', '_')
        else:
            # Fallback if title format is unexpected
            filename_title = f"chapter_{i+1}"
            
        # Sanitize filename to remove invalid characters
        filename_title = re.sub(r'[\\/*?:"<>|]', "", filename_title)
        
        filename = f"{i+1:03d}_{filename_title}.txt"
        
        full_output_path = os.path.join(output_dir, filename)
        
        with open(full_output_path, 'w', encoding='utf-8') as f:
            f.write(chapter_content)
            
        print(f"Created file: {filename}")

except FileNotFoundError:
    print(f"Error: The file was not found at {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
