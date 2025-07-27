#!/usr/bin/env python3
# Install: pip install twilio
from twilio.rest import Client

# Twilio credentials (get from twilio.com)
TWILIO_SID = 'your_account_sid'
TWILIO_TOKEN = 'your_auth_token'
TWILIO_PHONE = '+1234567890'  # Your Twilio phone number

def send_real_sms(to_phone, message):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        
        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=to_phone
        )
        
        print(f"✅ SMS sent to {to_phone}")
        print(f"Message ID: {sms.sid}")
        return True
    except Exception as e:
        print(f"❌ SMS failed: {e}")
        return False

if __name__ == '__main__':
    # Test SMS
    phone = "+1 475-231-1111"
    message = "🚛 FUEL ALERT: Check vehicle fuel level immediately. From: Diesel Monitoring System"
    send_real_sms(phone, message)