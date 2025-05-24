from flask import Flask, render_template_string, request, jsonify, redirect, url_for, send_from_directory
import os
import threading
import time
import sys
import subprocess
import atexit
import zipfile
import pandas as pd
import json
import yaml
import docx
import requests
from werkzeug.utils import secure_filename
import pyautogui
from datetime import datetime
import socket

# Initialize Flask app
app_calls = Flask(__name__)

# Configuration
SERVER_DIR = 'servers'
BASE_PORT = 5001  # Main app runs on 5000, micro-servers start from 5001
NUM_SERVERS = 10

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'xls', 'doc', 'docx', 'csv', 'zip'}
app_calls.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the directories exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

# Store server processes
server_processes = {}
server_logs = {}

# Global variables
user_key = "test_key"  # Default test key
user_plan = ""
openaikey = ""
prompt_index = 0
gpt4_system_prompts = ["You are a helpful assistant"]
api_requests = {}
api_outputs = {}
workflows = []
last_request_id = ""
queue_lock = threading.Lock()
action_queue = []
openrouter_api_key = ""  # Store the OpenRouter API key

# Template strings
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Server Control Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            padding: 20px;
        }
        .btn {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 5px;
            cursor: pointer;
            border-radius: 4px;
        }
        .btn-blue {
            background-color: #2196F3;
        }
        .btn-purple {
            background-color: #9C27B0;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            padding: 10px;
            margin: 5px 0;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        textarea {
            width: 100%;
            min-height: 100px;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            font-family: monospace;
            margin-bottom: 10px;
        }
        .api-key-input {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Multi-Server Control Panel</h1>
    
    <div class="card">
        <h2>Server Management</h2>
        <p>Manage and customize 10 micro servers running on separate ports.</p>
        <a href="/servers" class="btn btn-blue">Manage Servers</a>
    </div>
    
    <div class="card">
        <h2>Code Generation</h2>
        <p>Use OpenRouter API to generate code based on your requirements.</p>
        <input type="text" id="openrouterKey" class="api-key-input" placeholder="Enter your OpenRouter API key" value="{{openrouter_api_key}}">
        <textarea id="codePrompt" placeholder="Describe the code you want to generate...">Create a simple Python function that connects to a PostgreSQL database</textarea>
        <button id="generateBtn" class="btn btn-purple">Generate Code</button>
        <div id="generationResult" style="margin-top: 10px; white-space: pre-wrap; font-family: monospace;"></div>
    </div>
    
    <div class="card">
        <h2>File Upload</h2>
        <p>Upload files to process with the server.</p>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit" class="btn">Upload</button>
        </form>
    </div>
    
    <div class="card">
        <h2>Available Endpoints</h2>
        <ul>
            <li><strong>/agents</strong> - API endpoint for agent interactions</li>
            <li><strong>/upload</strong> - Upload files for processing</li>
            <li><strong>/servers</strong> - Server management interface</li>
            <li><strong>/generate-code</strong> - Generate code using OpenRouter API</li>
        </ul>
    </div>
    
    <script>
        document.getElementById('generateBtn').addEventListener('click', function() {
            const key = document.getElementById('openrouterKey').value.trim();
            const prompt = document.getElementById('codePrompt').value.trim();
            const resultDiv = document.getElementById('generationResult');
            
            if (!key) {
                resultDiv.textContent = "Error: Please enter your OpenRouter API key";
                return;
            }
            
            if (!prompt) {
                resultDiv.textContent = "Error: Please enter a prompt for code generation";
                return;
            }
            
            resultDiv.textContent = "Generating code...";
            
            fetch('/generate-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    api_key: key,
                    prompt: prompt
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultDiv.textContent = "Error: " + data.error;
                } else {
                    resultDiv.textContent = data.result;
                    // Save the API key
                    fetch('/save-api-key', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            api_key: key
                        }),
                    });
                }
            })
            .catch((error) => {
                resultDiv.textContent = "Error: " + error.message;
            });
        });
    </script>
