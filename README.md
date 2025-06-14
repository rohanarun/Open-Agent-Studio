# Open Agent Studio 

Open Agent Studio is the first cross platform desktop application built to enable Agentic Process Automation as an open-source alternative and replacement for UIpath and all other RPA tools today. 

Download for Windows and Mac at https://cheatlayer.com .

We founded Cheat Layer during the pandemic to help people who had lost their jobs and businesses rebuild online using GPT-3. We personally helped hundreds pro bono before turning to AI for help.

In August 2021, we were the first startup to get approved by openAI to sell GPT-3 for automation. 

Businesses today are threatening to fire employees and replace them with AI. We believe within 2 years, the AI necessary to generate most of those businesses will be a commodity.

In a future where the AI in your pocket can generate custom, secure, and free versions of all the most expensive business software, we believe there'll be a level playing field that removes the barrier to build these businesses. More small businesses will build competitive brands through personal relationships, better quality service, and network effects through unique data. We invite you to join us in building this future together faster.

## Windows Install instructions:


[![Windows Install Instructions!](https://img.youtube.com/vi/gsU5033ms5k/0.jpg)](https://www.youtube.com/watch?v=8xhFKkD4H-0)


https://www.youtube.com/watch?v=8xhFKkD4H-0

## Introducing The World's First Video To Agents!
[![Introducing The World's First Video To Agents!](https://img.youtube.com/vi/gsU5033ms5k/0.jpg)](https://www.youtube.com/watch?v=gsU5033ms5k)


## Agentic Process Automation
![Generalized Agents framework](https://storage.googleapis.com/cheatlayer/agent.png)
![image](https://github.com/user-attachments/assets/ff792176-c3cc-41df-bbaf-8728e7520540)


### Semantic Targets

We were the first startup to invent the idea of "semantic targets" using LLMs before ChatGPT was launched. Semantic targets and agentic process automation was a concept we introduced to replace brittle code selectors and computer vision in 2022. You can see the code for semantic targets in this repo starting  2 years ago, and were approved by openAI to sell GPT-3 for autoamtion as the first startup in 2021. 

Semantic targets distils the underlying intent of a target to english, so they still work even if services completely change their designs. This enables building robust, future-proof, agents. 

Semantic targets can be dynamic or robust based on how strict the language is. 

### Semantic Triggers
![Semantic Triggers](https://storage.googleapis.com/cheatlayer/semtriggers.png)

### Reasoning Based Targets
![Reasoning Based Targets](https://storage.googleapis.com/cheatlayer/reasoning.png)  

## Agents API
The Agents API now runs on every Open Agent Studio instance. An easy way to test this is to run Ngrok locally, or use Open Agent Studio which publishes a public IP address you can use as your personal Agents API. 
![Agents API](https://storage.googleapis.com/cheatlayer/agents_api.png)
It even returns all the saved agent data during the automation, plus the verification testing loop steps we use to verify each action. 

<h1>Key Concepts</h1>

<b>Nodes:</b> Individual actions an agent can perform
<b>Variables:</b>  Data that can be passed between nodes
<b>Verification:</b>  Checking if a node's action was successful
<b>Global Variables:</b>  Shared data accessible across all nodes

<h1>POST /agents</h1>
Creates and runs a new agent based on the provided JSON configuration.

Request Body
```

{
  "key": "your_api_key",
  "json_output": [
    {
      "type": "action_type",
      "parameters": "action_specific_parameters"
    },
    ...
  ],
  "goal": "description_of_agent_goal"
}
```
Response
Returns a string representation of the agent's output data after executing all actions.

<h1>Agent Node Types</h1>

<h2>Browser Automation</h2>

<b>Delay</b>

Pauses execution for a specified time.

<ParamField body="time" type="number"> The time to pause in seconds </ParamField> 
```
json { "type": "delay", "time": 5 } 
``` 
<b>Keypress</b>

Types text or presses a key.

<ParamField body="prompt" type="string"> The text to type or key to press </ParamField>  
```
{ "type": "keypress", "prompt": "Hello, World!" } 
``` 

<b>Click</b>

Clicks on a specified target.

<ParamField body="target" type="string"> Description of element to click in simple language</ParamField> <ParamField body="browser_mode" type="boolean" optional> Set to true for browser-specific clicks </ParamField> 
```
json { "type": "click", "target": "Submit button", "browser_mode": true } 
``` 
<b>Open Tab</b>

Opens a new browser tab.

<ParamField body="target" type="string"> URL to open </ParamField> 
```
json { "type": "open tab", "target": "https://www.example.com" } 
``` 
<h2>Data Processing</h2>

<b>GPT4</b>

Uses GPT-4 for natural language processing.

<ParamField body="prompt" type="string"> System message for GPT-4 </ParamField> <ParamField body="input" type="array"> Array of input data keys </ParamField> <ParamField body="data" type="string"> Output variable key </ParamField> 
```
json { "type": "gpt4", "prompt": "Summarize the following text:", "input": ["article_text"], "data": "summary" } 
``` 
<b>Python</b>

Executes custom Python code.

<ParamField body="code" type="string"> Python code to execute </ParamField> 
```
json { "type": "python", "code": "import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.head())" } 
``` 
<b>Bash</b>

Executes bash commands.

<ParamField body="command" type="string"> Bash command to execute </ParamField> 
```
json { "type": "bash", "command": "ls -la" } 
``` 
<h2>Integrations</h2>

<b>Google Sheets Create</b>

Creates a new Google Sheet.

<ParamField body="URL" type="string"> Variable to store sheet URL </ParamField> <ParamField body="Sheet_Name" type="string"> Variable to store sheet name </ParamField> 
```
json { "type": "google_sheets_create", "URL": "new_sheet_url", "Sheet_Name": "new_sheet_name" } 
``` 
<b>Google Sheets Add Row</b>

Adds a row to a Google Sheet.

<ParamField body="URL" type="string"> Sheet URL variable </ParamField> <ParamField body="Sheet_Name" type="string"> Sheet name variable </ParamField> <ParamField body="data" type="array"> Array of data to add </ParamField> 
```
json { "type": "google_sheets_add_row", "URL": "sheet_url", "Sheet_Name": "sheet_name", "data": ["John", "Doe", "30"] } 
``` 
<b>Google Sheets Read</b>


Reads data from a Google Sheet.

<ParamField body="URL" type="string"> Sheet URL </ParamField> <ParamField body="Sheet_Name" type="string"> Sheet name </ParamField> <ParamField body="data" type="string"> Variable to store read data </ParamField> 
```
json { "type": "google_sheets_read", "URL": "sheet_url", "Sheet_Name": "sheet_name", "data": "sheet_data" } 
``` 
<b>Email</b>

Sends an email.

<ParamField body="to" type="string"> Recipient email </ParamField> <ParamField body="subject" type="string"> Email subject </ParamField> <ParamField body="body" type="string"> Email body </ParamField> <ParamField body="data" type="string"> Variable containing additional data to append </ParamField> 
```
json { "type": "email", "to": "recipient@example.com", "subject": "Monthly Report", "body": "Please find the monthly report attached.", "data": "report_data" } 
``` 
<b>API</b>


Makes an API call.

<ParamField body="URL" type="string"> API endpoint </ParamField> <ParamField body="headers" type="object"> Request headers </ParamField> <ParamField body="body" type="object"> Request body </ParamField> <ParamField body="data" type="string" optional> Variable containing data to send </ParamField> <ParamField body="output" type="string" optional> Variable to store response </ParamField> 
```
json { "type": "api", "URL": "https://api.example.com/data", "headers": {"Content-Type": "application/json"}, "body": {"key": "value"}, "data": "request_data", "output": "api_response" } 
``` 
<h2>Utility</h2>


<b>Add Data</b>


Loads data from various file types.

<ParamField body="target" type="string"> Variable to store data </ParamField> <ParamField body="data" type="string"> File path </ParamField> 
```
json { "type": "add_data", "target": "csv_data", "data": "/path/to/file.csv" } 
``` 
<b>Schedule</b>

Schedules the agent to run at specified times.

<ParamField body="cron" type="string"> Cron expression for scheduling </ParamField> 
```
json { "type": "schedule", "cron": "0 9 * * 1-5" } 
``` 
<b>Generalized Agent</b>


Performs a generalized action based on a description using our state machine to solve open-ended problems.

<ParamField body="description" type="string"> Action to perform </ParamField> 
```
json { "type": "general", "description": "Search for the latest news articles about AI and summarize them" } 
``` 
<b>Semantic Scrape</b>

Scrapes data based on a semantic description.

<ParamField body="target" type="string"> Description of data to scrape </ParamField> <ParamField body="data" type="string"> Variable to store scraped data </ParamField> 
```
json { "type": "semanticScrape", "target": "product reviews and ratings", "data": "product_reviews" } 
``` 
Complete Example: Web Scraping and Data Processing Agent

```
json { "key": "your_api_key", "json_output": [ { "type": "open tab", "target": "https://example.com/products" }, { "type": "delay", "time": 5 }, { "type": "semanticScrape", "target": "product listings", "data": "product_data" }, { "type": "gpt4", "prompt": "Analyze the product data and summarize the findings", "input": ["product_data"], "data": "analysis_result" }, { "type": "google_sheets_create", "URL": "sheet_url", "Sheet_Name": "sheet_name" }, { "type": "google_sheets_add_row", "URL": "sheet_url", "Sheet_Name": "sheet_name", "data": ["analysis_result"] }, { "type": "email", "to": "manager@company.com", "subject": "Product Analysis Report", "body": "Please find the latest product analysis attached.", "data": "analysis_result" } ], "goal": "Scrape product data, analyze it, save to Google Sheets, and email the results" } 
``` 
Best Practices

1) Use descriptive names for variables to make the workflow clear.
2) Add appropriate delays between actions to allow for page loading.
3) Handle errors gracefully by checking node verification results.
4) Use GPT-4 nodes to add flexibility and intelligence to your agents.
5) Leverage integrations like Google Sheets for data storage and sharing.
6) When using the python node, ensure all necessary libraries are imported.
7) For file operations in the add_data node, ensure file paths are correct and accessible.
8) When scheduling agents with the schedule node, use correct cron syntax.
9) For API calls, double-check URL, headers, and body parameters.
10) Use the general node for complex actions that may require multiple steps.

