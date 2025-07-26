import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

print("=== Advanced Discord Webhook Test ===")
print(f"Testing webhook: {webhook_url[:50]}..." if webhook_url else "No webhook URL found")
print()

if not webhook_url:
    print("❌ No DISCORD_WEBHOOK_URL found in .env file")
    exit()

# Test 1: Basic URL validation
print("🔍 Test 1: URL Validation")
if webhook_url.startswith("https://discord.com/api/webhooks/"):
    print("✅ URL format looks correct")
else:
    print("❌ URL format incorrect - should start with https://discord.com/api/webhooks/")
    print(f"Your URL starts with: {webhook_url[:40]}...")

print()

# Test 2: Network connectivity to Discord
print("🔍 Test 2: Discord Connectivity")
try:
    response = requests.get("https://discord.com", timeout=5)
    if response.status_code == 200:
        print("✅ Can reach Discord.com")
    else:
        print(f"⚠️ Discord.com returned status: {response.status_code}")
except Exception as e:
    print(f"❌ Cannot reach Discord.com: {e}")
    print("This might be a network/firewall issue")

print()

# Test 3: Webhook GET request (to check if webhook exists)
print("🔍 Test 3: Webhook Existence Check")
try:
    response = requests.get(webhook_url, timeout=10)
    if response.status_code == 200:
        webhook_info = response.json()
        print("✅ Webhook exists and is accessible")
        print(f"   Webhook name: {webhook_info.get('name', 'Unknown')}")
        print(f"   Channel ID: {webhook_info.get('channel_id', 'Unknown')}")
    elif response.status_code == 404:
        print("❌ Webhook not found (404) - it may have been deleted")
    elif response.status_code == 401:
        print("❌ Webhook unauthorized (401) - URL might be invalid")
    else:
        print(f"⚠️ Unexpected status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
except requests.exceptions.ConnectionError:
    print("❌ Connection error - this is the same error you're seeing")
    print("Possible causes:")
    print("   • Firewall blocking Discord webhooks")
    print("   • ISP blocking Discord")
    print("   • Network connectivity issues")
    print("   • Discord server issues")
except requests.exceptions.Timeout:
    print("❌ Request timed out - slow connection or Discord issues")
except Exception as e:
    print(f"❌ Error checking webhook: {e}")

print()

# Test 4: Try sending a test message with retry logic
print("🔍 Test 4: Send Test Message (with retries)")

test_payload = {
    "content": "🧪 Advanced webhook test - connection successful!",
    "username": "ReDAC Test Bot"
}

for attempt in range(3):
    try:
        print(f"   Attempt {attempt + 1}/3...")
        response = requests.post(
            webhook_url, 
            json=test_payload, 
            timeout=15,
            headers={'User-Agent': 'ReDAC-Bot/1.0'}
        )
        
        if response.status_code == 204:
            print("✅ SUCCESS: Test message sent!")
            print("Check your Discord channel for the test message")
            break
        elif response.status_code == 429:
            print("⚠️ Rate limited - waiting 5 seconds...")
            time.sleep(5)
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error on attempt {attempt + 1}: {e}")
        if attempt < 2:
            print("   Retrying in 3 seconds...")
            time.sleep(3)
    except Exception as e:
        print(f"❌ Error on attempt {attempt + 1}: {e}")
        break
else:
    print("❌ All attempts failed")

print()
print("=== Troubleshooting Suggestions ===")
print("If you're getting connection errors:")
print("1. 📱 Try using mobile hotspot to test")
print("2. 🔄 Create a new Discord webhook")
print("3. 🔒 Check if your firewall blocks Discord")
print("4. 🌐 Try a VPN if available")
print("5. ⏰ Wait a few minutes and try again")
print()
print("=== End Test ===")