from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Crew, Process
from tasks import Tasks
from agents import Agents
from langchain_groq import ChatGroq
import requests
import os
from tools.post_list import post_list
from tools.page_list import page_list
from langchain_google_genai import ChatGoogleGenerativeAI
# site_url = 'http://host.docker.internal/wordpress/'
# site_url = 'https://acetechinside.com'
# username = "aparna"
# password = "Wewillwin@01"  
# site_url = 'http://localhost:80/wordpress/'
# username = "root"
# password = "Su6yalun@"    
username = os.getenv("WORDPRESS_USER")
password = os.getenv("WORDPRESS_PASSWORD")
site_url = os.getenv("WORDPRESS_SITE_URL")
response = requests.post(f'{site_url}/wp-json/jwt-auth/v1/token', data={
            'username': username,
            'password': password,
        })
token = response.json().get('token')

app = FastAPI()
agents = Agents()
tasks = Tasks()
my_llm = ChatGroq(
    api_key="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",
    model="llama3-8b-8192",
)
# my_llm = ChatGoogleGenerativeAI(
#     model="gemini-pro",
#     verbose=True,
#     temperature=0.5,
#     google_api_key="AIzaSyDvKrVQ4_7hZGN8qfZ-fEA0elvTjv9nnj4"
# )

class PostCreateRequest(BaseModel):
    topic: str

class PageCreateRequest(BaseModel):
    topic: str

class PostUpdateRequest(BaseModel):
    post_id: int

class PageUpdateRequest(BaseModel):
    page_id: int

class PostDeleteRequest(BaseModel):
    post_title: str

class PageDeleteRequest(BaseModel):
    page_id: int

class ThemeCreateRequest(BaseModel):
    project_name: str
    author: str

# @app.post("/user/")
# async def create_user():
#     wordpress_admin = agents.wordpress_admin()
#     user_module_task = tasks.user_module_task(wordpress_admin)
#     crew01 = Crew(
#         agents=[wordpress_admin],
#         tasks=[user_module_task],
#         verbose=True,
#     )
#     result01 = crew01.kickoff()
#     return {"result": result01}

@app.post("/post/create/")
async def create_post(request: PostCreateRequest):
    topic = request.topic
    markdown_file="styled_markdown.md"
    output_html_file="styled_markdown.html"
    seo_specialist = agents.seo_specialist(topic)
    researcher = agents.researcher(topic)
    content_writer = agents.content_writer(topic)
    css_specialist = agents.css_specialist()
    conversion_agent = agents.conversion_agent()
    wordpress_admin = agents.wordpress_admin()
    seo_task = tasks.seo_task(seo_specialist, topic)
    research_task = tasks.research_task(researcher, topic, [seo_task])
    content_writer_task = tasks.content_writer_task(content_writer, topic, [research_task])
    apply_bootstrap_styles_to_markdown = tasks.apply_bootstrap_styles_to_markdown(css_specialist,[content_writer_task])
    convert_markdown_to_html_task = tasks.convert_markdown_to_html_task(conversion_agent,markdown_file,output_html_file)
    post_creation_task = tasks.post_creation_task(wordpress_admin, topic,[content_writer_task],site_url, token)
    crew01 = Crew(
        agents=[seo_specialist, researcher, content_writer],
        tasks=[seo_task, research_task, content_writer_task],
        verbose=True,
    )
    result01 = crew01.kickoff()
    crew = Crew(
        agents=[css_specialist,conversion_agent],
        tasks=[apply_bootstrap_styles_to_markdown,convert_markdown_to_html_task],
        verbose=True,
    )
    result01 = crew.kickoff()
    crew = Crew(
        agents=[wordpress_admin],
        tasks=[post_creation_task],
        verbose=True,
    )
    result01 = crew.kickoff()
