#!/usr/bin/env python3
from send_bot_alert import send_telegram_bot_alert
import webbrowser

def quick_sms():
    phone = "+1 475-231-1111"
    
    print(f"📱 Quick SMS to {phone}")
    message = input("Enter message: ")
    
    if message:
        # Open SMS app
        sms_url = f"sms:{phone}?body={message}"
        webbrowser.open(sms_url)
        
        # Log to Telegram
        log_msg = f"""📱 SMS SENT TO {phone}

Message: {message}

Status: Opened SMS app
Action: Manual send required"""
        
        send_telegram_bot_alert(log_msg)
        print(f"✅ SMS app opened for {phone}")
        print(f"📝 Message: {message}")
    else:
        print("❌ No message entered")

if __name__ == '__main__':
    quick_sms()