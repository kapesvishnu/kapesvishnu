#!/usr/bin/env python3
import time
from src.vehicle_manager import VehicleManager
from src.tank_monitor import TankMonitor
from src.location_tracker import LocationTracker
from send_bot_alert import send_telegram_bot_alert

def run_all_tests():
    print("DIESEL TANK MONITORING SYSTEM - ALL TESTS")
    print("=" * 50)
    
    # Test 1: Vehicle Manager
    print("1. VEHICLE MANAGER")
    vm = VehicleManager('data/test_all.json')
    print("✓ Valid registration:", vm.register_vehicle("TRUCK001"))
    print("✓ Valid fuel update:", vm.record_daily_update("TRUCK001", 85.5))
    print("✗ Invalid fuel:", vm.record_daily_update("TRUCK001", -10))
    print("✗ Empty vehicle:", vm.register_vehicle(""))
    
    # Test 2: Tank Monitor
    print("\n2. TANK MONITOR")
    tm = TankMonitor("TRUCK001", 90.0)
    reading = tm.get_reading()
    print(f"✓ Fuel reading: {reading:.1f}%")
    
    # Test 3: Location Tracker
    print("\n3. LOCATION TRACKER")
    lt = LocationTracker("TRUCK001")
    location = lt.get_live_location()
    mileage = lt.estimate_mileage(10.5, 150.0)
    print(f"✓ Location: {location}")
    print(f"✓ Mileage: {mileage:.1f} km/L")
    
    # Test 4: Notifications
    print("\n4. TELEGRAM ALERTS")
    alerts = [
        "🚨 CRITICAL: TRUCK001 fuel drop 70.5%",
        "⚠️ WARNING: VAN002 fuel drop 29.2%",
        "🔴 EMERGENCY: BUS003 fuel drop 90.2%"
    ]
    
    for i, alert in enumerate(alerts, 1):
        print(f"✓ Sending alert {i}/3")
        send_telegram_bot_alert(alert)
        time.sleep(1)
    
    # Test 5: Dashboard Data
    print("\n5. DASHBOARD DATA")
    vehicles = ["TRUCK001", "VAN002", "BUS003"]
    for vehicle in vehicles:
        vm.register_vehicle(vehicle)
        vm.record_daily_update(vehicle, 75.0)
        print(f"✓ Added {vehicle}")
    
    print(f"✓ Total vehicles: {len(vm.vehicles)}")
    
    print("\n" + "=" * 50)
    print("ALL TESTS COMPLETED ✓")
    print("Check Telegram for 3 alert messages")

if __name__ == '__main__':
    run_all_tests()