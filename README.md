# Open Agent Studio 

Open Agent Studio is the first cross platform desktop application built to enable Agentic Process Automation as an open-source alternative and replacement for UIpath and all other RPA tools today. 

Download for Windows and Mac at https://openagent.studio.

We founded Cheat Layer during the pandemic to help people who had lost their jobs and businesses rebuild online using GPT-3. We personally helped hundreds pro bono before turning to AI for help.

In August 2021, we were the first startup to get approved by openAI to sell GPT-3 for automation. We were the first to publish our framework for agents, Project Atlas, in July 2022.

Businesses today are threatening to fire employees and replace them with AI. We believe within 2 years, the AI necessary to generate most of those businesses will be a commodity.

In a future where the AI in your pocket can generate custom, secure, and free versions of all the most expensive business software, we believe there'll be a level playing field that removes the barrier to build these businesses. More small businesses will build competitive brands through personal relationships, better quality service, and network effects through unique data. We invite you to join us in building this future together faster.

This is an older public version of our internal private repo which will be updated in the coming days with the latest updates to Open Agent Studio 7.0.0 whch can be downloaded at openagent.studio now. 

## Introducing The World's First Video To Agents!
[![Introducing The World's First Video To Agents!](https://img.youtube.com/vi/gsU5033ms5k/0.jpg)](https://www.youtube.com/watch?v=gsU5033ms5k)


## Agentic Process Automation
![Generalized Agents framework](https://storage.googleapis.com/cheatlayer/agent.png)
![image](https://github.com/user-attachments/assets/ff792176-c3cc-41df-bbaf-8728e7520540)


### Semantic Targets
Semantic targets distils the underlying intent of a target to english, so they still work even if services completely change their designs. This enables building robust, future-proof, agents. 

Semantic targets can be dynamic or robust based on how strict the language is. 

### Semantic Triggers
![Semantic Triggers](https://storage.googleapis.com/cheatlayer/semtriggers.png)

### Reasoning Based Targets
![Reasoning Based Targets](https://storage.googleapis.com/cheatlayer/reasoning.png)  

---
title: 'Agents API'
description: 'Trigger agents from other services using a simple JSON API that returns results'
---
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
