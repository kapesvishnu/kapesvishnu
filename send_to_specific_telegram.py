#!/usr/bin/env python3
import requests
from config.config import TELEGRAM_BOT_TOKEN

def send_to_telegram_phone(phone_number, message, vehicle_id):
    """Send message to specific Telegram user by phone number"""
    
    # Phone to Telegram chat ID mapping
    phone_to_chat = {
        "+1 555-123-4567": "7542768640",  # Your main chat
        "+91 9876543210": "7542768640",   # Same for demo
        "+1 555-234-5678": "7542768640",  # Add more chat IDs here
        "+91 8765432109": "7542768640"
    }
    
    chat_id = phone_to_chat.get(phone_number, "7542768640")  # Default to main chat
    
    telegram_message = f"""📱 SMS TO {vehicle_id}
Phone: {phone_number}
Message: {message}

Sent from Dashboard"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': telegram_message
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"✓ SMS notification sent to Telegram for {phone_number}")
            return True
        else:
            print(f"✗ Failed to send: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    # Test sending to specific phone
    send_to_telegram_phone("+1 555-123-4567", "Test SMS message", "VEHICLE001")