By following this documentation, you can create sophisticated automated agents capable of handling a wide range of tasks across multiple platforms and services. The Agents API provides a flexible and powerful framework for defining complex sequences of actions, data processing, and integrations.


## No-Code Actions

This documentation details Open Agent Studio's no-code actions, designed to build powerful desktop automations without writing code. Each action is described along with its input parameters and an example use case.

### 1. Start Node

**Icon:** 

**Description:**  Initiates the automation process by opening a specified application or a URL.

**Input Parameters:**

- **Initial Program:** The path to the program's executable (e.g., "C:\Program Files\Google\Chrome\Application\chrome.exe").
- **Arguments:**  Additional commands for the program, often a URL for a web browser.
- **Data:** Stores the node's settings in JSON format.

**Example Use Case:**  To begin your automation by opening the Cheat Layer website, put your browser's path in "Initial Program" and "https://cheatlayer.com" in "Arguments".

### 2. Move Mouse

**Icon:** 
**Description:**  Moves the mouse cursor to precise coordinates on your screen.

**Input Parameters:**

- **X Coordinate:** Horizontal position (pixels).
- **Y Coordinate:**  Vertical position (pixels).

**Example Use Case:**  Place the cursor over a specific area within an application before clicking or typing.

### 3. Magic Clicker

