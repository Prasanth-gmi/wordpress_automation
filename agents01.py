from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from auto_docker01 import DockerAutomationTool
# user input
image_name = input("Enter the image name : ")
dockerhub_username = input("Enter the dockerhub username : ")
dockerhub_password = input("Enter the dockerhub password : ")
repo_name = input("Enter the repo name : ")
tag = input("Enter the tag value : ")

# Initialize the LLM and tools
my_llm = ChatGroq(
    api_key="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",
    model="llama3-8b-8192",
)

Docker_Specialist = Agent(
    role="Docker Specialist",
    goal=f"Fully automate the lifecycle of Docker-based workflows, from building and testing Docker images to pushing them to DockerHub. Ensure seamless container operations, optimize image creation, and maintain efficiency and security in the entire process.",
    backstory="You are a containerization virtuoso with deep expertise in Docker. Over the years, you’ve become the go-to specialist for automating Docker processes, mastering both the intricacies of Docker commands and the nuances of building efficient, lightweight images. Whether it's setting up a continuous integration pipeline, testing containers, or pushing the final image to DockerHub, you excel in every phase of Docker workflows. Your passion lies in simplifying the complexity of containerized environments, ensuring faster builds, flawless execution, and zero downtime.",
    llm=my_llm,
)

dockerfile = Task(
    description=f"""
        - {image_name}
        - {dockerhub_username}
        - {dockerhub_password}
        - {repo_name}
        - {tag}
        - Automate the complete Docker workflow from building, testing, and running Docker images to pushing them to the DockerHub repository. Ensure security and efficiency.
    """,
    expected_output=f"""
        A detailed log including:
        - Docker build status: Whether the Docker image was built successfully or encountered errors.
        - Docker push status: Confirmation that the image has been pushed to DockerHub.
        - DockerHub pull command: The command to pull the image from DockerHub, in the format:
            docker pull {dockerhub_username}/{repo_name}:{tag}
        - Docker run command: The command to run the image, in the format:
            docker run -d -p 8000:8000 {dockerhub_username}/{repo_name}:{tag}
    """,
    agent=Docker_Specialist,
    tools=[DockerAutomationTool],
)


crew = Crew(
    agents=[Docker_Specialist], 
    tasks=[dockerfile], 
    verbose=True,
    )
result = crew.kickoff()
