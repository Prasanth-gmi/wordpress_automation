import os
from crewai import Agent
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the LLM and tools
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

os.environ["SERPER_API_KEY"] = "e90e19aa7aac5143aba2a6c77f982f657a253869"
search_tool = SerperDevTool()

class Agents:
    def seo_specialist(self, topic):
        return Agent(
            role='SEO Specialist',
            goal=f'Develop SEO strategies and identify keywords for {topic}',
            backstory='You are an experienced SEO specialist with a keen understanding of search engine algorithms and user behavior.',
            verbose=True,
            llm=my_llm,
            allow_delegation=False,
        )

    def researcher(self, topic):
        return Agent(
            role='Researcher',
            goal=f'Gather comprehensive information on {topic}',
            backstory='You are a diligent researcher with a knack for finding reliable and relevant information quickly.',
            verbose=True,
            llm=my_llm,
            allow_delegation=False,
        )
  
    def content_writer(self, topic):
        return Agent(
            role='Content Writer',
            goal=f'Create engaging and informative blog posts on {topic}',
            backstory='You are a skilled writer with experience in creating compelling content across various niches.',
            verbose=True,
            llm=my_llm,
            allow_delegation=False,
        )
    
    def css_specialist(self):
        return Agent(
            role='Advanced CSS Stylist',
            goal='Apply advanced Bootstrap styles to HTML files generated from Markdown content, ensuring a modern and responsive design.',
            backstory='A CSS specialist with extensive expertise in Bootstrap styling, adept at converting Markdown content into sophisticated, responsive HTML designs with advanced styling techniques.',
            verbose=True,
            llm=my_llm,
            allow_delegation=False,
    )
    
    def conversion_agent(self):
        return Agent(
            role='Markdown-to-HTML Converter',
            goal='Convert Markdown files into HTML files by copying the content as-is, changing the file extension without altering the content or structure.',
            backstory='A diligent converter specialized in maintaining the integrity of Markdown content while converting it into HTML format for seamless integration.',
            verbose=True,
            llm=my_llm,
        )
        
    def wordpress_admin(self):
        return Agent(
            role="WordPress Admin",
            goal="Ensure seamless site operation, robust security, and peak performance by expertly managing content updates, plugins, themes, and user roles while consistently optimizing the user experience.",
            backstory="As the WordPress Administrator for a top-tier online business, your deep expertise in WordPress management is the backbone of the site’s success. You are a master at ensuring flawless site operation, from routine content updates to complex plugin configurations. Your keen eye for security and performance optimization keeps the site not only running smoothly but also safe from potential threats. With an unmatched knowledge of themes, plugins, and user management, you take pride in providing a superior experience for both users and content creators, all while swiftly addressing any challenges that arise.",
            llm=my_llm,
        )
    
    def agent_wordpress_theme_developer(self,project_name):
        return Agent(
            role="Full Stack WordPress Theme Developer",
            goal=f"Develop a complete, responsive WordPress Theme for {project_name} with advanced Bootstrap integration",
            backstory="""As an expert in full stack development and WordPress theme creation, 
                    I specialize in crafting comprehensive, responsive, and visually stunning WordPress websites. 
                    With a deep understanding of modern web practices, PHP, WordPress, and Bootstrap, 
                    I deliver high-quality, user-centered solutions that are both functional and aesthetically pleasing. 
                    My focus is on creating cohesive themes where all components work seamlessly together 
                    to provide an exceptional user experience. I follow WordPress coding standards rigorously 
                    to ensure compatibility and performance.""",
            llm=my_llm,
            verbose=True,
        )
        
    def agent_extractor(self):
        return Agent(
            role="Content Extractor",
            goal="Extract valuable information from various sources, including websites, blogs, and news articles",
            backstory="I am a skilled, knowledgeable, and organized content extractor who can quickly and effectively gather information from various sources, including websites, blogs, and news articles. My goal is to help users find the most relevant and valuable content for their needs, making it easier for them to find and share information that aligns with their interests and goals.",
            llm=my_llm,
            verbose=True,
        )