**Icon:** 

**Description:**  Simulates various mouse click types, either by coordinates or using semantic targeting of elements.

**Input Parameters:**

- **Automation Input:**  Allows for dynamic clicks based on global variables or inputs from "phone_transcript", "email_transcript", or "sms_transcript".
- **X:** Horizontal coordinate (pixels).
- **Y:** Vertical coordinate (pixels).
- **Click Type:**  
    - "Single Left Click": Standard click.
    - "Single Right Click": For opening right-click menus. 
    - "Double Click": For opening files or selecting text.
    - "Drag":  Click and hold for moving elements. 
- **Mode:** 
    - **Desktop:** Clicks are based on "X" and "Y" coordinates.
    - **Browser:**  Targets elements within the web browser using a semantic description ("Target In English").
    - **First/Last:** If there are multiple matches, clicks the first or last matching element.
    - **Loop Total Runs/Loop Node Runs:**   Repeats the click a set number of times or based on the number of times this node has run.
- **Target In English:** Describe the web element to be clicked (e.g., "Download button," "Menu link").
- **Data:** Node settings in JSON.

**Example Use Cases:**

- Click a button on a form:  Set "Mode" to "Browser", describe the button in "Target In English".
- Click a specific area in an application: Use "Desktop" mode and "X", "Y" coordinates. 

