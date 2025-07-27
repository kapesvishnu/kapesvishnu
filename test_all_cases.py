#!/usr/bin/env python3
import asyncio
import time
from src.vehicle_manager import VehicleManager
from src.tank_monitor import TankMonitor
from src.location_tracker import LocationTracker
from send_bot_alert import send_telegram_bot_alert

def test_vehicle_manager():
    print("=== TESTING VEHICLE MANAGER ===")
    vm = VehicleManager('data/test_all.json')
    
    # Test valid cases
    print("✓ Valid registration:", vm.register_vehicle("TRUCK001"))
    print("✓ Valid fuel update:", vm.record_daily_update("TRUCK001", 85.5))
    
    # Test invalid cases
    print("✗ Empty vehicle ID:", vm.register_vehicle(""))
    print("✗ Duplicate registration:", vm.register_vehicle("TRUCK001"))
    print("✗ Invalid fuel level:", vm.record_daily_update("TRUCK001", -10))
    print("✗ Non-numeric fuel:", vm.record_daily_update("TRUCK001", "abc"))
    print("✗ Unregistered vehicle:", vm.record_daily_update("TRUCK999", 50))

def test_tank_monitor():
    print("\n=== TESTING TANK MONITOR ===")
    tm = TankMonitor("TRUCK001", 90.0)
    
    # Test normal readings
    reading = tm.get_reading()
    print(f"✓ Normal reading: {reading:.1f}%")
    
    # Simulate sudden drop
    tm.fuel_level = 20.0
    tm.readings.append((time.time(), 20.0))
    drop_detected = tm.check_for_sudden_drop()
    print(f"✓ Sudden drop detected: {drop_detected}")

def test_location_tracker():
    print("\n=== TESTING LOCATION TRACKER ===")
    lt = LocationTracker("TRUCK001")
    
    # Test location updates
    location = lt.get_live_location()
    print(f"✓ Current location: {location}")
    
    mileage = lt.estimate_mileage(10.5, 150.0)
    print(f"✓ Estimated mileage: {mileage:.1f} km/L")

def test_notifications():
    print("\n=== TESTING NOTIFICATIONS ===")
    
    # Test different alert scenarios
    scenarios = [
        {"vehicle": "TRUCK001", "prev": 90.5, "curr": 15.2, "type": "CRITICAL"},
        {"vehicle": "VAN002", "prev": 75.0, "curr": 45.8, "type": "WARNING"},
        {"vehicle": "BUS003", "prev": 95.3, "curr": 5.1, "type": "EMERGENCY"}
    ]
    
    for scenario in scenarios:
        drop = scenario["prev"] - scenario["curr"]
        message = f"""🚨 FUEL {scenario["type"]} 🚨
Vehicle: {scenario["vehicle"]}
Previous: {scenario["prev"]}%
Current: {scenario["curr"]}%
Drop: {drop:.1f}%"""
        
        print(f"✓ Sending {scenario['type']} alert for {scenario['vehicle']}")
        send_telegram_bot_alert(message)
        time.sleep(1)  # Avoid rate limiting

def test_dashboard_data():
    print("\n=== TESTING DASHBOARD DATA ===")
    vm = VehicleManager('data/vehicles.json')
    
    # Add test vehicles
    vehicles = ["TRUCK001", "VAN002", "BUS003"]
    fuel_levels = [85.5, 67.2, 92.1]
    
    for vehicle, fuel in zip(vehicles, fuel_levels):
        vm.register_vehicle(vehicle)
        vm.record_daily_update(vehicle, fuel)
        print(f"✓ Added {vehicle} with {fuel}% fuel")
    
    print(f"✓ Total vehicles in system: {len(vm.vehicles)}")

async def run_all_tests():
    print("DIESEL TANK MONITORING SYSTEM - COMPREHENSIVE TEST")
    print("=" * 60)
    
    test_vehicle_manager()
    test_tank_monitor()
    test_location_tracker()
    test_notifications()
    test_dashboard_data()
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("Check Telegram for alert notifications")

if __name__ == '__main__':
    asyncio.run(run_all_tests())