</body>
</html>
"""

SERVERS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Micro Servers Control Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .server-box {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            padding: 20px;
        }
        .server-controls {
            margin: 10px 0 20px;
        }
        button, .btn {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        .stop {
            background-color: #f44336;
        }
        .restart {
            background-color: #2196F3;
        }
        .view {
            background-color: #9C27B0;
        }
        textarea {
            width: 100%;
            height: 300px;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            font-family: monospace;
            margin-bottom: 10px;
        }
        .status-running {
            color: green;
            font-weight: bold;
        }
        .status-stopped {
            color: red;
            font-weight: bold;
        }
        .global-controls {
            margin-bottom: 20px;
        }
        .logs {
            font-family: monospace;
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 4px;
            max-height: 150px;
            overflow-y: auto;
            white-space: pre-wrap;
            margin-top: 10px;
        }
        .code-gen-controls {
            margin-top: 10px;
        }
        .api-key-input {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .code-prompt {
            width: 100%;
            min-height: 80px;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            font-family: monospace;
            margin-bottom: 10px;
        }
        .btn-purple {
            background-color: #9C27B0;
        }
    </style>
</head>
<body>
    <h1>Micro Servers Control Panel</h1>
    
    <div class="global-controls">
        <a href="/restart-all" class="btn restart">Restart All Servers</a>
        <a href="/" class="btn">Back to Home</a>
    </div>
    
    {% for server in servers %}
    <div class="server-box">
        <h2>Server {{ server.id }}</h2>
        <div>
            Port: {{ server.port }} | 
            Status: <span class="status-{% if server.status == 'Running' %}running{% else %}stopped{% endif %}">{{ server.status }}</span>
            {% if server.status == 'Running' %}
            | <a href="http://localhost:{{ server.port }}" target="_blank" class="btn view">View Server</a>
            {% endif %}
        </div>
        
        <div class="server-controls">
            {% if server.status == 'Running' %}
            <a href="/stop/{{ server.id }}" class="btn stop">Stop</a>
            <a href="/restart/{{ server.id }}" class="btn restart">Restart</a>
            {% else %}
            <a href="/start/{{ server.id }}" class="btn">Start</a>
            {% endif %}
        </div>
        
        <form action="/edit/{{ server.id }}" method="post">
            <textarea name="content" id="code-content-{{ server.id }}">{{ server.content }}</textarea>
            
            <div class="code-gen-controls">
                <input type="text" id="openrouterKey-{{ server.id }}" class="api-key-input" placeholder="Enter your OpenRouter API key" value="{{openrouter_api_key}}">
                <textarea id="codePrompt-{{ server.id }}" class="code-prompt" placeholder="Describe improvements or changes to the code...">Improve this server code by adding more routes and better error handling.</textarea>
                <button type="button" onclick="generateServerCode({{ server.id }})" class="btn btn-purple">Generate Code with AI</button>
                <div id="generationResult-{{ server.id }}" style="margin: 10px 0; white-space: pre-wrap; font-family: monospace;"></div>
            </div>
            
            <button type="submit">Save & Apply</button>
        </form>
        
        <div>
            <h3>Logs</h3>
            <div class="logs">{{ server.logs }}</div>
        </div>
    </div>
    {% endfor %}
    
    <script>
        // Auto-refresh the page every 10 seconds to update status
        setTimeout(() => {
            location.reload();
        }, 10000);
        
        function generateServerCode(serverId) {
            const key = document.getElementById(`openrouterKey-${serverId}`).value.trim();
            const prompt = document.getElementById(`codePrompt-${serverId}`).value.trim();
            const codeContent = document.getElementById(`code-content-${serverId}`).value.trim();
            const resultDiv = document.getElementById(`generationResult-${serverId}`);
            
            if (!key) {
                resultDiv.textContent = "Error: Please enter your OpenRouter API key";
                return;
            }
            
            if (!prompt) {
                resultDiv.textContent = "Error: Please enter a prompt for code generation";
                return;
            }
            
            resultDiv.textContent = "Generating improved code...";
            
            fetch('/generate-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    api_key: key,
                    prompt: prompt,
                    current_code: codeContent
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultDiv.textContent = "Error: " + data.error;
                } else {
                    // Update the textarea with the new code
                    document.getElementById(`code-content-${serverId}`).value = data.result;
                    resultDiv.textContent = "Code updated successfully! Don't forget to Save & Apply.";
                    
                    // Save the API key
                    fetch('/save-api-key', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            api_key: key
                        }),
                    });
                }
            })
            .catch((error) => {
                resultDiv.textContent = "Error: " + error.message;
            });
        }
    </script>
</body>
</html>
"""

