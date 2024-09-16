from crewai_tools import tool
import re

@tool
def convert_md_to_html_file(markdown_file: str, output_html_file: str):
    """
    Convert a Markdown file to an HTML file by extracting the content between backticks and changing the file extension.
    
    Args:
    markdown_file (str): The name of the Markdown file to be converted.
    output_html_file (str): The name of the output HTML file where the content will be saved.
    
    Returns:
    str: A message indicating the success or failure of the operation.
    """
    try:
        # Read the content from the Markdown file
        with open(markdown_file, 'r', encoding='utf-8') as md_file:
            content = md_file.read()

        # Extract the content between backticks
        match = re.search(r'```(.*?)```', content, re.DOTALL)
        if match:
            extracted_content = match.group(1).strip()
        else:
            return "No content found between backticks in the Markdown file."

        # Save the extracted content to the new HTML file
        with open(output_html_file, 'w', encoding='utf-8') as html_file:
            html_file.write(extracted_content)

        return f"Markdown content between backticks successfully copied to {output_html_file}."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"