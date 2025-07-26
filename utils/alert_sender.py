import requests
import json
import os
from dotenv import load_dotenv

class AlertSender:
    """
    ALERT SENDER: Sends alerts to different platforms
    Currently supports Discord (easiest and free!)
    """
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        # Get Discord webhook URL from environment
        self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
        
        # Debug print to check if webhook is loaded
        if self.discord_webhook:
            print(f"✅ Discord webhook loaded: {self.discord_webhook[:50]}...")
        else:
            print("❌ Discord webhook not found in environment variables")
    
    def send_discord_alert(self, message: str) -> bool:
        """
        Send alert to Discord channel via webhook
        
        How to get Discord Webhook URL:
        1. Go to your Discord server
        2. Right-click on a channel → Edit Channel
        3. Go to Integrations → Webhooks
        4. Create New Webhook
        5. Copy the Webhook URL
        """
        if not self.discord_webhook or self.discord_webhook.strip() == "":
            print("❌ Discord webhook URL is empty or not configured")
            return False
        
        if not self.discord_webhook.startswith("https://discord.com/api/webhooks/"):
            print("❌ Discord webhook URL format is incorrect")
            return False
        
        try:
            payload = {
                "content": message,
                "username": "CrisisPilot • Critical Alert System",
                "avatar_url": "https://cdn-icons-png.flaticon.com/512/564/564619.png"
            }
            
            response = requests.post(self.discord_webhook, json=payload, timeout=10)
            
            if response.status_code == 204:
                print("✅ Discord alert sent successfully!")
                return True
            else:
                print(f"❌ Discord webhook failed: Status {response.status_code}")
                print(f"Response: {response.text}")
                return False
            
        except Exception as e:
            print(f"❌ Error sending Discord alert: {e}")
            return False
    
    def send_alert(self, message: str, platform: str = "discord") -> bool:
        """
        Main method to send alerts
        """
        if platform.lower() == "discord":
            return self.send_discord_alert(message)
        else:
            print(f"Platform {platform} not supported yet")
            return False

    def test_connection(self) -> bool:
        """Test if the alert system is working"""
        test_message = "🧪 Automated System Test – Operational integrity confirmed! ✅"
        return self.send_discord_alert(test_message)