#!/usr/bin/env python3
import time
from send_bot_alert import send_telegram_bot_alert
from src.vehicle_manager import VehicleManager

def send_live_updates():
    vm = VehicleManager('data/vehicles_mixed.json')
    
    # Send current status
    message = "📊 LIVE VEHICLE STATUS\n\n"
    
    for vehicle_id, data in vm.vehicles.items():
        if data['readings']:
            fuel = data['readings'][-1]['fuel_level']
            liters = fuel * 2.0
            status = "🟢" if fuel > 70 else "🟡" if fuel > 30 else "🔴"
            
            message += f"{status} {vehicle_id}\n"
            message += f"   Fuel: {fuel:.1f}% ({liters:.1f}L)\n"
            message += f"   📍 {data.get('destination', 'Unknown')}\n"
            message += f"   📞 {data.get('contact', 'No contact')}\n\n"
    
    message += "Commands:\n"
    message += "/vehicles - Refresh status\n"
    message += "/fuel [ID] - Check specific vehicle\n"
    message += "/update [ID] [LEVEL] - Update reading"
    
    send_telegram_bot_alert(message)
    print("✅ Live status sent to Telegram")

def send_emergency_alert():
    alert = """🚨 EMERGENCY FUEL THEFT ALERT 🚨

🚛 Vehicle: VEHICLE001
📍 Location: Mumbai-Pune Highway (KM 45)
⛽ Fuel Drop: 78.2% → 15.3% (62.9% loss)
⏰ Time: Just now
📞 Driver: +91 9876543210

🔴 IMMEDIATE ACTION REQUIRED:
1. Contact driver immediately
2. Check vehicle location
3. Report to authorities if needed

Use /fuel VEHICLE001 for updates"""
    
    send_telegram_bot_alert(alert)
    print("🚨 Emergency alert sent!")

if __name__ == '__main__':
    print("Sending live updates to Telegram...")
    send_live_updates()
    
    time.sleep(2)
    
    print("Sending emergency alert...")
    send_emergency_alert()