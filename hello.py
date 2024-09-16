import requests
site_url = 'http://localhost:80/wordpress/'
username = input("Enter the User Name : ")
password = input("Enter the Password : ")
response = requests.post(f'{site_url}/wp-json/jwt-auth/v1/token', data={
            'username': username,
            'password': password
        })
token = response.json().get('token')
print(token)