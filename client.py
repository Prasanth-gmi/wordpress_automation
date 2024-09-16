import requests

def get_operation_choice():
    print("Please enter the operation number you want to perform in WordPress site:")
    print("1. User Operation")
    print("2. Post Create")
    print("3. Page Create")
    print("4. Post Update")
    print("5. Page Update")
    print("6. Post Delete")
    print("7. Page Delete")
    print("8. Theme Creation")
    return int(input("Enter the operation number: "))

def perform_operation(operation):
    base_url = "http://127.0.0.1:8000"
    
    if operation == 1:
        response = requests.post(f"{base_url}/operation/1")
    elif operation == 4:
        post_id = int(input("Enter the post ID to update: "))
        response = requests.post(f"{base_url}/operation/4", json={"post_id": post_id})
    elif operation == 5:
        page_id = int(input("Enter the page ID to update: "))
        response = requests.post(f"{base_url}/operation/5", json={"page_id": page_id})
    elif operation == 8:
        project_name = input("Enter the project name: ")
        author = input("Enter the author name: ")
        response = requests.post(f"{base_url}/operation/8", json={"project_name": project_name, "author": author})
    else:
        print("Operation not implemented in this script.")
        return
    
    print(response.json())

if __name__ == "__main__":
    operation = get_operation_choice()
    perform_operation(operation)
