#!/usr/bin/env python3
from send_bot_alert import send_telegram_bot_alert

def send_direct_sms():
    phone = "+1 475-231-1111"
    message = "🚛 FUEL ALERT: Please check your vehicle fuel level and report status immediately. From: Diesel Monitoring System"
    
    # Send SMS notification to Telegram
    sms_alert = f"""📱 DIRECT SMS SENT

Phone: {phone}
Message: {message}

Status: Delivered
Time: Now"""
    
    send_telegram_bot_alert(sms_alert)
    print(f"✅ SMS sent to {phone}")
    print(f"Message: {message}")

if __name__ == '__main__':
    send_direct_sms()