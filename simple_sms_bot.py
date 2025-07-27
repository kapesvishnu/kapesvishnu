#!/usr/bin/env python3
from send_bot_alert import send_telegram_bot_alert

def send_sms_to_phone():
    """Send SMS notification for +1 475-231-1111"""
    
    phone = "+1 475-231-1111"
    message = "🚛 FUEL CHECK: Please report your current fuel level immediately. Reply with fuel percentage. From: Diesel Monitoring"
    
    # Create SMS notification
    sms_alert = f"""📱 SMS COMMAND EXECUTED

TO: {phone}
MESSAGE: {message}

INSTRUCTIONS:
1. Copy phone number: {phone}
2. Copy message: {message}
3. Send SMS manually from your phone

STATUS: Ready to send"""
    
    # Send to Telegram
    send_telegram_bot_alert(sms_alert)
    print(f"✅ SMS details sent to Telegram")
    print(f"📱 Phone: {phone}")
    print(f"💬 Message: {message}")

def send_emergency_sms():
    """Send emergency SMS"""
    
    phone = "+1 475-231-1111"
    message = "🚨 EMERGENCY: Contact control room NOW at +91 9876543210. Urgent response required. From: Diesel Monitoring System"
    
    sms_alert = f"""🚨 EMERGENCY SMS

TO: {phone}
MESSAGE: {message}

⚠️ URGENT - SEND IMMEDIATELY
Copy and send this SMS now!"""
    
    send_telegram_bot_alert(sms_alert)
    print("🚨 Emergency SMS details sent!")

if __name__ == '__main__':
    print("Choose SMS type:")
    print("1. Fuel check SMS")
    print("2. Emergency SMS")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        send_sms_to_phone()
    elif choice == "2":
        send_emergency_sms()
    else:
        print("Invalid choice")