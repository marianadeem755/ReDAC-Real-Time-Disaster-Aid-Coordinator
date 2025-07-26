# 🚨 CrisisPilot: Global Disaster Swift Response Assistant

**Developed by [Your Company Name]**

An AI-powered disaster monitoring and alert system that monitors global news, analyzes potential threats, and sends instant Discord alerts to keep communities informed and safe during emergencies.

## 🎯 What is CrisisPilot?

CrisisPilot is an intelligent disaster response assistant that:
- **Monitors global news** for disasters and emergencies in real-time
- **Analyzes threats** using advanced AI to assess risk levels
- **Sends instant Discord alerts** to notify your community of potential dangers
- **Provides conversational AI** to answer safety questions and emergency guidance

## 🏗️ Project Structure

```
CrisisPilot/
├── app.py                      # Main Streamlit application interface
├── config.py                   # Configuration and settings management
├── requirements.txt            # Python package dependencies
├── .env                        # Environment variables (API keys, settings)
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
├── test_alerts.py              # Alert system testing utilities
├── agents/                     # AI Agent Components
│   ├── __pycache__/           # Python cache files
│   ├── __init__.py            # Package initialization
│   ├── alert_agent.py         # Disaster analysis and alerting logic
│   ├── alert_message_agent.py # Alert message formatting and customization
│   ├── alert_sender.py        # Discord alert delivery system
│   ├── chat_agent.py          # Conversational AI for user interaction
│   └── news_agent.py          # News monitoring and data collection
└── utils/                      # Utility Functions
    ├── __pycache__/           # Python cache files
    ├── __init__.py            # Package initialization
    ├── alert_sender.py        # Alert delivery utilities
    ├── parsers.py             # Data parsing and formatting tools
    └── templates.py           # LangChain prompt templates
```

## 🚀 Quick Setup Guide

### Prerequisites
- Python 3.8 or higher
- Discord server with webhook permissions
- Internet connection for news monitoring

### Step 1: Clone and Install
```bash
git clone [your-repository-url]
cd CrisisPilot
pip install -r requirements.txt
```

### Step 2: Get Required API Keys

