#!/usr/bin/env python3
import datetime

def send_fuel_alert(vehicle_id, current_level, previous_level):
    drop_percentage = previous_level - current_level
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    alert_message = f"""
🚨 FUEL THEFT ALERT 🚨
Time: {timestamp}
Vehicle: {vehicle_id}
Previous Level: {previous_level}%
Current Level: {current_level}%
Drop: {drop_percentage}%
Status: CRITICAL - Immediate attention required!
    """
    
    print("=" * 50)
    print("NOTIFICATION SENT")
    print("=" * 50)
    print(alert_message)
    print("=" * 50)
    
    # Log to file
    with open('alerts.log', 'a') as f:
        f.write(f"{timestamp} - ALERT: {vehicle_id} fuel drop {drop_percentage}%\n")

if __name__ == '__main__':
    # Simulate fuel theft detection
    send_fuel_alert("TRUCK001", 15.2, 85.7)
    send_fuel_alert("VAN002", 8.5, 92.3)