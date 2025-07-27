import json
import os
from datetime import datetime

class VehicleManager:
    def __init__(self, data_file='data/vehicles.json'):
        self.data_file = data_file
        self.vehicles = self._load_vehicles()

    def _load_vehicles(self):
        if not os.path.exists(self.data_file):
            return {}
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def _save_vehicles(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.vehicles, f, indent=4)

    def register_vehicle(self, vehicle_id):
        if not vehicle_id or vehicle_id in self.vehicles:
            return False
        self.vehicles[vehicle_id] = {'readings': []}
        self._save_vehicles()
        return True

    def record_daily_update(self, vehicle_id, fuel_level):
        if vehicle_id not in self.vehicles:
            return False
        try:
            fuel_level = float(fuel_level)
            if fuel_level < 0 or fuel_level > 100:
                return False
        except (ValueError, TypeError):
            return False
        today = datetime.now().strftime('%Y-%m-%d')
        self.vehicles[vehicle_id]['readings'].append({'date': today, 'fuel_level': fuel_level})
        self._save_vehicles()
        return True
