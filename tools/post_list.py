import requests

def post_list(site_url, token):
    url = f'{site_url}/wp-json/wp/v2/posts'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        posts = response.json()

        # Filter to return only id and title
        filtered_posts = [{"id": post["id"], "title": post["title"]["rendered"]} for post in posts]
        return filtered_posts

    except requests.exceptions.RequestException as e:
        # Check if response is available, otherwise handle the exception
        if response is not None:
            status_code = response.status_code
            error_message = response.text
        else:
            status_code = None
            error_message = str(e)
        
        raise Exception(f"Error: {error_message} (Status code: {status_code})")