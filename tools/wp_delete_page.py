from crewai_tools import tool
import requests
import sys

class WordPressPage:
    def __init__(self, site_url, token):
        """
        Initialize the WordPressPage class with site URL and JWT token.

        Args:
        site_url (str): The URL of the WordPress site.
        token (str): The JWT token for authentication.
        """
        self.site_url = site_url
        self.token = token
    
    def delete_page(self, page_id):
        """
        Delete a page from a WordPress site using its ID.

        Args:
        page_id (int): The ID of the page to be deleted.
        
        Returns:
        dict: The response from the WordPress API.
        """
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.delete(f'{self.site_url}/wp-json/wp/v2/pages/{page_id}', headers=headers)
        return response.json()

@tool
def wordpress_delete_page(page_id: int, site_url: str, token: str):
    """
    Delete a page from a WordPress site using its ID.

    Args:
    page_id (int): The ID of the page to be deleted.
    site_url (str): The URL of the WordPress site.
    token (str): The JWT token for authentication.
    """
    wp = WordPressPage(site_url, token)
    
    # Delete the page
    response = wp.delete_page(page_id)
    
    print(f'Page Deleted: {response}')
    sys.exit()