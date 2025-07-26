import random

class LocationTracker:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.location = (round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6))

    def get_live_location(self):
        # Simulate location change
        lat, lon = self.location
        lat += random.uniform(-0.01, 0.01)
        lon += random.uniform(-0.01, 0.01)
        self.location = (round(lat, 6), round(lon, 6))
        return self.location

    def estimate_mileage(self, fuel_consumed, distance_traveled):
        if fuel_consumed <= 0:
            return 0
        return distance_traveled / fuel_consumed
