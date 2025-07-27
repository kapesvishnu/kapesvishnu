#!/usr/bin/env python3
from send_bot_alert import send_telegram_bot_alert

def test_bot_commands():
    print("Testing Telegram Bot Commands...")
    
    # Test 1: Vehicle Status
    status_msg = """🚛 VEHICLE STATUS UPDATE

/vehicles - View all vehicles
/fuel VEHICLE001 - Check fuel level
/add TRUCK005 85.5 - Add new vehicle
/update VEHICLE001 45.2 - Update fuel level

Current Fleet:
• VEHICLE001: 78.2% 🟢 ACTIVE → Mumbai
• VEHICLE002: 89.7% 🟢 ACTIVE → Delhi  
• VEHICLE003: 45.3% 🟡 LOW → Chennai
• VEHICLE004: No data ⚪ INACTIVE → Kolkata

Use commands above to interact with the system!"""
    
    send_telegram_bot_alert(status_msg)
    print("✅ Status message sent")
    
    # Test 2: Fuel Alert
    alert_msg = """🚨 CRITICAL FUEL ALERT 🚨

Vehicle: VEHICLE001
Previous Level: 78.2%
Current Level: 25.1%
Drop: 53.1%
Location: Mumbai Highway
Time: 2024-01-16 14:30

⚠️ POSSIBLE FUEL THEFT DETECTED!
Contact driver immediately: +91 9876543210

Commands:
/fuel VEHICLE001 - Check current status
/update VEHICLE001 [level] - Update reading"""
    
    send_telegram_bot_alert(alert_msg)
    print("✅ Alert message sent")
    
    # Test 3: Help Message
    help_msg = """🤖 DIESEL TANK MONITORING BOT

Available Commands:
/start - Show this help
/vehicles - List all vehicles
/fuel [ID] - Check specific fuel level
/add [ID] [LEVEL] - Add new vehicle
/update [ID] [LEVEL] - Update fuel reading
/alert - Send test alert

Examples:
• /fuel VEHICLE001
• /add TRUCK005 85.5
• /update VEHICLE002 67.3

Dashboard: http://localhost:8080
Support: Contact system admin"""
    
    send_telegram_bot_alert(help_msg)
    print("✅ Help message sent")

if __name__ == '__main__':
    test_bot_commands()