# Simplest possible micro server template
SIMPLE_SERVER_TEMPLATE = """
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Micro Server {server_id}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h1>Micro Server {server_id} Running</h1>
        <p>This is a customizable micro server running on port {port}.</p>
        <p>Edit your server code in the control panel.</p>
        <p><a href="http://localhost:5000/servers">Back to Control Panel</a></p>
    </body>
    </html>
    '''

@app.route('/hello')
def hello():
    return "Hello from Server {server_id}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port={port}, debug=False)
"""

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_content(file, filename):
    file_extension = filename.rsplit('.', 1)[1].lower()

    if file_extension in ['xlsx', 'xls']:
        df = pd.read_excel(file)
        return df.to_dict()
    elif file_extension == 'csv':
        df = pd.read_csv(file)
        return df.to_dict()
    elif file_extension == 'txt':
        return file.read().decode('utf-8')
    elif file_extension in ['doc', 'docx']:
        doc = docx.Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif file_extension in ['png', 'jpg', 'jpeg', 'gif', 'pdf']:
        return f"Binary file: {filename}"
    else:
        return None

def handle_keypress(action):
    try:
        x = {"saved": action["prompt"], "key": action.get("key", "")}
        if "Current Directory" in str(x["saved"]):
            pyautogui.write(os.getcwd(), interval=0.05)
        if "resource_path" in str(x["key"]).lower():
            pyautogui.write(os.getcwd(), interval=0.05)
        if "backspace" in str(x["key"]).lower():
            pyautogui.press('backspace')
        elif "space" in str(x["key"]).lower():
            pyautogui.write(" ", interval=0.05)
        elif "period" in str(x["key"]).lower():
            pyautogui.write(".", interval=0.05)
        elif "slash" in str(x["key"]).lower():
            pyautogui.write("/", interval=0.05)
        elif "return" in str(x["key"]).lower():
            pyautogui.press('enter')
        elif "shift" in str(x["key"]).lower():
            pyautogui.keyDown("shift")
        elif "ctrl" in str(x["key"]).lower():
            pyautogui.keyDown("ctrl")
        elif "alt" in str(x["key"]).lower():
            pyautogui.keyDown("alt")
        elif "tab" in str(x["key"]).lower():
            pyautogui.keyDown("tab")
        elif "enter" in str(x["key"]).lower():
            pyautogui.press('enter')
        elif action["prompt"] != "Shift":
            pyautogui.typewrite(action["prompt"])
        elif action["prompt"] == "Enter":
            pyautogui.press('enter')
    except Exception as e:
        print(f"Error handling keypress: {str(e)}")

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def create_server_template(server_id, port):
    """Create a basic Flask server template with the server ID and port filled in"""
    return SIMPLE_SERVER_TEMPLATE.format(server_id=server_id, port=port)

def initialize_servers():
    """Initialize server files if they don't exist"""
    for i in range(1, NUM_SERVERS + 1):
        server_file = os.path.join(SERVER_DIR, f'server_{i}.py')
        port = BASE_PORT + i - 1
        if not os.path.exists(server_file):
            with open(server_file, 'w') as f:
                f.write(create_server_template(i, port))

def read_server_logs(server_id):
    """Read the output logs for a server"""
    if server_id in server_logs:
        return server_logs[server_id]
    return "No logs available"

def capture_output(process, server_id):
    """Capture and store output from the server process"""
    global server_logs
    server_logs[server_id] = ""
    max_log_length = 10000  # Maximum log length to keep memory usage reasonable
    
    while server_id in server_processes:
        try:
            output = process.stdout.readline().decode('utf-8')
            if output:
                # Append to logs and truncate if necessary
                server_logs[server_id] += output
                if len(server_logs[server_id]) > max_log_length:
                    server_logs[server_id] = server_logs[server_id][-max_log_length:]
                print(f"Server {server_id}: {output}", end='')
        except Exception as e:
            print(f"Error reading server {server_id} output: {str(e)}")
            break
        time.sleep(0.1)  # Small delay to prevent CPU hogging

