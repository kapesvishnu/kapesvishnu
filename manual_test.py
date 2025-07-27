#!/usr/bin/env python3
from src.vehicle_manager import VehicleManager

def main():
    vm = VehicleManager('data/test_vehicles.json')
    
    while True:
        print("\n=== Vehicle Manager Test ===")
        print("1. Register Vehicle")
        print("2. Record Fuel Reading")
        print("3. View Vehicles")
        print("4. Exit")
        
        choice = input("Choose option: ")
        
        if choice == '1':
            vehicle_id = input("Enter vehicle ID: ")
            if vm.register_vehicle(vehicle_id):
                print(f"✓ Vehicle {vehicle_id} registered")
            else:
                print("✗ Failed to register vehicle")
                
        elif choice == '2':
            vehicle_id = input("Enter vehicle ID: ")
            fuel_level = input("Enter fuel level (0-100): ")
            if vm.record_daily_update(vehicle_id, fuel_level):
                print("✓ Fuel reading recorded")
            else:
                print("✗ Failed to record reading")
                
        elif choice == '3':
            print("\nVehicles:")
            for vid, data in vm.vehicles.items():
                print(f"- {vid}: {len(data['readings'])} readings")
                
        elif choice == '4':
            break

if __name__ == '__main__':
    main()