#### 1. Groq API (Required - AI Processing)
1. Visit [console.groq.com](https://console.groq.com)
2. Create a free account
3. Generate your API key
4. Copy the key for configuration

#### 2. Serper API (Optional - Enhanced News Search)
1. Visit [serper.dev](https://serper.dev)
2. Sign up for free account (100 searches/month included)
3. Get your API key from the dashboard
4. Copy the key for configuration

#### 3. Discord Webhook (Required - Alert Delivery)
1. Open your Discord server
2. Go to Server Settings → Integrations
3. Click "Create Webhook" or "View Webhooks"
4. Choose the channel for alerts
5. Copy the Webhook URL

### Step 3: Configure Environment Variables
Create a `.env` file in the project root with your API keys:

```bash
# Required - AI Processing
GROQ_API_KEY=your_groq_api_key_here

# Optional - Enhanced news search (uses mock data if not provided)
SERPER_API_KEY=your_serper_api_key_here

# Required - Discord Alert Delivery
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url_here
```

### Step 4: Run CrisisPilot
```bash
streamlit run app.py
```

The application will open in your web browser at `http://localhost:8501`

## 🎮 How to Use CrisisPilot

### 1. Initial Setup
- Enter your location (city, state, country) in the sidebar
- Test your Discord integration using the "Test Alert System" button
- Verify alerts are received in your Discord channel

### 2. Monitor for Disasters
- Click "Check for Disasters" to scan for threats in your area
- The system will analyze news articles and assess risk levels
- Automatic alerts will be sent to Discord if threats are detected

### 3. Interactive Chat
- Use the chat interface to ask questions about:
  - Emergency preparedness
  - Safety procedures
  - Current disaster information
  - Evacuation guidance

### 4. Alert Management
- Customize alert sensitivity in the settings
- Choose notification preferences
- Monitor alert history and responses

## 📱 Discord Integration

### Alert Format
CrisisPilot sends structured alerts to your Discord channel:

```
🚨 CRISIS PILOT ALERT 🚨

📍 Location: [Your Area]
⚠️  Threat Type: [Earthquake/Flood/Storm/etc.]
🔴 Severity Level: [High/Medium/Low]
📅 Detected: [Timestamp]

📰 Summary: [AI-generated threat analysis]

🛡️ Recommendations: [Safety guidance]

Stay safe and follow local authorities' guidance!
```

### Test Alert
The system includes a test function that sends:
```
🧪 CRISIS PILOT TEST ALERT 🧪
Alert system is operational and ready to protect your community!
```

## 🔧 Technical Architecture

### AI Components
- **News Agent**: Monitors global news sources for disaster-related content
- **Alert Agent**: Analyzes news data using AI to determine threat levels
- **Message Agent**: Formats and customizes alert messages
- **Chat Agent**: Provides conversational assistance and safety guidance

### LangChain Integration
- **Prompt Templates**: Structured AI instructions for consistent analysis
- **Output Parsers**: Convert AI responses into actionable data
- **Chains**: Link multiple AI operations for complex processing
- **Runnables**: Modern execution framework for efficient processing

### Data Flow
```
Location Input → News Monitoring → AI Analysis → Threat Assessment → Discord Alert → User Notification
```

## 🛠️ Configuration Options

### Alert Sensitivity Levels
- **High**: Alerts for all potential threats
- **Medium**: Alerts for moderate to severe threats only
- **Low**: Alerts for severe threats only

### Supported Disaster Types
- Natural disasters (earthquakes, floods, hurricanes)
- Weather emergencies (severe storms, blizzards)
- Human-caused emergencies (fires, chemical spills)
- Public safety alerts (evacuations, emergency declarations)

## 🧪 Testing and Validation

### Run Alert Tests
```bash
python test_alerts.py
```

### Validate Configuration
- Check `.env` file has all required variables
- Test Discord webhook URL in browser
- Verify API key permissions and limits

### Mock Data Mode
If Serper API is unavailable, CrisisPilot automatically uses realistic mock data for testing and development.

## 🚨 Emergency Response Features

### Real-time Monitoring
- Continuous news scanning
- AI-powered threat assessment
- Instant notification delivery

### Multi-language Support
- Alerts available in multiple languages
- Localized emergency guidance
- Cultural context awareness

### Community Integration
- Discord server-wide notifications
- Role-based alert targeting
- Community response coordination

## 🔮 Future Enhancements

### Planned Features
- **Multi-platform Alerts**: Slack, Telegram, SMS integration
- **Weather Integration**: Real-time weather data correlation
- **Evacuation Mapping**: Route planning and traffic analysis
- **Mobile Application**: Dedicated mobile app with push notifications
- **API Access**: Developer API for third-party integrations

### Advanced AI Features
- Predictive threat modeling
- Historical disaster pattern analysis
- Personalized risk assessments
- Community vulnerability mapping

## 📊 System Requirements

### Minimum Requirements
- Python 3.8+
- 512MB RAM
- 100MB disk space
- Stable internet connection

### Recommended Configuration
- Python 3.10+
- 1GB RAM
- 500MB disk space
- High-speed internet connection

## 🆘 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Discord alerts not working
- Verify webhook URL is correct and active
- Check Discord server permissions
- Test webhook URL in browser (should show JSON response)

#### API key errors
- Ensure `.env` file exists in project root
- Verify API keys are active and have sufficient credits
- Check for extra spaces or characters in keys

#### No disasters detected
- Try different location formats ("New York, NY" vs "New York City")
- Check if Serper API key is working correctly
- Verify internet connection for news access

### Getting Help

1. Check the troubleshooting section above
2. Review error messages in the console
3. Test individual components using provided test scripts
4. Contact support team for technical assistance

## 📄 License and Legal

### Open Source License
This project is released under [Your License Choice] license. See LICENSE file for details.

### Data Privacy
- No personal data is stored permanently
- API keys are encrypted and secure
- News data is processed temporarily for analysis only

### Disclaimer
CrisisPilot is a supplementary alert system. Always follow official emergency services and local authorities for definitive emergency guidance.

## 🤝 Contributing

We welcome contributions to improve CrisisPilot:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

### Development Setup
```bash
git clone [repository-url]
cd CrisisPilot
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

## 📞 Support and Contact

- **Technical Support**: [your-support-email]
- **Documentation**: [your-docs-url]
- **Bug Reports**: [your-issues-url]
- **Feature Requests**: [your-feature-requests-url]

---

**🏢 Developed by [Your Company Name]**
**🌍 Protecting communities worldwide through intelligent disaster response**

**🔧 Built with Python 🐍 • LangChain 🧠 • Streamlit ⚡ • Discord Webhooks 🔔**