### 4. Keypress

**Icon:** 

**Description:** Automates keyboard input, sending keystrokes and typing text to the active window.

**Input Parameters:**

- **String:**  The key or character sequence to type (e.g., "enter", "Hello, World!").
- **Saved Values:**  Provides a quick option to type the current directory path. 
- **GPT-4 Mode:** Let GPT-4 process the "String" before the keypress, enabling dynamic content generation.
- **Automation Input:** Use a global variable to define the keystroke sequence. 
- **Data:** Node settings in JSON.

We support the following keyboard keys if you enter them only into the string input:
| Input String                      | Output Action       |
|------------------------------------|---------------------|
| "Current Directory"        | Write resource path |
| "resource_path"             | Write resource path |
| "backspace"                  | Press backspace     |
| "space"                      | Write space         |
| "period"                     | Write period (.)    |
| "slash"                      | Write slash (/)     |
| "return"                     | Press enter         |
| "shift"                      | Hold shift key      |
| "ctrl"                       | Hold ctrl key       |
| "alt"                        | Hold alt key        |
| "tab"                        | Hold tab key        |
| "enter"                      | Press enter         |

**Example Use Cases:**

-  Press Enter to submit a form:  Set "String" to "enter".
- Type a message into a document: Provide the text in the "String" parameter.

### 5. Delay

**Icon:** 

**Description:**  Introduces a pause in the automation to allow time for websites to load, processes to complete, etc.

**Input Parameters:**

- **seconds:** The duration of the pause expressed in seconds.

**Example Use Case:** Wait for a web page to load after clicking a link before trying to interact with it.

### 6. Open Program

**Icon:** 

**Description:** Opens a specified program on your computer with optional arguments.

**Input Parameters:**

- **program:** The path to the application's executable file (e.g., "C:\Program Files\Notepad++\notepad++.exe").
- **arguments:** (Optional) Parameters to pass to the program.  For a web browser, this would be the URL.
- **Automated Input:** You can dynamically define the program and arguments using a global variable.
- **Data:** Node settings in JSON. 

**Example Use Case:** Open a website in Chrome by setting "program" to your Chrome executable path and "Arguments" to "https://www.example.com".

### 7. Bash

**Icon:** 

**Description:**  Executes a bash command in your operating system's terminal.

**Input Parameters:**

- **command:** The bash command you want to be executed,  including any necessary arguments.

**Example Use Case:**  Run a command to update a system package:  `sudo apt-get update`

### 8. Python Code

**Icon:** 

**Description:**  Embed custom Python code directly into your workflow to add complex logic or interact with external libraries. 

**Input Parameters:**

- **code:** The Python code block to execute.

**Special Features:**

- **Dynamic Variable Substitution:** Placeholders like `{{my_variable}}` will be replaced by the corresponding values from your global variables.
- **Access to Internal Functions:**  Your code can access Open Agent Studio's internal functions to send notifications, manage variables, and more.

**Example Use Cases:** 

- **Data Processing:** Clean and manipulate data scraped from a website (e.g., extract specific values, format text). 
- **API Integration:**  Interact with external web services by making API calls and handling the results.

### 9. Magic Scraper (Semantic Scrape)

**Icon:** 

**Description:**  Describes a targeted region of a screenshot using AI. This provides a way  to dynamically identify web elements, even if their visual presentation changes.

**Input Parameters:**

