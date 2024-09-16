from crewai_tools import BaseTool, tool
import os
import re
import shutil  # Import for zipping functionality

class MarkdownProcessor:
    def __init__(self, file_path, folder_name):
        self.file_path = file_path
        self.main_folder = folder_name
        self.sub_files = [
            'header.php',
            'index.php',
            'footer.php',
            'style.css',
            'functions.php',
            'theme.json'
        ]
        self.file_patterns = {file: re.compile(
            rf'\*\*{file}\*\*|'
            rf'\*{file}\*|'
            rf'\*\*{file}:?\*\*|'
            rf'\*{file}:?\*|'
            rf'##{file}##|'
            rf'#{file}#|'
            rf'##{file}|'
            rf'#{file}'
        ) for file in self.sub_files}
    
    def read_content(self):
        with open(self.file_path, 'r', encoding='utf-8') as md_file:
            return md_file.read()

    def clean_content(self, file_name, content):
        if file_name == 'theme.json':
            # Remove backtick code block markers and any trailing content after the JSON object
            content = re.sub(r'^```json', '', content, flags=re.MULTILINE).strip()
            content = re.sub(r'```$', '', content, flags=re.MULTILINE).strip()
            # Ensure content ends properly after the last closing curly brace
            content = re.sub(r'^(.*\{.*\}.*?)(\n.*)?$', r'\1', content, flags=re.DOTALL).strip()
        else:
            # General content cleaning (e.g., remove backticks)
            start_marker_pattern = r'```[\w]*'  # Marker at the start of the content (e.g., ```json)
            end_marker_pattern = r'```'        # Marker at the end of the content

            # Remove content between start and end markers
            content = re.sub(rf'^{start_marker_pattern}\s*', '', content, flags=re.MULTILINE).strip()
            content = re.sub(rf'\s*{end_marker_pattern}$', '', content, flags=re.MULTILINE).strip()

            # Ensure content ends properly after the last backtick block
            last_backtick_index = content.rfind('```')
            if last_backtick_index != -1:
                content = content[:last_backtick_index].strip()

        return content

    def extract_file_content(self, file_name, content):
        pattern = self.file_patterns[file_name]
        matches = list(pattern.finditer(content))
        
        if matches:
            start_index = matches[0].end()
            next_start_index = len(content)
            for other_file in self.sub_files:
                if other_file != file_name:
                    other_pattern = self.file_patterns[other_file]
                    other_match = other_pattern.search(content, start_index)
                    if other_match:
                        next_start_index = min(next_start_index, other_match.start())
            
            file_content = content[start_index:next_start_index].strip()
            return self.clean_content(file_name, file_content)
        return ''

    def write_files(self):
        if not os.path.exists(self.main_folder):
            os.makedirs(self.main_folder)

        content = self.read_content()
        for file_name in self.sub_files:
            file_content = self.extract_file_content(file_name, content)
            if file_content:
                file_path = os.path.join(self.main_folder, file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(file_content)
                print(f"Content for '{file_name}' has been written to '{file_path}'")
        
        # Create a ZIP file of the theme folder
        zip_file_path = f"{self.main_folder}.zip"
        shutil.make_archive(self.main_folder, 'zip', self.main_folder)
        print(f"ZIP file '{zip_file_path}' has been created.")

        return f"Theme folder '{self.main_folder}' and its sub-files have been created and populated with content, and the folder has been zipped."

@tool
def markdown_to_files(file_path: str, folder_name: str):
    """
    Convert content from a Markdown file into specific theme files and create a ZIP archive of the theme folder.
    
    Args:
    file_path (str): Path to the Markdown file containing content to be extracted and written.
    folder_name (str): Name of the main folder where the theme files will be created.
    """
    processor = MarkdownProcessor(file_path, folder_name)
    result = processor.write_files()
    print(result)
