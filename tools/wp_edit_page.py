import requests
from flask import Flask, request, jsonify, render_template_string
import webbrowser
import threading
from crewai_tools import tool

app = Flask(__name__)

# Simple HTML template for the editor
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>WordPress Content Editor</title>
    <script src="https://cdn.ckeditor.com/4.16.0/full/ckeditor.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #4CAF50;
            font-size: 28px;
        }
        form {
            max-width: 900px;
            margin: 0 auto;
            background: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            font-size: 18px;
        }
        label {
            font-weight: bold;
            margin-bottom: 10px;
            display: block;
            color: #555;
            font-size: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 18px;
        }
        textarea {
            width: 100%;
            height: 550px;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 18px;
        }
        button {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 18px;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>WordPress Content Editor</h1>
    <form id="editor-form">
        <input type="hidden" id="page-id" value="{{ page_id }}">
        <label for="title">Title:</label>
        <input type="text" id="title" name="title">
        <br>
        <label for="content">Content:</label>
        <textarea id="editor" name="content"></textarea>
        <br>
        <button type="button" onclick="updatePage()">Update Page</button>
    </form>

    <script>
        CKEDITOR.replace('editor', {
            extraPlugins: 'colorbutton,font',
            toolbar: [
                { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'] },
                { name: 'colors', items: ['TextColor', 'BGColor'] },
                { name: 'styles', items: ['FontSize'] },
                { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'] },
                { name: 'links', items: ['Link', 'Unlink'] },
                { name: 'insert', items: ['Image', 'Table', 'HorizontalRule'] },
                { name: 'document', items: ['Source'] }
            ],
            fontSize_sizes: '18/18px;20/20px;22/22px;24/24px;26/26px;28/28px;30/30px;32/32px;36/36px;48/48px;60/60px;72/72px;'
        });

        window.onload = function() {
            loadPage();
        };

        function loadPage() {
            const pageId = document.getElementById('page-id').value;
            fetch(`/load-page/${pageId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.content && data.title) {
                        CKEDITOR.instances.editor.setData(data.content);
                        document.getElementById('title').value = data.title;
                    } else {
                        alert('Failed to load page content');
                    }
                })
                .catch(error => {
                    console.error('Error loading page:', error);
                    alert('Error loading page');
                });
        }

        function updatePage() {
            const pageId = document.getElementById('page-id').value;
            const title = document.getElementById('title').value;
            const content = CKEDITOR.instances.editor.getData();
            
            fetch('/update-page', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({page_id: pageId, title: title, content: content}),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.message === "Page updated successfully") {
                    // Shutdown the server after successful update
                    fetch('/shutdown', { method: 'POST' });
                }
            })
            .catch(error => {
                console.error('Error updating page:', error);
                alert('Error updating page');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    page_id = app.config['PAGE_ID']
    return render_template_string(MAIN_TEMPLATE, page_id=page_id)

@app.route('/load-page/<int:page_id>')
def load_page(page_id):
    url = f"{app.config['SITE_URL']}/wp-json/wp/v2/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {app.config['JWT_TOKEN']}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        page_data = response.json()
        return jsonify({"title": page_data['title']['rendered'], "content": page_data['content']['rendered']})
    else:
        return jsonify({"error": "Failed to load page"}), 400

@app.route('/update-page', methods=['POST'])
def update_page():
    data = request.json
    page_id = data['page_id']
    title = data['title']
    content = data['content']
    
    url = f"{app.config['SITE_URL']}/wp-json/wp/v2/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {app.config['JWT_TOKEN']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title,
        "content": content
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return jsonify({"message": "Page updated successfully"})
    else:
        return jsonify({"error": "Failed to update page"}), 400

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """
    Shutdown the Flask server.
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({"message": "Server shutting down..."})

@tool
def wordpress_edit_page(page_id: int, site_url: str, token: str):
    """
    This tool is useful for WordPress page editing based on ID.
    
    Args:
    page_id (int): The ID of the page to edit.
    site_url (str): The site URL for the WordPress site.
    token (str): The JWT token for authentication.
    """
    app.config['PAGE_ID'] = page_id
    app.config['SITE_URL'] = site_url
    app.config['JWT_TOKEN'] = token

    def run_flask():
        app.run(host='0.0.0.0', port=5002, debug=False)

    # Start the Flask app in a separate thread
    threading.Thread(target=run_flask).start()

    # Open the browser to the Flask app
    webbrowser.open("http://localhost:5002/")
