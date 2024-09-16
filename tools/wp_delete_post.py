import requests
import sys
from crewai_tools import tool

class WordPressPost:
    def __init__(self, site_url, token):
        self.site_url = site_url
        self.token = token

    def get_post_by_title(self, title):
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'search': title, 'per_page': 100}  # Increase the per_page to get more results if available
        response = requests.get(f'{self.site_url}/wp-json/wp/v2/posts', headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch posts: {response.status_code}, {response.text}")
            return None
        
        posts = response.json()

        # Debugging: Print the response content
        print(f"Response from WordPress API: {posts}")

        # Find the post with the exact title match (case insensitive)
        for post in posts:
            if post['title']['rendered'].strip().lower() == title.strip().lower():
                return post

        return None

    def delete_post(self, post_id):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.delete(f'{self.site_url}/wp-json/wp/v2/posts/{post_id}', headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to delete post: {response.status_code}, {response.text}")
        return response.json()

@tool
def wordpress_delete_post_by_title(title: str, site_url: str, token: str):
    """
    Delete a post from a WordPress site using its title.
    
    Args:
    title (str): The title of the post to be deleted.
    site_url (str): The URL of the WordPress site.
    token (str): The JWT token for authentication.
    """
    wp = WordPressPost(site_url, token)
    
    # Get the post by title
    post = wp.get_post_by_title(title)
    
    if post:
        post_id = post['id']
        # Delete the post
        response = wp.delete_post(post_id)
        print(f'Post "{title}" Deleted: {response}')
    else:
        print(f'Post with title "{title}" not found.')
    
    sys.exit()
