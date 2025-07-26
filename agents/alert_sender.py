import requests
import json
import os
import time
from dotenv import load_dotenv

class AlertSender:
    """
    ALERT SENDER: Sends alerts to Discord with improved reliability
    Now includes better error handling, retry logic, and connection testing
    """
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        # Get Discord webhook URL from environment
        self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
        
        # Validate webhook URL on initialization
        if self.discord_webhook:
            if self._validate_webhook_url(self.discord_webhook):
                print(f"✅ Discord webhook loaded and validated")
            else:
                print(f"⚠️ Discord webhook URL format may be invalid")
        else:
            print("❌ Discord webhook not found in environment variables")
    
    def _validate_webhook_url(self, url: str) -> bool:
        """Validate Discord webhook URL format"""
        return (
            url and 
            url.strip() != "" and 
            url.startswith("https://discord.com/api/webhooks/") and
            len(url.split('/')) >= 7  # Basic URL structure check
        )
    
    def send_discord_alert(self, message: str) -> bool:
        """
        Send alert to Discord channel via webhook with retry logic
        
        Args:
            message: Alert message to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self._validate_webhook_url(self.discord_webhook):
            print("❌ Discord webhook URL is invalid or not configured")
            return False
        
        payload = {
            "content": message,
            "username": "CrisisPilot • Critical Alert System",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/564/564619.png"
        }
        
        # Retry logic with exponential backoff
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.discord_webhook, 
                    json=payload, 
                    timeout=15,
                    headers={
                        'User-Agent': 'CrisisPilot-CriticalAlert-Bot/1.0',
                        'Content-Type': 'application/json'
                    }
                )
                
                if response.status_code == 204:
                    print(f"✅ Discord alert sent successfully on attempt {attempt + 1}")
                    return True
                elif response.status_code == 429:
                    # Rate limited - wait longer
                    retry_after = int(response.headers.get('Retry-After', 10))
                    print(f"⚠️ Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                elif response.status