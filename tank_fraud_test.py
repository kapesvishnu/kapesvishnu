#!/usr/bin/env python3
import datetime
from send_bot_alert import send_telegram_bot_alert

class TankFraudDetector:
    def __init__(self, vehicle_id, tank_capacity):
        self.vehicle_id = vehicle_id
        self.tank_capacity = tank_capacity
        self.readings = []
        self.fraud_threshold = 20.0  # 20% sudden drop = fraud
        
    def add_reading(self, fuel_level, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        
        if fuel_level < 0 or fuel_level > self.tank_capacity:
            return False, "Invalid fuel level"
            
        self.readings.append({
            'timestamp': timestamp,
            'fuel_level': fuel_level,
            'percentage': (fuel_level / self.tank_capacity) * 100
        })
        return True, "Reading added"
    
    def detect_fraud(self):
        if len(self.readings) < 2:
            return False, "Need at least 2 readings"
            
        current = self.readings[-1]
        previous = self.readings[-2]
        
        drop_percentage = previous['percentage'] - current['percentage']
        time_diff = (current['timestamp'] - previous['timestamp']).total_seconds() / 60  # minutes
        
        if drop_percentage >= self.fraud_threshold and time_diff < 60:  # 20% drop in <1 hour
            return True, {
                'drop_percentage': drop_percentage,
                'time_diff': time_diff,
                'previous_level': previous['fuel_level'],
                'current_level': current['fuel_level']
            }
        return False, "Normal consumption"
    
    def check_linkage(self):
        if len(self.readings) < 3:
            return "Need more readings"
            
        recent = self.readings[-3:]
        drops = []
        
        for i in range(1, len(recent)):
            drop = recent[i-1]['percentage'] - recent[i]['percentage']
            drops.append(drop)
            
        avg_drop = sum(drops) / len(drops)
        
        if avg_drop > 15:
            return "LINKAGE DETECTED - Consistent high fuel loss"
        elif avg_drop > 5:
            return "POSSIBLE LINKAGE - Monitor closely"
        else:
            return "NORMAL - No linkage detected"

def interactive_test():
    print("=== DIESEL TANK FRAUD DETECTION TEST ===")
    
    vehicle_id = input("Enter Vehicle ID: ").strip()
    tank_capacity = float(input("Enter Tank Capacity (Liters): "))
    
    detector = TankFraudDetector(vehicle_id, tank_capacity)
    
    while True:
        print(f"\n--- {vehicle_id} (Capacity: {tank_capacity}L) ---")
        print("1. Add Fuel Reading")
        print("2. Check for Fraud")
        print("3. Check Diesel Linkage")
        print("4. View All Readings")
        print("5. Simulate Fraud Scenario")
        print("6. Exit")
        
        choice = input("Choose option: ").strip()
        
        if choice == '1':
            try:
                fuel_level = float(input("Enter current fuel level (Liters): "))
                success, msg = detector.add_reading(fuel_level)
                if success:
                    percentage = (fuel_level / tank_capacity) * 100
                    print(f"✓ Reading added: {fuel_level}L ({percentage:.1f}%)")
                else:
                    print(f"✗ Error: {msg}")
            except ValueError:
                print("✗ Invalid input")
                
        elif choice == '2':
            is_fraud, result = detector.detect_fraud()
            if is_fraud:
                alert_msg = f"""🚨 FUEL FRAUD DETECTED 🚨
Vehicle: {vehicle_id}
Previous: {result['previous_level']:.1f}L
Current: {result['current_level']:.1f}L
Drop: {result['drop_percentage']:.1f}%
Time: {result['time_diff']:.1f} minutes
Status: CRITICAL"""
                print(alert_msg)
                send_telegram_bot_alert(alert_msg)
            else:
                print(f"✓ {result}")
                
        elif choice == '3':
            linkage_status = detector.check_linkage()
            print(f"Linkage Status: {linkage_status}")
            if "DETECTED" in linkage_status:
                alert_msg = f"⚠️ DIESEL LINKAGE ALERT\nVehicle: {vehicle_id}\nStatus: {linkage_status}"
                send_telegram_bot_alert(alert_msg)
                
        elif choice == '4':
            print("\nAll Readings:")
            for i, reading in enumerate(detector.readings, 1):
                print(f"{i}. {reading['timestamp'].strftime('%H:%M:%S')} - {reading['fuel_level']:.1f}L ({reading['percentage']:.1f}%)")
                
        elif choice == '5':
            print("Simulating fraud scenario...")
            # Add normal reading
            detector.add_reading(tank_capacity * 0.8)  # 80%
            print("✓ Added normal reading: 80%")
            
            # Add fraud reading (sudden drop)
            detector.add_reading(tank_capacity * 0.2)  # 20%
            print("✓ Added fraud reading: 20%")
            
            # Check fraud
            is_fraud, result = detector.detect_fraud()
            if is_fraud:
                print(f"🚨 FRAUD DETECTED: {result['drop_percentage']:.1f}% drop")
            
        elif choice == '6':
            break
            
        else:
            print("Invalid option")

if __name__ == '__main__':
    interactive_test()