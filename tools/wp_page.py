from crewai_tools import tool
import requests
import json

import sys

class WordPressAPI:
    def __init__(self, site_url, token):
        self.site_url = site_url
        self.token = token

    def create_page(self, title, content, parent_id=None):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "title": title,
            "content": content,
            "status": 'draft',
        }
        
        if parent_id is not None:
            payload["parent"] = parent_id
        
        url = f"{self.site_url}/wp-json/wp/v2/pages"
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error creating page: {response.text}")

    def get_pages(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        
        url = f"{self.site_url}/wp-json/wp/v2/pages"
        pages = []
        page = 1
        
        while True:
            response = requests.get(f"{url}?page={page}&per_page=100&_fields=id,title", headers=headers)
            
            if response.status_code == 200:
                new_pages = response.json()
                if not new_pages:
                    break
                pages.extend(new_pages)
                page += 1
            elif response.status_code == 400:
                # We've reached beyond the last page, so we can stop
                break
            else:
                raise Exception(f"Error fetching pages: {response.text}")
        
        return pages

@tool
def create_wordpress_page(topic: str, site_url: str, token: str):
    """
    Create a new page on a WordPress site using the REST API.
    
    Args:
    topic (str): The topic name should be the same as the topic name from main.py
    site_url (str): The site_url should be same as the site_url from ./main.py. don't add extra content.
    token (str): The token should be the same as the token from ./main.py. don't add extra content.
    
    Returns:
    dict: A dictionary containing information about the created page, including its ID.
    
    Raises:
    Exception: If there's an error creating the page.
    """
    # WordPress site details

    # Initialize WordPress API
    wp_api =  WordPressAPI(site_url, token)

    # # List existing pages
    # try:
    #     existing_pages = wp_api.get_pages()
    #     print("\nExisting Pages (ID and Name):")
    #     print("------------------------------")
    #     for page in existing_pages:
    #         print(f"ID: {page['id']} - Name: {page['title']['rendered']}")
    #     print("------------------------------\n")
    # except Exception as e:
    #     print(f"Error fetching existing pages: {str(e)}")
    #     return {
    #         "success": False,
    #         "message": f"Error fetching existing pages: {str(e)}"
    #     }

    # # Get parent page ID from user
    # parent_id = input("Enter the parent page ID (press Enter for no parent): ")
    
    # # Convert parent_id to integer or None
    # parent_id = int(parent_id) if parent_id.strip() else None

    # Get page content
    try:
        with open('./styled_markdown.html', 'r') as file:
            file_contents = file.read()
        lines = file_contents.split('\n')
        contents = '\n'.join(lines[1:])
    except Exception as e:
        return {
            "success": False,
            "message": f"Error reading content file: {str(e)}"
        }

    try:
        # Create the page
        result = wp_api.create_page(topic, contents)   #parent_id
        return {
            "success": True,
            "message": f"Page created successfully. ID: {result['id']}",
            "page_id": result['id'],
            "page_url": result['link']
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating page: {str(e)}"
        }
    sys.exit()