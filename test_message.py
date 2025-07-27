#!/usr/bin/env python3
from send_bot_alert import send_telegram_bot_alert

def test_message():
    # Test message to vehicle
    message = """📱 MESSAGE TO VEHICLE001
Contact: +91 9876543210
Message: Please check fuel level and report status immediately.

Sent from Diesel Tank Monitoring Dashboard"""
    
    print("Sending message to Telegram...")
    result = send_telegram_bot_alert(message)
    
    if result:
        print("✓ Message sent successfully!")
    else:
        print("✗ Failed to send message")

if __name__ == '__main__':
    test_message()