@app.post("/page/create/")
async def create_page(request: PageCreateRequest):
    topic = request.topic
    markdown_file="styled_markdown.md"
    output_html_file="styled_markdown.html"
    seo_specialist = agents.seo_specialist(topic)
    researcher = agents.researcher(topic)
    content_writer = agents.content_writer(topic)
    css_specialist = agents.css_specialist()
    conversion_agent = agents.conversion_agent()
    wordpress_admin = agents.wordpress_admin()
    seo_task = tasks.seo_task(seo_specialist, topic)
    research_task = tasks.research_task(researcher, topic, [seo_task])
    content_writer_task = tasks.content_writer_task(content_writer, topic, [research_task])
    apply_bootstrap_styles_to_markdown = tasks.apply_bootstrap_styles_to_markdown(css_specialist,[content_writer_task])
    convert_markdown_to_html_task = tasks.convert_markdown_to_html_task(conversion_agent,markdown_file,output_html_file)
    page_creation_task = tasks.page_creation_task(wordpress_admin, topic,[content_writer_task],site_url, token)
    crew01 = Crew(
        agents=[seo_specialist, researcher, content_writer],
        tasks=[seo_task, research_task, content_writer_task],
        verbose=True,
    )
    result01 = crew01.kickoff()
    crew = Crew(
        agents=[css_specialist,conversion_agent],
        tasks=[apply_bootstrap_styles_to_markdown,convert_markdown_to_html_task],
        verbose=True,
    )
    result01 = crew.kickoff()
    crew = Crew(
        agents=[wordpress_admin],
        tasks=[page_creation_task],
        verbose=True,
    )
    result01 = crew.kickoff()
    return {"result": result01}

@app.get("/post/post_list/")
async def list_post():
    return (post_list(site_url,token))
    
@app.get("/page/page_list/")
async def list_pages():
    return (page_list(site_url,token))
    
@app.put("/post/update/")
async def update_post(request: PostUpdateRequest):
    post_id = request.post_id
    wordpress_admin = agents.wordpress_admin()
    post_edit_task = tasks.post_edit_task(wordpress_admin, post_id,site_url, token)
    crew01 = Crew(
        agents=[wordpress_admin],
        tasks=[post_edit_task],
        verbose=True,
    )
    result01 = crew01.kickoff()
    return {"result": result01}

@app.put("/page/update/")
async def update_page(request: PageUpdateRequest):
    page_id = request.page_id
    wordpress_admin = agents.wordpress_admin()
    page_edit_task = tasks.page_edit_task(wordpress_admin, page_id,site_url, token) 
    crew01 = Crew(
        agents=[wordpress_admin],
        tasks=[page_edit_task],
        verbose=True,
    )
    result01 = crew01.kickoff()
    return {"result": result01}

@app.delete("/post/delete/")
async def delete_post(request: PostDeleteRequest):
    post_title = request.post_title
    wordpress_admin = agents.wordpress_admin()
    delete_post_task = tasks.delete_post_task(wordpress_admin, post_title,site_url, token)
    crew01 = Crew(
        agents=[wordpress_admin],
        tasks=[delete_post_task],
        verbose=True,
    )
    result01 = crew01.kickoff()
    return {"result": result01}

@app.delete("/page/delete/")
async def delete_page(request: PageDeleteRequest):
    page_id = request.page_id
    wordpress_admin = agents.wordpress_admin()
    delete_page_task = tasks.delete_page_task(wordpress_admin, page_id,site_url, token)
    crew01 = Crew(
        agents=[wordpress_admin],
        tasks=[delete_page_task],
        verbose=True,
    )
    result01 = crew01.kickoff()
    return {"result": result01}

@app.post("/theme/create/")
async def create_theme(request: ThemeCreateRequest):
    project_name = request.project_name
    author = request.author
    file_path = "output/complete_theme.md"
    folder_name = project_name
    agent_wordpress_theme_developer = agents.agent_wordpress_theme_developer(project_name)
    agent_extractor = agents.agent_extractor()
    task_complete_wordpress_theme = tasks.task_complete_wordpress_theme(agent_wordpress_theme_developer, author, project_name)
    task_extract_content = tasks.task_extract_content(agent_extractor, file_path, folder_name)
    crew01 = Crew(
        agents=[agent_wordpress_theme_developer],
        tasks=[task_complete_wordpress_theme],
        verbose=True,
    )
    result01 = crew01.kickoff()
    crew01 = Crew(
        agents=[agent_extractor],
        tasks=[task_extract_content],
        verbose=True,
    )
    result01 = crew01.kickoff()
    return {"result": result01}

# uvicorn main01:app --reload