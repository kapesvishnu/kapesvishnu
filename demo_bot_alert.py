#!/usr/bin/env python3

def demo_telegram_alert():
    print("=" * 60)
    print("TELEGRAM BOT ALERT DEMO")
    print("=" * 60)
    
    alert_message = """🚨 FUEL THEFT ALERT 🚨
    
Vehicle: TRUCK001
Time: 2025-07-26 18:20:15
Previous Level: 85.7%
Current Level: 15.2%
Drop: 70.5%

⚠️ CRITICAL - Immediate attention required!

Bot Token: 8490975345:AAHbPK7KCzQZMbsLwRpiSb8K5Oggsn1ziJg
Chat ID: @Fuel_Monitoring_Tank_bot

Status: Ready to send (requires valid chat setup)"""
    
    print(alert_message)
    print("=" * 60)
    print("To activate:")
    print("1. Start chat with bot using token")
    print("2. Get numeric chat ID")
    print("3. Update config.py with correct chat ID")
    print("=" * 60)

if __name__ == '__main__':
    demo_telegram_alert()