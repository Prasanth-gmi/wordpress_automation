import docker
import os
from crewai_tools import tool

def build_and_push_docker_image(dockerfile_path, image_name, dockerhub_username, dockerhub_password, repo_name, tag):
    client = docker.from_env()

    # Build Docker image
    try:
        print(f"Building Docker image '{image_name}' from path '{dockerfile_path}'...")
        image, logs = client.images.build(path=dockerfile_path, tag=image_name)
        for log in logs:
            if 'stream' in log:
                print(log['stream'].strip())
    except Exception as e:
        print(f"Error while building image: {e}")
        return

    # Log in to Docker Hub
    try:
        print(f"Logging into Docker Hub as '{dockerhub_username}'...")
        client.login(username=dockerhub_username, password=dockerhub_password)
        print("Login successful.")
    except Exception as e:
        print(f"Error logging in to Docker Hub: {e}")
        return

    # Tag the image for Docker Hub
    try:
        full_image_name = f"{dockerhub_username}/{repo_name}:{tag}"
        print(f"Tagging image '{image_name}' as '{full_image_name}'...")
        image.tag(f"{dockerhub_username}/{repo_name}", tag)
    except Exception as e:
        print(f"Error tagging image: {e}")
        return

    # Push the image to Docker Hub
    try:
        print(f"Pushing image '{full_image_name}' to Docker Hub...")
        push_logs = client.images.push(f"{dockerhub_username}/{repo_name}", tag=tag, stream=True, decode=True)
        for log in push_logs:
            if 'status' in log:
                print(log['status'])
    except Exception as e:
        print(f"Error pushing image to Docker Hub: {e}")

# if __name__ == "__main__":
#     # Path to the directory containing your Dockerfile
@tool
def DockerAutomationTool(image_name: str, dockerhub_username: str, dockerhub_password: str, repo_name: str, tag: str):
    """  
    A custom tool to automate Docker tasks: building and pushing an image to DockerHub.
    
    Args:
    - image_name: Set the docker image_name. It should be same agents.py file image_name value.
    - dockerhub_username: Set the dockerhub_username. It should be same agents.py file dockerhub_username value.
    - dockerhub_password: Set the dockerhub_password. It should be same agents.py file dockerhub_password value.
    - repo_name: Set the dockerhub repo_name. It should be same agents.py file repo_name value.
    - tag: Set the tag. It should be same agents.py file tag value.
    
    Returns:
    - A report detailing the success or failure of each Docker operation.
    """
    
    dockerfile_path = os.path.abspath(".")  # Adjust if necessary

    build_and_push_docker_image(dockerfile_path, image_name, dockerhub_username, dockerhub_password, repo_name, tag)