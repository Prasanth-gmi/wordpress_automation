from crewai import Crew, Process
from tasks import Tasks
from agents import Agents
from langchain_groq import ChatGroq
agents = Agents()
tasks = Tasks()
my_llm = ChatGroq(
    api_key="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",
    model="llama3-8b-8192",
)

print("Please, Enter the which operation you want to perform in wordpress site (eg: )")
print("1. User ")
print("2. Post Create ")
print("3. Page Create ")
print("4. Post Update ")
print("5. Page Update ")
print("6. Post Delete")
print("7. Page Delete")
print("8. Theme Creation")
operation = int(input("Please, Enter the operation number: "))
if operation == 1:
    wordpress_admin = agents.wordpress_admin()
    user_module_task = tasks.user_module_task(wordpress_admin)
    crew01 = Crew(
    agents=[wordpress_admin],
    tasks=[user_module_task],
    verbose=True,
    )
    result01 = crew01.kickoff()
elif operation == 2:
    topic = input("Please, Which topic you want? \n")
    category = input("Please, Enter the category : ")
    tag = input("Please, Enter the tag : ")
    seo_specialist = agents.seo_specialist(topic)
    researcher = agents.researcher(topic)
    content_writer = agents.content_writer(topic)
    wordpress_admin = agents.wordpress_admin()
    seo_task = tasks.seo_task(seo_specialist,topic)
    research_task = tasks.research_task(researcher,topic,[seo_task])
    content_writer_task = tasks.content_writer_task(content_writer,topic,[research_task])
    post_creation_task = tasks.post_creation_task(wordpress_admin,topic,category,tag)
    crew01 = Crew(
    agents=[seo_specialist,researcher,content_writer,],
    tasks=[seo_task,research_task,content_writer_task,],
    verbose=True,
    )
    result01 = crew01.kickoff()
    crew = Crew(
    agents=[wordpress_admin,],
    tasks=[post_creation_task,],
    verbose=True,
    )
    result01 = crew.kickoff()
elif operation == 3:
    topic = input("Please, Which topic you want? \n")
    seo_specialist = agents.seo_specialist(topic)
    researcher = agents.researcher(topic)
    content_writer = agents.content_writer(topic)
    wordpress_admin = agents.wordpress_admin()
    seo_task = tasks.seo_task(seo_specialist,topic)
    research_task = tasks.research_task(researcher,topic,[seo_task])
    content_writer_task = tasks.content_writer_task(content_writer,topic,[research_task])
    page_creation_task = tasks.page_creation_task(wordpress_admin,topic)
    crew01 = Crew(
    agents=[seo_specialist,researcher,content_writer,],
    tasks=[seo_task,research_task,content_writer_task,],
    verbose=True,
    )
    result01 = crew01.kickoff()
    crew = Crew(
    agents=[wordpress_admin,],
    tasks=[page_creation_task,],
    verbose=True,
    )
    result01 = crew.kickoff()
elif operation == 4:
    get_wp_post_list.main()
    post_id = int(input("Enter the post id: "))
    wordpress_admin = agents.wordpress_admin()
    post_edit_task = tasks.post_edit_task(wordpress_admin,post_id)
    crew01 = Crew(
    agents=[wordpress_admin],
    tasks=[post_edit_task],
    verbose=True,
    )
    result01 = crew01.kickoff()
elif operation == 5:
    get_wp_page_list.main()
    page_id = int(input("Enter the page id: "))
    wordpress_admin = agents.wordpress_admin()
    page_edit_task = tasks.page_edit_task(wordpress_admin,page_id)
    crew01 = Crew(
    agents=[wordpress_admin],
    tasks=[page_edit_task],
    verbose=True,
    )
    result01 = crew01.kickoff()
elif operation == 6:
    get_wp_post_list.main()
    post_id = int(input("Enter the post id: "))
    wordpress_admin = agents.wordpress_admin()
    delete_post_task = tasks.delete_post_task(wordpress_admin,post_id)
    crew01 = Crew(
    agents=[wordpress_admin],
    tasks=[delete_post_task],
    verbose=True,
    )
    result01 = crew01.kickoff()
elif operation == 7:
    get_wp_page_list.main()
    page_id = int(input("Enter the page id: "))
    wordpress_admin = agents.wordpress_admin()
    delete_page_task = tasks.delete_page_task(wordpress_admin,page_id)
    crew01 = Crew(
    agents=[wordpress_admin],
    tasks=[delete_page_task],
    verbose=True,
    )
    result01 = crew01.kickoff()
elif operation == 8:
    project_name = input("Enter the project name : ")
    author = input("Enter the author name : ")
    file_path="output/complete_theme.md"
    folder_name = project_name
    agent_wordpress_theme_developer = agents.agent_wordpress_theme_developer(project_name)
    agent_extractor = agents.agent_extractor()
    task_complete_wordpress_theme = tasks.task_complete_wordpress_theme(agent_wordpress_theme_developer,author,project_name)
    task_extract_content = tasks.task_extract_content(agent_extractor,file_path, folder_name)
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