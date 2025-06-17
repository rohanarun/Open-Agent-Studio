# Open Agent Studio

<div align="center">

![Open Agent Studio Logo](https://storage.googleapis.com/cheatlayer/agent.png)

**The first cross-platform desktop application for Agentic Process Automation**  
*An open-source alternative to UIPath and traditional RPA tools*

[![Downloads](https://img.shields.io/badge/Downloads-Available-green)](#-installation)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue)](#-installation)
[![License](https://img.shields.io/badge/License-Open%20Source-orange)](#-contributing)
[![Star History](https://api.star-history.com/svg?repos=rohanarun/Open-Agent-Studio&type=Date)](https://star-history.com/#rohanarun/Open-Agent-Studio&Date)

[🚀 **Get Started**](#-installation) • [📖 **Documentation**](#-key-concepts) • [🤝 **Contributing**](#-contributing) • [💬 **Support**](#-support)

</div>

---

## 🌟 What is Open Agent Studio?

Open Agent Studio is an open-source alternative to UIPath and traditional RPA tools by enabling **Agentic Process Automation** through natural language. Instead of brittle selectors and complex code, describe what you want in plain English and let AI handle the rest.

### ✨ Key Features

- 🎯 **Semantic Targets**: Future-proof automation that survives UI changes
- 🎬 **Video-to-Agent**: World's first video-based agent creation
- 🌐 **Cross-Platform**: Works on Windows and Linux
- 🔗 **Built-in API**: Every instance includes a REST API
- 🧠 **AI-Powered**: GPT-4 integration for intelligent decision making
- 🔄 **Self-Healing**: Robust verification and testing loops

---

## 📥 Installation

### Windows
1. **Download**: [Windows Executable](https://toy.new/cheatlayer.zip)
2. **Extract** the ZIP file
3. **Install Python 3.10** from [Windows Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5)
4. **Run** the application (click "More info" → "Run anyway" if Windows shows security warnings)

### Linux
1. **Download**: [Linux Executable](https://toy.new/main.zip)
2. **Extract** and run

### 📺 Video Tutorials
- [Windows Installation Guide](https://www.youtube.com/watch?v=8xhFKkD4H-0)
- [Video-to-Agent Demo](https://www.youtube.com/watch?v=gsU5033ms5k)

---

## 🚀 Quick Start

### 1. Create Your First Agent
```json
{
  "key": "your_api_key",
  "json_output": [
    {
      "type": "open tab",
      "target": "https://example.com"
    },
    {
      "type": "click",
      "target": "Login button",
      "browser_mode": true
    }
  ],
  "goal": "Navigate to website and click login"
}
```

### 2. Test Locally
```bash
curl -X POST http://localhost:8080/agents \
  -H "Content-Type: application/json" \
  -d @your_agent.json
```

---

## 🧠 Key Concepts

| Concept | Description |
|---------|-------------|
| **Nodes** | Individual actions an agent can perform |
| **Variables** | Data passed between nodes |
| **Verification** | Automatic checking of action success |
| **Semantic Targets** | Natural language element descriptions |
| **Agent API** | Built-in REST API for automation |

### 🎯 Semantic Targets
Instead of fragile CSS selectors, use natural language:
```json
{
  "type": "click",
  "target": "blue submit button",
  "browser_mode": true
}
```

This works even if the website completely changes its design!

---

## 🛠 Agent Node Types

<details>
<summary><strong>🌐 Browser Automation</strong></summary>

### Click
```json
{
  "type": "click",
  "target": "Submit button",
  "browser_mode": true
}
```

### Type Text
```json
{
  "type": "keypress",
  "prompt": "Hello, World!"
}
```

### Open Tab
```json
{
  "type": "open tab",
  "target": "https://example.com"
}
```

### Wait/Delay
```json
{
  "type": "delay",
  "time": 5
}
```

</details>

<details>
<summary><strong>🧠 AI & Data Processing</strong></summary>

### GPT-4 Processing
```json
{
  "type": "gpt4",
  "prompt": "Summarize the following text:",
  "input": ["article_text"],
  "data": "summary"
}
```

### Python Execution
```json
{
  "type": "python",
  "code": "import pandas as pd\nprint('Hello from Python!')"
}
```

### Semantic Scraping
```json
{
  "type": "semanticScrape",
  "target": "product prices",
  "data": "price_data"
}
```

</details>

<details>
<summary><strong>📊 Integrations</strong></summary>

### Google Sheets
```json
{
  "type": "google_sheets_add_row",
  "URL": "sheet_url",
  "Sheet_Name": "Sheet1",
  "data": ["John", "Doe", "30"]
}
```

### Email
```json
{
  "type": "email",
  "to": "user@example.com",
  "subject": "Automation Report",
  "body": "Task completed successfully!"
}
```

### API Calls
```json
{
  "type": "api",
  "URL": "https://api.example.com/data",
  "headers": {"Content-Type": "application/json"},
  "body": {"key": "value"}
}
```

</details>

---

## 📖 Complete Example

Here's a complete agent that scrapes data, analyzes it, and sends results:

```json
{
  "key": "your_api_key",
  "json_output": [
    {
      "type": "open tab",
      "target": "https://news.ycombinator.com"
    },
    {
      "type": "semanticScrape",
      "target": "top story headlines",
      "data": "headlines"
    },
    {
      "type": "gpt4",
      "prompt": "Summarize these headlines and identify key trends:",
      "input": ["headlines"],
      "data": "analysis"
    },
    {
      "type": "google_sheets_create",
      "URL": "sheet_url",
      "Sheet_Name": "news_analysis"
    },
    {
      "type": "google_sheets_add_row",
      "URL": "sheet_url",
      "Sheet_Name": "news_analysis",
      "data": ["{{analysis}}"]
    },
    {
      "type": "email",
      "to": "manager@company.com",
      "subject": "Daily News Analysis",
      "body": "Please find today's analysis attached.",
      "data": "analysis"
    }
  ],
  "goal": "Scrape news, analyze trends, save to sheets, and email results"
}
```

---

## 📡 Agent API Reference

### POST /agents
Creates and runs a new agent.

**Request:**
```json
{
  "key": "your_api_key",
  "json_output": [...],
  "goal": "description"
}
```

**Response:**
Returns execution results and verification data.

---

## 🎯 Best Practices

1. **Use descriptive semantic targets** instead of technical selectors
2. **Add appropriate delays** for page loading
3. **Handle errors gracefully** with verification
4. **Use meaningful variable names**
5. **Test with simple workflows first**
6. **Leverage GPT-4 for complex logic**
7. **Always verify critical actions**

---

## 🗺 Roadmap

- [ ] **Open Agent Cloud** - Cloud-based execution
- [ ] **Enhanced Video-to-Agent** - Improved conversion accuracy
- [ ] **Advanced Evaluations** - Better testing for generalized agents
- [ ] **Improved Testing Loop** - Self-healing automation
- [ ] **Full Open Source Backend** - Complete local deployment

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🚀 Get Started
1. Email [rohan@cheatlayer.com](mailto:rohan@cheatlayer.com) for contributor access
2. Join our community discussions
3. Check out open issues and feature requests

### 🎯 Areas We Need Help
- **Evaluations** for generalized agents
- **Testing loop improvements**
- **Video-to-agent enhancement**
- **Documentation and tutorials**
- **Bug reports and fixes**

### 📋 Development Setup
```bash
# Clone the repository
git clone https://github.com/rohanarun/Open-Agent-Studio.git

# Contact us for backend setup instructions
# Email: rohan@cheatlayer.com
```

---

## 💬 Support

- **📧 Email**: [rohan@cheatlayer.com](mailto:rohan@cheatlayer.com)
- **📚 Documentation**: [docs.cheatlayer.com](https://docs.cheatlayer.com)
- **🐛 Issues**: [GitHub Issues](https://github.com/rohanarun/Open-Agent-Studio/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/rohanarun/Open-Agent-Studio/discussions)

---

## 🏆 Our Story

Founded during the pandemic to help people rebuild their businesses with AI, we were the first startup approved by OpenAI to sell GPT-3 for automation in August 2021. We invented "Semantic Targets" and achieved 97% accuracy with our Atlas-2 multimodal model.

**Our Vision**: In a future where AI can generate custom, secure, and free versions of expensive business software, we're building tools that level the playing field for everyone.

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=rohanarun/Open-Agent-Studio&type=Date)](https://star-history.com/#rohanarun/Open-Agent-Studio&Date)

---

<div align="center">

**Made with ❤️ by the Cheat Layer Team**

[Get Started Now](#-installation) • [Star on GitHub](https://github.com/rohanarun/Open-Agent-Studio) • [Join the Community](mailto:rohan@cheatlayer.com)

</div>
