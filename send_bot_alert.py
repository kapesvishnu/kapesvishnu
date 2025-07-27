#!/usr/bin/env python3
import requests
from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_bot_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✓ Alert sent to Telegram bot successfully")
            return True
        else:
            print(f"✗ Failed to send alert: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error sending alert: {e}")
        return False

if __name__ == '__main__':
    alert_message = """🚨 <b>FUEL THEFT ALERT</b> 🚨
    
<b>Vehicle:</b> TRUCK001
<b>Time:</b> 2025-07-26 18:20:15
<b>Previous Level:</b> 85.7%
<b>Current Level:</b> 15.2%
<b>Drop:</b> 70.5%

⚠️ <b>CRITICAL - Immediate attention required!</b>"""
    
    send_telegram_bot_alert(alert_message)