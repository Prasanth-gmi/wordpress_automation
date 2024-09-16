import os
from textwrap import dedent
from crewai import Task
from agents import Agents
from crewai_tools import SerperDevTool
from tools.wp_post import wordpress_post
from tools.wp_page import create_wordpress_page
from tools.wp_edit_post import wordpress_edit_post
from tools.wp_edit_page import wordpress_edit_page
from tools.wp_delete_post import wordpress_delete_post_by_title
from tools.wp_delete_page import wordpress_delete_page
from tools.wp_user_module import wordpress_user_management
from tools.wp_theme_create import markdown_to_files
from tools.convert_md_to_html_file import convert_md_to_html_file
os.environ["SERPER_API_KEY"] = "e90e19aa7aac5143aba2a6c77f982f657a253869"
search_tool = SerperDevTool()

class Tasks:
    def seo_task(self, agent, topic):
        return Task(
            description=f'Develop an SEO strategy and identify keywords for a blog post on {topic}',
            agent=agent,
            expected_output="""
                1. Primary keyword: [insert primary keyword]
                2. Secondary keywords: [list 3-5 secondary keywords]
                3. Recommended title: [insert SEO-optimized title]
                4. Meta description: [insert 150-160 character meta description]
                5. Content structure:
                - Introduction (brief overview of [topic])
                - [3-5 main sections or subheadings]
                - Conclusion
                6. Recommended word count: [insert recommended word count]""",
            tools=[search_tool],
        )

    def research_task(self, agent, topic, context):
        return Task(
            description=f'Research comprehensive information on {topic}',
            agent=agent,
            expected_output="""
                1. Overview of [topic],
                2. Key points or aspects of [topic]:
                - [list 5-7 key points]
                3. Recent developments or trends in [topic] (within the last 1-2 years)
                4. Statistics or data related to [topic]
                5. Expert opinions or quotes on [topic]
                6. Potential challenges or controversies related to [topic]
                7. Future outlook for [topic]
                """,
            tools=[search_tool],
            context=context,
        )

    def content_writer_task(self, agent, topic, context):
        return Task(
            description=f"Write a blog post about {topic} using the SEO strategy and research provided",
            expected_output="""
                1. Introduction:
                - Brief overview of [topic]
                - Thesis statement
                2. Main body:
                - [3-5 main sections, each addressing a key aspect of the topic]
                - Use of relevant statistics, expert quotes, and examples
                - Incorporation of primary and secondary keywords naturally
                3. Conclusion:
                - Summary of key points
                4. Meta description: [insert 150-160 character meta description]
                """,
            agent=agent,
            context=context,
            output_file="content.md",
        )

    def apply_bootstrap_styles_to_markdown(self,agent,context):
        return Task(
            description=f"""Transform the provided Markdown file into an HTML masterpiece optimized for WordPress, leveraging Bootstrap's latest CDN. The resulting HTML should exemplify modern web design while adhering to WordPress best practices:

            1. Styling:
            - Use Bootstrap's utility classes for responsive typography, following WordPress standard sizes:
                - H1: 2.5rem (40px)
                - H2: 2rem (32px)
                - H3: 1.75rem (28px)
                - H4: 1.5rem (24px)
                - Body text: 1rem (16px)
            - Implement a color scheme that complements WordPress themes, using Bootstrap's text and background utilities.
            - Utilize Bootstrap's spacing utilities for consistent margins and padding.

            2. Layout:
            - Employ Bootstrap's responsive grid system for flexible, mobile-first layouts.
            - Ensure proper content hierarchy using appropriate heading tags (h1, h2, h3, etc.).

            3. Components:
            - Integrate Bootstrap components that enhance readability and user engagement:
                - Use cards for featured content or summary sections.
                - Implement accordions for FAQs or expandable content sections.
                - Utilize alerts for important notices or callouts.

            4. Images:
            - Wrap images in Bootstrap's `img-fluid` class for responsive behavior.
            - Use `figure` and `figcaption` for image captions, styled with Bootstrap classes.
            - Implement lazy loading for images to improve page load times.

            5. Interactivity:
            - Add Bootstrap's collapse component for expandable sections.
            - Implement tooltips or popovers for additional information or definitions.

            6. Accessibility:
            - Ensure proper ARIA labels and roles are used with Bootstrap components.
            - Maintain sufficient color contrast for text readability.

            7. WordPress Integration:
            - Avoid using custom CSS; rely solely on Bootstrap classes for styling.
            - Ensure compatibility with WordPress Gutenberg blocks by using appropriate div structures.
            - Omit any site-wide elements like navigation or footers, focusing only on post content.

            The final HTML should be a visually appealing, highly readable, and interactive WordPress post that maintains consistency with typical WordPress styling while leveraging Bootstrap's capabilities.""",
            expected_output="An HTML file that seamlessly integrates Bootstrap styling with WordPress best practices. The output should be a polished, responsive, and visually engaging post ready for direct insertion into the WordPress editor, requiring no additional styling or formatting.",
            agent=agent,
            context=context,
            output_file="styled_markdown.md",
        )
    
    def convert_markdown_to_html_task(self,agent,markdown_file,output_html_file):
        return Task(
            description=f"""Convert the provided Markdown file '{markdown_file}' into an HTML file '{output_html_file}', optimizing it for WordPress integration:

            1. Content Conversion:
            - Accurately convert all Markdown syntax to corresponding HTML elements.
            - Preserve the document structure, including headings, paragraphs, lists, and code blocks.

            2. Image Handling:
            - Convert Markdown image syntax to HTML <img> tags.
            - Add the 'img-fluid' class to all images for responsive behavior.
            - Wrap images in <figure> tags and include <figcaption> for captions when available.

            3. Link Processing:
            - Ensure all links are properly converted to HTML <a> tags.
            - Add 'target="_blank"' and 'rel="noopener noreferrer"' to external links for security.

            4. Code Blocks:
            - Wrap code blocks in <pre><code> tags with appropriate language classes.
            - Ensure proper escaping of HTML entities within code blocks.

            5. WordPress-specific Optimizations:
            - Add 'wp-block-' prefixed classes to top-level elements for Gutenberg compatibility.
            - Implement proper spacing between elements using Bootstrap utility classes.

            6. Metadata:
            - If present in the Markdown, convert front matter to HTML comments for WordPress SEO plugins.

            7. Accessibility:
            - Ensure heading levels are properly nested for screen readers.
            - Add appropriate ARIA labels to elements where necessary.

            8. Output:
            - Save the converted content as '{output_html_file}' with a .html extension.
            - Ensure the HTML structure is clean, properly indented, and free of unnecessary whitespace.
            - Remove heading tag like <h1>""",
            expected_output=f"""A well-structured HTML file '{output_html_file}' that:
            1. Accurately represents the content of '{markdown_file}'.
            2. Is optimized for WordPress integration with appropriate classes and structure.
            3. Incorporates responsive image handling and accessibility features.
            4. Is ready for direct insertion into the WordPress editor without requiring additional formatting.""",
            agent=agent,
            tools=[convert_md_to_html_file]
        )
    def post_creation_task(self, agent, topic, context, site_url, token):
        return Task(
            description=f"Post content related to {topic}.",
            expected_output=f"""
                    1. {topic}
                    2. {site_url}, {token}
                    3. Title should be {topic}. The title should be the topic value; don't add extra content to the title.
                    4. site_url should be {site_url}. The site_url should be the site_url value; don't add extra content to the site_url.
                    5. token should be {token}. The token should be the token value; don't add extra content to the token.
                    6. Using wordpress_post post the content in wordpress. The content should be very structured.
                    7. Add bootstrap style. The post should be well styled. Give unique look and feel.
                    8. Using wordpress_post post the content in wordpress. using rest api with JWT token.
                """,
            agent=agent,
            context=context,
            tools=[wordpress_post],
        )

    def page_creation_task(self, agent, topic, context, site_url, token):
        return Task(
            description=f"Page content related to {topic}.",
            expected_output=f"""
                    1. {topic}
                    2. {site_url}, {token}
                    3. Title should be {topic}. The title should be the topic value; don't add extra content to the title.
                    4. site_url should be {site_url}. The site_url should be the site_url value; don't add extra content to the site_url.
                    5. token should be {token}. The token should be the token value; don't add extra content to the token.
                    6. Using wordpress_page create the page content in wordpress. The content should be very structured.
                    7. Add bootstrap style. The page should be well styled. Give unique look and feel.
                    8. Using wordpress_page create the page content in wordpress. using rest api with JWT token.
                """,
            agent=agent,
            context=context,
            tools=[create_wordpress_page],
	)

    def post_edit_task(self, agent, post_id,site_url, token):
        return Task(
            description=f"Update the post based on {post_id}.",
            expected_output=f"""
                    1. Fetch title and content from WordPress based on {post_id}.
                    2. site_url should be {site_url}. The site_url should be the site_url value; don't add extra content to the site_url.
                    3. token should be {token}. The token should be the token value; don't add extra content to the token.
                    2. Open Flask and update the content. When the update button is pressed, update the WordPress site.
                """,
            agent=agent,
            tools=[wordpress_edit_post],
        )

    def page_edit_task(self, agent, page_id,site_url, token):
        return Task(
            description=f"Update the page based on {page_id}.",
            expected_output=f"""
                    1. Fetch title and content from WordPress based on {page_id}.
                    2. site_url should be {site_url}. The site_url should be the site_url value; don't add extra content to the site_url.
                    3. token should be {token}. The token should be the token value; don't add extra content to the token.
                    4. Open Flask and update the content. When the update button is pressed, update the WordPress site.
                """,
            agent=agent,
            tools=[wordpress_edit_page],
        )
    
    def delete_post_task(self, agent, post_title,site_url, token):
        return Task(
            description=f"Delete the page with related Page ID {post_title}.",
            expected_output=f"""
                    1. The provided Page Title is {post_title}.
                    2. Ensure that the page with Title {post_title} is deleted from the WordPress site at {site_url}.
                    3. Verify that the page no longer appears in the list of pages on the WordPress site.
                    4. Provide a confirmation that the page has been successfully deleted.
                    5. The task was performed using the following token: {token}.
                """,
            agent=agent,
            tools=[wordpress_delete_post_by_title],
        )
    
    def delete_page_task(self, agent, page_id,site_url, token):
        return Task(
            description=f"Delete the post with related Page ID {page_id}.",
            expected_output=f"""
                    1. Fetch title and content from WordPress based on {page_id}.
                    2. site_url should be {site_url}. The site_url should be the site_url value; don't add extra content to the site_url.
                    3. token should be {token}. The token should be the token value; don't add extra content to the token.
                    4. Open Flask and update the content. When the update button is pressed, update the WordPress site.
                """,
            agent=agent,
            tools=[wordpress_delete_page],
        )
    
    def user_module_task(self, agent):
        return Task(
            description=f"Create,Update and delete user for WordPress Site .",
            expected_output=f"""
                    Create, Update and delete user WordPress Site users.
                """,
            agent=agent,
            tools=[wordpress_user_management],
        )

    def task_complete_wordpress_theme(self, agent, author, project_name):
        return Task(
            description=f"Develop a complete WordPress Theme for {project_name} including index.php, header.php, footer.php, functions.php, style.css, and theme.json, all featuring advanced Bootstrap integration and responsive design.",
            expected_output=f"""

        Develop a fully-featured WordPress Theme for `{project_name}` with the following components and requirements:

        1. **header.php:**
            - Include a link to the stylesheet (`style.css`) in the `<head>` section.
            - Integrate Bootstrap CDN links for CSS and JS.
            - Use WordPress’s default navbar with the following requirements:
            - Align the site logo to the left using Bootstrap’s grid system.
            - Align navigation links to the right in a row format.
            - Ensure the navbar is responsive and supports dropdowns.
            - Style the default WordPress navbar to ensure:
                - The logo and navigation links are correctly aligned.
                - Submenus are displayed properly, appearing only when the parent menu item is clicked.
                - Apply Bootstrap’s advanced styling to ensure a polished look and consistent user experience.
            - Ensure the navbar links scroll to the corresponding sections on the page:
                - "Home" should scroll to the top of the index page.
                - "Pricing" should scroll to the Pricing section.
                - "Products" should scroll to the Products section.
                - "Blog/News" should scroll to the Blog/News section.
            - Set the navbar background color to black, font color to white, and active links to blue.

        2. **index.php:**
            - Call `get_header()` to include `header.php` at the beginning of the file.
            - Construct a multi-section layout using advanced Bootstrap components and animations to enhance visual appeal and interactivity.
            - Incorporate the following sections: Hero, Products, Pricing, and Blog/News.
            - Use Bootstrap’s grid system and utilities for responsive and neatly aligned content:
            
            - **Hero Section:**
                - **Full-Page Cover:** Ensure the Hero section spans the full viewport height with a captivating background image or color. Use Bootstrap’s `d-flex`, `align-items-center`, and `justify-content-center` utilities to center the content both horizontally and vertically.
                - **Content:** Display a large, bold heading "Welcome to {project_name}" with ample spacing. Include a prominently styled "Get Started" button using Bootstrap’s button classes. The button should be visually striking and color-coordinated with the overall theme.
                - **Styling:** Apply text alignment and spacing utilities to achieve a balanced, aesthetically pleasing layout. Ensure that the content stands out against the background with clear contrast.

            - **Products Section:**
                - **Heading and Layout:** Place a centered heading above the products grid. Use Bootstrap’s grid system to display products in a responsive grid layout, with two product cards per row.
                - **Product Cards:** Each product should be presented in a Bootstrap card component, featuring an image, title, description, and a call-to-action button. Ensure that cards are evenly spaced and well-aligned within the grid.
                - **Styling:** Utilize Bootstrap’s card and grid utilities to maintain a clean and organized presentation. Apply margin and padding utilities to ensure proper spacing between product cards.

            - **Pricing Section:**
                - **Heading and Layout:** Center the heading above the pricing grid. Display pricing plans ("Free Plan," "Paid Plan," "Premium Plan") using Bootstrap’s card components for a structured and appealing layout.
                - **Pricing Cards:** Each card should highlight the features and benefits of the respective pricing plan. Use Bootstrap’s card classes to create a visually distinct pricing table, with clear distinctions between different plans.
                - **Styling:** Apply Bootstrap’s card and text utilities to ensure readability and emphasis on key features. Use background colors and borders to differentiate between pricing tiers effectively.

            - **Blog/News Section:**
                - **Heading and Layout:** Center the heading above the blog/news grid. Display the latest posts or updates using Bootstrap’s card and grid components for a cohesive layout.
                - **Dynamic Content:** Utilize WordPress functions to query and dynamically display posts and pages. Implement a loop to handle varying numbers of posts and pages, adjusting the grid layout based on content count.
                - **Styling:** Ensure each blog/news item is displayed within a card component, featuring an image, title, excerpt, and a "Read More" link. Use Bootstrap’s spacing and typography utilities to maintain a clean, readable presentation.

            - Ensure that all sections are fully responsive, with content adapting smoothly to different screen sizes. Utilize Bootstrap’s responsive utilities to maintain proper alignment, spacing, and visual consistency across devices.
            - Call `get_footer()` to include `footer.php` at the end of the file.


        3. **footer.php:**
            - Include Bootstrap CSS and JS links from the CDN in the `<head>` section.
            - Design the footer using Bootstrap’s grid system for a responsive layout:
            - Contact information section aligned to the left with Bootstrap styling.
            - Newsletter signup form on the right with modern Bootstrap styling.
            - Footer content should be divided into multiple columns for organization.
            - Apply advanced Bootstrap styles for visual consistency.
            - Include copyright notice and legal information at the bottom, centered with Bootstrap’s typography and alignment classes.
            - Include the project name `{project_name}` and author name `{author}` as required.

        4. **functions.php:**
            - Implement a theme setup function enabling post thumbnails, title tags, and custom menus.
            - Enqueue Bootstrap CSS and JS from CDN and the theme’s custom stylesheet.
            - Register navigation menus and widget areas.
            - Add custom functions for theme-specific features and ensure Bootstrap styles are correctly integrated.
            - Ensure dropdown menus and submenus work in the navigation bar without the Navwalker method, ensuring dropdowns appear only when the menu item is clicked.
            - Follow advanced PHP practices for efficiency and security.

        5. **style.css:**
        
            - Define global styles for typography, colors, and layout in alignment with Bootstrap’s framework.
            - **Theme Header Comment:** Include theme metadata:
            ```
            /*
            Theme Name: {project_name}
            Theme URI: https://example.com/{project_name}
            Author: {author}
            Author URI: https://example.com/{author}
            Description: A responsive and advanced WordPress theme for {project_name}.
            Version: 1.0
            License: GNU General Public License v2 or later
            License URI: http://www.gnu.org/licenses/gpl-2.0.html
            Text Domain: {project_name}
            */
            ```
            - **Theme Header:**: it is must.
            - **Header Styles:**
            - Style the header section to ensure the logo and navigation are displayed correctly.
            - Ensure the header background color and text color match the overall theme.
            - **Footer Styles:**
            - Style the footer section to ensure proper alignment of contact information, social media links, and quick links.
            - Apply background color, text color, and responsive design principles to the footer.
            - **Index Page Styles:**
            - Style individual sections (Hero, Products, Pricing, Blog/News) for visual consistency.
            - Ensure all sections are responsive and visually appealing with proper spacing and alignment.
            - Ensure responsive adjustments and consistent color scheme and typography across the theme.

        6. **theme.json:**
            - Include comprehensive theme metadata such as name, version, and description.
            - Define color palette settings aligned with Bootstrap’s color system.
            - Specify typography settings including font families, sizes, and line heights.
            - Configure layout settings to complement Bootstrap’s grid system.
            - Set custom theme supports and editor styles for a consistent design.
            - Ensure theme settings are compatible with the latest WordPress and Bootstrap versions.

        Ensure all components are fully responsive, integrate advanced Bootstrap features, and provide a seamless user experience. Adhere to WordPress coding standards and modern PHP practices throughout the development process.

            """,
            agent=agent,
            output_file="output/complete_theme.md",
        )
        
    def task_extract_content(self, agent, file_path, folder_name):
        return Task(
            description=f"Use the `markdown_to_files` tool to extract content from the specified Markdown file {file_path} based on predefined patterns for different files. The tool will clean the content by removing code block markers and write it to the appropriate files in the {folder_name} folder. Ensure that the ZIP archive of the theme folder is created after writing the files.",
            expected_output=f"The content from the Markdown file at {file_path} should be extracted, cleaned, and saved to the respective files in the '{folder_name}' folder. Additionally, a ZIP file of the theme folder should be created.",
            agent=agent,
            tools=[markdown_to_files],
        )