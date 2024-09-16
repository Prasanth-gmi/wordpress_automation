from crewai_tools import tool
import requests
import sys

class WordPress:
    def __init__(self, site_url, username, password):
        self.site_url = site_url
        self.token = self.get_token(username, password)
    
    def get_token(self, username, password):
        response = requests.post(f'{self.site_url}/wp-json/jwt-auth/v1/token', data={
            'username': username,
            'password': password
        })
        token = response.json().get('token')
        if not token:
            raise ValueError("Failed to obtain authentication token")
        return token
    
    def wp_user(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        username = input("Enter Username: ")
        name = input("Enter Name: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        roles = input("Enter Role (e.g. subscriber, author, editor, administrator): ")
        user_data = {
            'username': username,
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'roles': [roles],
        }
        response = requests.post(f'{self.site_url}/wp-json/wp/v2/users', headers=headers, json=user_data)
        return response.json()

    def update_user(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        user_id = input("Enter User ID to update: ")
        print("Enter new details (leave blank to keep current value):")
        name = input("Enter Name: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        roles = input("Enter Role (e.g. subscriber, author, editor, administrator): ")
        
        user_data = {}
        if name: user_data['name'] = name
        if first_name: user_data['first_name'] = first_name
        if last_name: user_data['last_name'] = last_name
        if email: user_data['email'] = email
        if password: user_data['password'] = password
        if roles: user_data['roles'] = [roles]

        response = requests.post(f'{self.site_url}/wp-json/wp/v2/users/{user_id}', headers=headers, json=user_data)
        return response.json()

    def delete_user(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        user_id = input("Enter User ID to delete: ")
        reassign = input("Enter User ID to reassign content to (or leave blank): ")
        
        params = {'force': True}
        if reassign:
            params['reassign'] = reassign

        response = requests.delete(f'{self.site_url}/wp-json/wp/v2/users/{user_id}', headers=headers, params=params)
        return response.json() if response.content else {'status': 'User deleted successfully'}

@tool
def wordpress_user_management():
    """
    Manage WordPress users: Create, Update, or Delete a user.
    """
    site_url = 'http://localhost:80/wordpress/'
    username = 'root'
    password = 'Su6yalun@'
    wp = WordPress(site_url, username, password)
    
    action = input("Choose action (create/update/delete): ").lower()
    
    try:
        if action == 'create':
            user = wp.wp_user()
            print(f'User Created: {user}')
        elif action == 'update':
            user = wp.update_user()
            print(f'User Updated: {user}')
        elif action == 'delete':
            result = wp.delete_user()
            print(f'Delete Result: {result}')
        else:
            print("Invalid action. Please choose create, update, or delete.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")

    sys.exit()
