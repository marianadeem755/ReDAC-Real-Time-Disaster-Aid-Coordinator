"""
Utils package for CrisisPilot: Global Disaster Swift Response Assistant

This package contains utility modules for:
- templates.py: LangChain prompt templates
- parsers.py: Output parsers for structuring AI responses  
- alert_sender.py: Alert delivery system for multiple platforms
"""

# Import key components to make them easily accessible
from .templates import NEWS_ANALYSIS_TEMPLATE, ALERT_TEMPLATE, CHAT_TEMPLATE
from .parsers import disaster_parser, chat_parser, parse_disaster_text
from .alert_sender import AlertSender

# Make key components available when importing the package
__all__ = [
    "NEWS_ANALYSIS_TEMPLATE",
    "ALERT_TEMPLATE", 
    "CHAT_TEMPLATE",
    "disaster_parser",
    "chat_parser",
    "parse_disaster_text",
    "AlertSender"
]