#!/usr/bin/env python3
from send_bot_alert import send_telegram_bot_alert

def send_custom_message():
    vehicle_id = input("Enter Vehicle ID: ").strip()
    contact = input("Enter Contact Number: ").strip()
    message = input("Enter Message: ").strip()
    
    if not all([vehicle_id, contact, message]):
        print("All fields are required!")
        return
    
    telegram_message = f"""📱 MESSAGE TO {vehicle_id}
Contact: {contact}
Message: {message}

Sent from Diesel Tank Monitoring Dashboard
Time: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    print("\nSending to Telegram...")
    result = send_telegram_bot_alert(telegram_message)
    
    if result:
        print("✓ Message sent successfully!")
    else:
        print("✗ Failed to send message")

if __name__ == '__main__':
    send_custom_message()