def start_server(server_id):
    """Start a micro server with the given ID"""
    port = BASE_PORT + server_id - 1
    server_file = os.path.join(SERVER_DIR, f'server_{server_id}.py')
    
    # Check if the port is already in use
    if is_port_in_use(port) and server_id not in server_processes:
        print(f"Warning: Port {port} is already in use but not tracked by this application")
    
    # Kill any existing process on this port
    stop_server(server_id)
    
    # Start the new server process
    try:
        process = subprocess.Popen(
            [sys.executable, server_file, str(port)], 
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=False,
            bufsize=1,
            universal_newlines=False
        )
        
        server_processes[server_id] = {
            'process': process,
            'port': port,
            'started': time.time()
        }
        
        # Start a thread to capture output
        output_thread = threading.Thread(
            target=capture_output, 
            args=(process, server_id),
            daemon=True
        )
        output_thread.start()
        
        # Give it a moment to start
        time.sleep(1)
        return port
    except Exception as e:
        print(f"Error starting server {server_id}: {str(e)}")
        server_logs[server_id] = f"Failed to start: {str(e)}"
        return None

def stop_server(server_id):
    """Stop a running server process"""
    if server_id in server_processes:
        try:
            server_processes[server_id]['process'].terminate()
            server_processes[server_id]['process'].wait(timeout=5)
        except (subprocess.TimeoutExpired, Exception) as e:
            try:
                server_processes[server_id]['process'].kill()
            except Exception as kill_error:
                print(f"Error killing server {server_id}: {str(kill_error)}")
        server_processes.pop(server_id, None)
        return True
    return False

def stop_all_servers():
    """Stop all running server processes"""
    for server_id in list(server_processes.keys()):
        stop_server(server_id)