- **Target In English:** Describe in plain English what you want to target (e.g., "The blue button that says 'Next'",  "The product image in the corner").
- **Automation Input:** If needed, you can provide the description dynamically using a global variable. 
- **Scrape Browser:** When used with web automations,  lets you specify the type of web elements to analyze (e.g., "Buttons").
- **Data:** Node settings in JSON.

**Example Use Case:**  Accurately target a button that has a varying position or changes its appearance from time to time.

-  **Extract pricing data from an e-commerce website:**  Use a description like "prices of all the laptops."
-  **Collect article titles from a news website:**  Use "article" as the "Target" and a description like "headlines of all articles."


### 11. Print

**Icon:**  ![](https://cheatlayer.com/static/media/printer.d42c85e3.svg)

**Description:** Displays the value of a specific global variable in Open Agent Studio's console for debugging.

**Input Parameters:**

- ** Variables:** Select the global variable whose contents you want to see in the console output.

**Example Use Case:**   Ensure that data scraped from a website has been stored correctly in a global variable before using it in another action. 

### 12. Scroll

**Icon:** ![](https://cheatlayer.com/static/media/arrows-scroll-vertical.e77e4c20.svg)

**Description:**  Automates the scrolling of a window - primarily useful for web pages. 

**Input Parameters:**

- **Distance:**  Specifies the amount of scrolling, with positive values scrolling down and negative values scrolling up.

**Example Use Case:**  Scroll to the bottom of a long web page to reveal more content to be scraped.

### 13. Send Data

**Icon:** ![](https://cheatlayer.com/static/media/arrow-up-right-from-square.1693d318.svg)

**Description:** Sends data to an external application or webhook using HTTP requests. Enables integration with web services.

**Input Parameters:**

- **Body Key 1/ Body Value 1 ... **:  These key-value pairs represent the data you want to send, with keys acting as labels.
- **Request:** Typically "POST" for sending data.
- **URL:** The web address to send the data to (e.g., a webhook URL, API endpoint).

**Example Use Cases: **

- **Add data to a Google Sheet:** Send the data to a special URL provided by Google Sheets.
- **Trigger an action in another application:** Send data to a webhook configured to receive data and initiate a task. 

### 14. If Else

**Icon:** ![](https://cheatlayer.com/static/media/code-branch.6c47396c.svg)

**Description:**  Adds conditional logic to your automations, letting the agent make choices based on data or conditions. 

**Input Parameters:**

- **Variables:**  The global variable to be evaluated. 
- **operator**: 
    - `includes`: Checks if one string contains another.
    -  `equals`: Tests for an exact match. 
    - `greater than / less than`:  For numerical comparisons.
    -  `regex match`:  Uses regular expressions for more complex pattern matching. 
- **condition:** The criteria to check against the "Variables" (e.g., a specific string, a number, a regular expression).

**Example Use Case:** You're scraping a webpage. If the text "Out of Stock" is found, you might want to trigger one set of actions, and a different set if its "In Stock'.

### 15. Generalized Agent

**Icon:** ![](https://cheatlayer.com/static/media/robot.c5110a8d.svg)

**Description:** Execute a pre-built automation agent — a self-contained automation flow — as a step within your larger workflow.  

**Input Parameters:**

- **prompt:** A brief description of the task you want the generalized agent to handle (e.g., "send a confirmation email", "upload a file to Dropbox," "check for new updates," "open a Google Sheet").  

**Example Use Case:**   You've downloaded a file. Use a Generalized Agent to automate the process of uploading it to your chosen cloud storage provider.

### 16. Google Sheets

**Icon:**  

**Description:**  Reads or writes data to and from Google Sheets,  ideal for storing scraped information, managing lists, or dynamic input.

**Input Parameters:**

- **URL:** The web address of your Google Sheet (including the sheet ID).
- **Read/Write:**  Choose whether you want to "Read" data from or "Write" data to the sheet.
- **sheet name:**  The name of the specific sheet tab (worksheet) within your Spreadsheet. 
- **Row 1 / Row 2 ... **:  (For writing) Define which data variables go into each row.  (For reading) Define which rows to read from.

**Example Use Cases:**

- Log scraped product data in a Google Sheet.
- Read a list of URLs from a Google Sheet as input for further automation actions. 

### 17. Email

**Icon:** ![](https://cheatlayer.com/static/media/envelope.e39582a8.svg)

**Description:**  Sends an email message with optional attachments.

**Input Parameters:**

- **to**:  The email address of the recipient.
- **to variable:**  Select a global variable that holds the recipient's email address (useful for dynamic emails). 
- **subject**: Subject line of the email.
- **body**:  The main content (message) of the email.
- **Body variable**:  Select a global variable containing additional email content if needed.
- **file**:  (Optional)  Path to the file that should be attached to the email.

**Example Use Case:** Alert yourself by email when a specific condition is met during automation, such as a product becoming available. 

Okay, here is the documentation for the remaining no-code actions.


### 18. Math

**Icon:** ![](https://cheatlayer.com/static/media/calculator.56001a7c.svg)

**Description::** Perform basic arithmetic operations within your workflow.

**Input Parameters:**

- **action:** Select the operation (add, subtract,  multiply, divide).
- **input:** A global variable containing the first number for the operation.
- **value:** Either a number or another global variable containing the second number.

**Example Use Case:**  Calculate discounts on e-commerce prices by subtracting a percentage.  

### 19. Get Data

**Icon:** ![](https://cheatlayer.com/static/media/arrow-down-to-square.e6db1d76.svg)

**Description:** Retrieves data from a URL, including web pages, APIs, or local files. 

**Input Parameters:**

- **URL:**  The URL or file path of the data you want to fetch.
- **Headers:** (Optional)   Headers to include in the HTTP request, formatted as JSON (useful for API authentication or specifying content types).  

**Example Use Cases:**

- **Get Data from a website:**  Fetch the HTML content of a webpage.
- **Call an API:**  Get data from an API endpoint.

### 20. Download

**Icon:** ![](https://cheatlayer.com/static/media/download.62b3f24e.svg)


**Description:**  Downloads a file from a URL to your computer.

**Input Parameters:**

- **URL or File:**  The URL of the file to download or the path to a file if you want to open it.
- **Download Location:** The path on your computer where the downloaded file will be saved.
- **Headers:** (Optional)  HTTP headers, formatted as JSON.

**Example Use Case:** Automate the process of downloading a file from a remote server. 

### 21. Screenshot

**Icon:** ![](https://cheatlayer.com/static/media/image.0152d78e.svg)

**Description:** Captures a screenshot of your entire screen or a specified region.

**Input Parameters:**

- **Location:** The complete path where you want the screenshot file to be saved (e.g., "C:\screenshots\my_screenshot.png").

**Example Use Case:** Document the state of your desktop during automation or capture images for visual analysis.


### 22. Webcam

**Icon:**  ![](https://cheatlayer.com/static/media/camera.75221914.svg) 

**Description:**  Captures an image from a connected webcam, saving the image to your computer.

**Input Parameters:**

-  **File Name:**  The name the captured image will be saved as (e.g.,  "webcam_capture.jpg").

 **Example Use Case:** You could integrate webcam captures into a workflow that analyzes images for visual inspection tasks or for gathering visual data. 

### 23. Synthetic Video  

**Icon:** 

 **Description:**  Generates videos based on text descriptions, using a variation of Stable Diffusion optimized for dynamic video content (requires Replicate API integration).

**Input Parameters:**

- **prompt:** A detailed text description of the video you want to create. The more specific, the better (e.g.,  "a robot exploring a futuristic cityscape at night").
- **motion bucket:**  Selects a category of motion to apply to your video (these motion buckets come from Replicate. You can find details on Replicate's model page). 
- **file:**  The filename to save the generated video as.
- **Automation Input:**  If your description is generated earlier in the workflow, you can use a variable here. 
- **frames:**  Determines the number of frames and the technique used for generating video frames. Options like "25_frames_with_svd_xt" are from Replicate. Please check the Replicate model page for updated options. 
- **resolution:**  
    -  `maintain_aspect_ratio`: Keeps the original dimensions. 
    -  `crop_to_16_9`:  Fits video into a 16:9 widescreen format.
    -  `use_image_dimensions` : If your input is an image, the generated video will use its dimensions.

**Example Use Cases:**

- **Create animated product demos:**  Describe your product in action. 
- **Generate short, conceptual videos:** Experiment with visual ideas or illustrate concepts for educational content. 


### 24. GPT-4 

**Icon:** 

**Description:**  Leverage the power of OpenAI's GPT-4 language model for advanced language processing and content creation.

**Input Parameters:**

- **input:** The text you want GPT-4 to work with. 
- **Automation Input:**  If the input comes from previous actions in your automation, select a global variable here.
- **Webhook Input:**  Configure how data is handled if the node is triggered by a webhook.
- **type output:** If set to true, GPT-4's output will be treated as code, ready for execution.

**Example Use Cases:**

- **Content Generation:**  Create blog posts, write stories, poems, or scripts for videos. 
- **Data Summarization:**  Condensing lengthy articles into digestible summaries. 
- **Code Writing:** GPT-4 can be used to generate code snippets or write entire programs.
- **Chatbots:**  Build AI-powered chatbots that interact naturally with users.

### 25. General (Project Atlas)

**Icon:** 

**Description:**  Describes the task you want to automate in plain English and lets the Cheat Layer AI (Project Atlas) figure out how to execute it, using its knowledge of UI patterns and web elements.

**Input Parameters:**

-  **prompt:**  Tell Project Atlas what you want it to do using clear and specific language. 

**Example Use Case:** "Create a Twitter post with a picture of a cat and the hashtag #cutecats." Project Atlas will attempt to launch Twitter (if not already open), compose the post, find an image of a cat (possibly using AI image generation), and publish the tweet.



### 26. Recorder

**Icon:** 

**Description:**  Records audio and screenshots to process downstream using language models. Outputs a transcript of the recording using OpenAI Whisper. 

**Input Parameters:**

-  **Audio File:**  the file name to save the .wav (no extension necessary)


-  **Time:**  The time in seconds to record the audio.

-  **Screenshot File(optional):**  The file name to save a screenshot.


**Example Use Case:** Build a fact-checker that loops constantly and allows verifying what people in a zoom or live meeting are saying. 


## Windows Instructions
Check docs.cheatlayer.com for more details. 

Install Python 3.10
You need to install python 3.10 to enable agents to install any arbitrary python library when solving general problems. 

You can get Python 3.10 from the Windows Store.

Python 3.1 for Cheat Layer Desktop
Windows Store Python 3.1 
### Step 1: Download the latest Desktop Version
Download the Software: Visit the official Cheat Layer website and download the latest version of Cheat Layer Desktop.

To get the latest version of Cheat Layer Desktop. Navigate to the cheat layer web page, click on the option for interactive onboarding, and then proceed to download Cheat Layer Desktop. 



### Step 2: Download and Decompress

Run the Installer: Locate the downloaded file and decompress the file.

Extracting the compressed files from .zip file
Extracting Cheat Layer Desktop
 Follow the on-screen instructions to finish the decompression process. 

### Step 3: Launch Cheat Layer Desktop 
Initiating Cheat Layer Desktop for the first time involves navigating through Windows security prompts. Upon launching the application, Windows may display security warnings. Users should select "More info".



Then select the option "Run anyway"



Then, follow this quick start guide to dive deeper into Cheat Layer Desktop:

Update:
Epic breakthrough! We just cracked unlimited agents and executions!


### Contributions:

Currently we still need to open source the backend and Chrome Extension to be able to run everything locally, but if you are interested in contributing please email me at rohan@cheatlayer.com and I can get you set up with free access while we work on publishing everything. 

We need help with evals for generalized stretch goals to push the limits of the state machine and Loom video to agents, and to improve the testing loop. We strongly believe the testing loop to be the path to the 'holy grail' for open-ended generalized tasks. 

Road Map:
1) Open agent cloud
2) Loom video to agent in Open Agent Cloud
3) Evals for generalized agents
4) Improve testing loop to reach generalized agents with this same scaffolding on the shoulders of the next generations of models.

Thansk!
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=rohanarun/Open-Agent-Studio&type=Date)](https://star-history.com/#rohanarun/Open-Agent-Studio&Date)
