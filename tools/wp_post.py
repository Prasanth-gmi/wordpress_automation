from crewai_tools import tool
import requests
import sys

class WordPress:
    def __init__(self, site_url, token):
        self.site_url = site_url
        self.token = token
    
    def get_categories(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f'{self.site_url}/wp-json/wp/v2/categories', headers=headers)
        return response.json() if response.status_code == 200 else []

    def get_tags(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f'{self.site_url}/wp-json/wp/v2/tags', headers=headers)
        return response.json() if response.status_code == 200 else []

    def create_category(self, name):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        data = {'name': name}
        response = requests.post(f'{self.site_url}/wp-json/wp/v2/categories', headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 400 and 'term_exists' in response.text:
            return {'id': response.json().get('data', {}).get('term_id')}
        else:
            return None

    def create_tag(self, name):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        data = {'name': name}
        response = requests.post(f'{self.site_url}/wp-json/wp/v2/tags', headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 400 and 'term_exists' in response.text:
            return {'id': response.json().get('data', {}).get('term_id')}
        else:
            return None

    def wp_post(self, topic, content, categories, tags):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        post_data = {
            'title': topic,
            'content': content,
            'status': 'draft',
            'categories': categories,
            'tags': tags
        }
        response = requests.post(f'{self.site_url}/wp-json/wp/v2/posts', headers=headers, json=post_data)
        return response.json() if response.status_code == 201 else None

def get_or_create_term(wp, name, existing_terms, create_func):
    # Check if the term (category or tag) already exists
    for term in existing_terms:
        if term['name'].lower() == name.lower():
            return term['id']
    
    # If it doesn't exist, create it
    new_term = create_func(name)
    if new_term and 'id' in new_term:
        return new_term['id']
    elif new_term and 'code' in new_term and new_term['code'] == 'term_exists':
        # If the term already exists but wasn't caught in the initial check, use the existing one
        return new_term['id']
    else:
        raise ValueError(f"Failed to create or retrieve the term '{name}'")

@tool
def wordpress_post(topic: str, contents:str, category: str, tags: list, site_url: str, token: str):
    """
    Post content to a WordPress site with a single category and multiple tags related to the topic. remove all .md file format in the content add well look and feel bootstrap design. this design cover to all users.
    
    Args:
    topic (str): The topic name should be the same as the topic name from ./main.py
    category (str): Give category value related to topic name within 26 characters only. category value should be all lowercase.
    tags (list): Provide a list of tag values, each within 26 characters. tags value should be all lowercase.
    site_url (str): The site_url should be same as the site_url from ./main.py. Don't add extra content.
    token (str): The token should be the same as the token from ./main.py. Don't add extra content.
    """
    with open('./styled_markdown.html', 'r') as file:
        file_contents = file.read()
    lines = file_contents.split('\n')
    contents = '\n'.join(lines[1:])
    
    wp = WordPress(site_url, token)
    
    # Get existing categories and tags
    existing_categories = wp.get_categories()
    existing_tags = wp.get_tags()
    
    # Get or create category
    try:
        category_ids = [get_or_create_term(wp, category, existing_categories, wp.create_category)]
    except ValueError as e:
        print(e)
        return
    
    # Process each tag separately and create them in WordPress if they don't exist
    tag_ids = []
    for tag in tags:
        try:
            tag_id = get_or_create_term(wp, tag, existing_tags, wp.create_tag)
            tag_ids.append(tag_id)
        except ValueError as e:
            print(e)
            return
    
    # Create the post with the category and the list of tag IDs
    response = wp.wp_post(topic, contents, category_ids, tag_ids)
    
    if response:
        print(f'Post Created: {response}')
        print(f'Category used: {category}')
        print(f'Tags used: {tags}')
    else:
        print("Failed to create the post.")
    sys.exit()