def call_openrouter_api(api_key, prompt, current_code=None):
    """Call the OpenRouter API to generate code based on the prompt"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    if current_code:
        content_text = f"I need to improve or change this Python code based on this requirement: '{prompt}'. Here's the current code:\n\n```python\n{current_code}\n```\n\nPlease provide the complete improved version of this code, with proper comments. Only return the code, without any other explanation. Make sure it works by minimally updating this code and keeping all the same interfaces and functioanlity"
    else:
        content_text = f"I need to write Python code based on this requirement: '{prompt}'. Please provide complete, well-commented code that addresses this requirement. Only return the code, without any other explanation."
    
    payload = {
        "model": "anthropic/claude-3.7-sonnet",
        "messages": [
            {
                "role": "user",
                "content": content_text
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        if 'choices' in data and len(data['choices']) > 0:
            message_content = data['choices'][0]['message']['content']
            
            # Extract code from response if it contains markdown code blocks
            if "```python" in message_content and "```" in message_content:
                # Extract the code between the first ```python and the next ```
                start = message_content.find("```python") + len("```python")
                if start < len("```python"):  # If ```python isn't found, try just ```
                    start = message_content.find("```") + len("```")
                end = message_content.find("```", start)
                
                if start < end:
                    return message_content[start:end].strip()
                    
            # If no code block is found or extraction fails, return the full message
            return message_content
        else:
            return "No response generated by the API"
            
    except requests.exceptions.RequestException as e:
        return f"Error calling OpenRouter API: {str(e)}"

# Register cleanup function
atexit.register(stop_all_servers)

# Routes
@app_calls.route('/')
def main_index():
    """Main index page that links to servers and other functionality"""
    return render_template_string(INDEX_HTML, openrouter_api_key=openrouter_api_key)

@app_calls.route('/servers')
def servers_list():
    """List all servers with status and editing capability"""
    servers = []
    for i in range(1, NUM_SERVERS + 1):
        port = BASE_PORT + i - 1
        status = "Running" if i in server_processes else "Stopped"
        
        # Read the server file content
        server_file = os.path.join(SERVER_DIR, f'server_{i}.py')
        with open(server_file, 'r') as f:
            content = f.read()
            
        servers.append({
            'id': i,
            'port': port,
            'status': status,
            'content': content,
            'logs': read_server_logs(i)
        })
    
    return render_template_string(SERVERS_HTML, servers=servers, openrouter_api_key=openrouter_api_key)

@app_calls.route('/start/<int:server_id>')
def start_server_route(server_id):
    """Start a micro server"""
    if 1 <= server_id <= NUM_SERVERS:
        port = start_server(server_id)
        if port and is_port_in_use(port):
            print(f"Server {server_id} started successfully on port {port}")
        else:
            print(f"Server {server_id} may have failed to start properly")
    return redirect(url_for('servers_list'))

@app_calls.route('/stop/<int:server_id>')
def stop_server_route(server_id):
    """Stop a micro server"""
    if 1 <= server_id <= NUM_SERVERS:
        if stop_server(server_id):
            print(f"Server {server_id} stopped successfully")
        else:
            print(f"Server {server_id} was not running")
    return redirect(url_for('servers_list'))

@app_calls.route('/restart/<int:server_id>')
def restart_server_route(server_id):
    """Restart a micro server"""
    if 1 <= server_id <= NUM_SERVERS:
        stop_server(server_id)
        time.sleep(1)  # Give it a moment to fully stop
        port = start_server(server_id)
        if port and is_port_in_use(port):
            print(f"Server {server_id} restarted successfully on port {port}")
        else:
            print(f"Server {server_id} may have failed to restart properly")
    return redirect(url_for('servers_list'))

@app_calls.route('/restart-all')
def restart_all_servers():
    """Restart all micro servers"""
    stop_all_servers()
    time.sleep(1)  # Give them a moment to fully stop
    for i in range(1, NUM_SERVERS + 1):
        port = start_server(i)
        if port and is_port_in_use(port):
            print(f"Server {i} restarted successfully on port {port}")
        else:
            print(f"Server {i} may have failed to restart properly")
    return redirect(url_for('servers_list'))

@app_calls.route('/edit/<int:server_id>', methods=['POST'])
def edit_server(server_id):
    """Edit a server file"""
    if 1 <= server_id <= NUM_SERVERS:
        content = request.form.get('content', '')
        server_file = os.path.join(SERVER_DIR, f'server_{server_id}.py')
        
        # Save the new content
        with open(server_file, 'w') as f:
            f.write(content)
        
        # Restart the server if it's running
        if server_id in server_processes:
            stop_server(server_id)
            time.sleep(1)  # Give it a moment to fully stop
            port = start_server(server_id)
            if port and is_port_in_use(port):
                print(f"Server {server_id} restarted with new code on port {port}")
            else:
                print(f"Server {server_id} may have failed to restart with new code")
                
    return redirect(url_for('servers_list'))

@app_calls.route('/status')
def get_status():
    """Get the status of all servers as JSON"""
    status = {}
    for i in range(1, NUM_SERVERS + 1):
        port = BASE_PORT + i - 1
        running = i in server_processes
        port_in_use = is_port_in_use(port)
        
        status[f'server_{i}'] = {
            'running': running,
            'port': port,
            'port_in_use': port_in_use,
            'uptime': time.time() - server_processes[i]['started'] if running else 0
        }
    
    return jsonify(status)

@app_calls.route('/generate-code', methods=['POST'])
def generate_code():
    """Generate code using the OpenRouter API"""
    try:
        data = request.json
        api_key = data.get('api_key')
        prompt = data.get('prompt')
        current_code = data.get('current_code')  # This is optional
        
        if not api_key:
            return jsonify({'error': 'API key is required'})
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'})
        
        # Call the OpenRouter API
        result = call_openrouter_api(api_key, prompt, current_code)
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app_calls.route('/save-api-key', methods=['POST'])
def save_api_key():
    """Save the OpenRouter API key for future use"""
    global openrouter_api_key
    try:
        data = request.json
        api_key = data.get('api_key')
        
        if api_key:
            openrouter_api_key = api_key
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'No API key provided'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app_calls.route("/agents", methods=['GET', 'POST'])
def agents():
    global last_request_id, user_key
    try:
        json_data = request.json
        print(json_data)
        
        # Set a default key for testing if needed
        request_key = json_data.get("key", "")
        if user_key == "" and request_key != "":
            user_key = request_key
            print(f"Setting user_key to {user_key}")
        
        print(f"Request key: {request_key}, User key: {user_key}")
        
        if request_key == user_key:
            print("KEY MATCH")
            agent_data = {}
            json_output = json_data["json_output"]
            
            # Generate random ID
            import random
            import string
            id_api = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            last_request_id = id_api
            api_requests[str(id_api)] = "pending"
            print(f"Request ID: {id_api}")
            print("PROCESSING NODES")
            
            if json_output[0]["type"] == "cookies":
                cookie_string = json_output[0]["file"]
                print(cookie_string)
    
                with open('cookies.txt', 'w') as file:
                    file.write(cookie_string.strip())
                
                print("SAVED COOKIES")
                
                api_requests[id_api] = "done"
                api_outputs[id_api] = "Cookies saved successfully"
                
            elif json_output[0]["type"] == "cheat_file":
                api_requests[id_api] = "done"
                api_outputs[id_api] = "Cheat file processed"
                
            elif json_output[0]["type"] == "click_direct":
                # Add click to queue
                with queue_lock:
                    action_queue.append({
                        "type": "click",
                        "x": json_output[0]["x"],
                        "y": json_output[0]["y"]
                    })
                
                api_requests[id_api] = "done"
                api_outputs[id_api] = "Click action queued"
            
            elif json_output[0]["type"] == "keypress_direct":
                # Add keypress to queue
                with queue_lock:
                    action_queue.append({
                        "type": "keypress",
                        "prompt": json_output[0]["prompt"],
                        "key": json_output[0].get("key", "")
                    })
                
                api_requests[id_api] = "done"
                api_outputs[id_api] = "Keypress action queued"
    
            elif json_output[0]["type"] == "move_direct":
                # Add move to queue
                with queue_lock:
                    if json_output[0]["x"] > 10 and json_output[0]["y"] > 10:
                        action_queue.append({
                            "type": "move",
                            "x": json_output[0]["x"],
                            "y": json_output[0]["y"]
                        })
                api_requests[id_api] = "done"
                api_outputs[id_api] = "Move action queued"
    
            else:
                api_requests[id_api] = "done"
                api_outputs[id_api] = "Unknown action type"
    
            # Wait for processing to complete
            wait_count = 0
            while api_requests[id_api] == "pending" and wait_count < 30:  # Wait up to 30 seconds
                time.sleep(1)
                wait_count += 1
    
            agent_data = api_outputs.get(id_api, "Processing timed out")
            return str(agent_data)
        else:
            return "Invalid key"
    except Exception as e:
        return f"Error in agents endpoint: {str(e)}"

@app_calls.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app_calls.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        file_contents = {}

        if filename.lower().endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if not file_info.filename.endswith('/'):  # Skip directories
                        with zip_ref.open(file_info) as file_in_zip:
                            content = read_file_content(file_in_zip, file_info.filename)
                            if content is not None:
                                file_contents[file_info.filename] = content
        else:
            with open(file_path, 'rb') as f:
                content = read_file_content(f, filename)
                if content is not None:
                    file_contents[filename] = content

        if not file_contents:
            return jsonify({'error': 'No readable content found in the uploaded file(s)'}), 400

        # Return the file contents
        return jsonify(file_contents)
    return jsonify({'error': 'File type not allowed'}), 400

# Action processor thread
def process_actions():
    while True:
        try:
            with queue_lock:
                if action_queue:
                    action = action_queue.pop(0)
                    if action["type"] == "click":
                        pyautogui.click(action["x"], action["y"])
                    elif action["type"] == "move":
                        pyautogui.moveTo(action["x"], action["y"])
                    elif action["type"] == "keypress":
                        handle_keypress(action)
        except Exception as e:
            print(f"Error processing action: {str(e)}")
        time.sleep(0.1)  # Small delay to prevent CPU hogging

def run_server():
    while True:
        try:
            print(f"Starting main server at {datetime.now()}")
            app_calls.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        except Exception as e:
            print(f"Server crashed at {datetime.now()} with error: {str(e)}")
            print("Restarting server in 5 seconds...")
            time.sleep(5)  # Wait 5 seconds before restarting

if __name__ == "__main__":
    # Initialize server files
    initialize_servers()
    
    # Start the action processor thread
    action_thread = threading.Thread(target=process_actions, daemon=True)
    action_thread.start()
    
    # Start all servers
    print("Starting micro servers...")
    for i in range(1, NUM_SERVERS + 1):
        try:
            port = start_server(i)
            if port:
                print(f"Started server {i} on port {port}")
            else:
                print(f"Failed to start server {i}")
        except Exception as e:
            print(f"Error starting server {i}: {str(e)}")
    
    # Run the main server
    run_server()
