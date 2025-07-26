# 🚨 ReDAC - Real-Time Disaster Aid Coordinator

A simplified AI-powered disaster monitoring system that fetches news, analyzes threats, and sends alerts to keep you safe!

## 🎯 What Does ReDAC Do?

ReDAC is like having a smart assistant that:
1. **Watches the news** for disasters in your area
2. **Analyzes threats** using AI to determine if you're at risk  
3. **Sends instant alerts** to Discord, Slack, or other platforms
4. **Chats with you** to answer questions about safety and disasters

## 🏗️ Project Structure

```
redac_project/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── agents/               # AI Agents
│   ├── news_agent.py     # Fetches disaster news
│   ├── alert_agent.py    # Analyzes and sends alerts
│   └── chat_agent.py     # Chatbot functionality
└── utils/                # Utilities
    ├── templates.py      # LangChain prompt templates
    ├── parsers.py        # Output parsers
    └── alert_sender.py   # Alert delivery system
```

## 🔧 LangChain Components Explained (Beginner-Friendly)

### What is LangChain?
LangChain is like a toolkit for building AI applications. Think of it as LEGO blocks for AI!

### Key Components Used:

1. **📝 Templates (Prompt Templates)**
   - **What**: Pre-written instructions for the AI (like fill-in-the-blank forms)
   - **Example**: "Analyze this news: {news_data} for location: {location}"
   - **Why**: Ensures consistent, structured AI responses

2. **🔧 Parsers (Output Parsers)**  
   - **What**: Tools that organize the AI's messy text into structured data
   - **Example**: Converts "DISASTER_FOUND: Yes" into `{"disaster_found": true}`
   - **Why**: Makes AI responses usable by our code

3. **⛓️ Chains**
   - **What**: Connect multiple steps together (like a recipe)
   - **Example**: Template → AI → Parser (one after another)
   - **Why**: Automates complex multi-step processes

4. **🏃 Runnables**
   - **What**: The modern LangChain way to execute components
   - **Example**: `chain.invoke({"input": "data"})` 
   - **Why**: More efficient and easier to use than old methods

5. **🤖 Agents**
   - **What**: Smart assistants that can use tools and make decisions
   - **Example**: NewsAgent decides what to search for, AlertAgent decides when to send alerts
   - **Why**: Creates autonomous, intelligent behavior

## 🚀 Quick Setup Guide

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Free API Keys

#### Groq API (Required - AI Processing)
1. Visit [console.groq.com](https://console.groq.com)
2. Create free account
3. Generate API key
4. Copy the key

#### Serper API (Optional - News Search)  
1. Visit [serper.dev](https://serper.dev)
2. Sign up for free account (100 searches/month free)
3. Get API key from dashboard
4. Copy the key

#### Discord Webhook (Recommended - Alerts)
1. Create a Discord server (or use existing)
2. Right-click on a channel → Edit Channel
3. Go to Integrations → Webhooks → Create New Webhook
4. Copy the Webhook URL

### Step 3: Configure Environment
1. Copy `.env.example` to `.env`
2. Fill in your API keys:
```bash
GROQ_API_KEY=your_actual_groq_key_here
SERPER_API_KEY=your_actual_serper_key_here  
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

## 🎮 How to Use ReDAC

1. **Enter Your Location**: Type your city/region in the sidebar
2. **Test Alerts**: Click "Test Alert System" to verify Discord integration
3. **Monitor Disasters**: Click "Check for Disasters" to scan for threats
4. **Chat for Help**: Use the chat box to ask questions about safety

## 🆓 Free Alert Platforms

### Discord (Recommended - Easiest!)
- **Cost**: Completely free
- **Setup**: 2 minutes with webhook URL
- **Features**: Rich formatting, instant delivery

### Slack (Alternative)
- **Cost**: Free tier available  
- **Setup**: Similar to Discord webhooks
- **Features**: Professional interface

### Telegram (Advanced)
- **Cost**: Free
- **Setup**: Create bot via BotFather
- **Features**: Mobile-first, global reach

## 🔍 Understanding the AI Workflow

Here's how ReDAC processes information:

```
User Location Input
        ↓
NewsAgent searches for disasters
        ↓  
Raw news articles found
        ↓
AlertAgent analyzes with AI using Templates
        ↓
AI response parsed into structured data
        ↓
If disaster found → Generate alert message
        ↓
AlertSender delivers to Discord/Slack
        ↓
ChatAgent provides conversational help
```

## 🧪 Testing the System

### Test Alert System
```python
# The system includes a test button that sends:
"🧪 ReDAC Alert System Test - System is working!"
```

### Mock Data Mode
If no Serper API key is provided, ReDAC uses realistic mock data for testing.

### Sample Disaster Alert
```
🚨 DISASTER ALERT 🚨

Type: Earthquake
Location: California  
Severity: Medium

Description: 5.2 earthquake detected near Los Angeles area

Stay safe and follow local authorities' guidance!
```

## 🎯 Key Features

- ✅ **Real-time news monitoring** with AI analysis
- ✅ **Multi-platform alerts** (Discord, Slack, etc.)
- ✅ **Conversational AI** for safety questions
- ✅ **Free and open-source** - no paid services required
- ✅ **Beginner-friendly** - well-documented and explained
- ✅ **Modular design** - easy to extend and customize

## 🚀 Potential Improvements

- Add more alert platforms (WhatsApp, SMS)
- Include weather data integration
- Add evacuation route mapping
- Support multiple languages
- Create mobile app version

## 🆘 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### API key errors  
- Check your `.env` file exists and has correct keys
- Verify API keys are valid and active

### Discord alerts not working
- Test webhook URL in browser - should show Discord info
- Check webhook permissions in Discord server

### No news found
- Try different location names (e.g., "New York" vs "NYC")
- Check if Serper API key is working

## 📚 Learning Resources

- [LangChain Documentation](https://docs.langchain.com)
- [Groq API Docs](https://console.groq.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Discord Webhook Guide](https://support.discord.com/hc/en-us/articles/228383668)

---

**Built with ❤️ using free and open-source tools for global disaster response.**# ReDAC-Real-Time-Disaster-Aid-Coordinator
