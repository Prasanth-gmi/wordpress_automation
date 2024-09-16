import requests

def page_list(site_url, token):
    url = f'{site_url}/wp-json/wp/v2/pages'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        pages = response.json()

        # Filter to return only id and title
        filtered_pages = [{"id": page["id"], "title": page["title"]["rendered"]} for page in pages]
        return filtered_pages

    except requests.exceptions.RequestException as e:
        # If the response is available, use its status_code and text, otherwise use the exception's message
        status_code = response.status_code if response else 500
        error_message = response.text if response else str(e)
        raise Exception(f"Error: {error_message} (Status code: {status_code})")