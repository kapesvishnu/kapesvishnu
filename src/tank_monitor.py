import random
import time
from src.notifications import send_telegram_alert, send_email_alert
import asyncio

class TankMonitor:
    def __init__(self, vehicle_id, initial_fuel_level=100):
        self.vehicle_id = vehicle_id
        self.fuel_level = initial_fuel_level
        self.readings = [(time.time(), initial_fuel_level)]

    def get_reading(self):
        # Simulate a gradual decrease in fuel level
        self.fuel_level -= random.uniform(0.1, 0.5)
        self.readings.append((time.time(), self.fuel_level))
        return self.fuel_level

    def check_for_sudden_drop(self, drop_threshold=10):
        if len(self.readings) < 2:
            return False

        last_reading_time, last_fuel_level = self.readings[-1]
        previous_reading_time, previous_fuel_level = self.readings[-2]

        fuel_drop = previous_fuel_level - last_fuel_level

        if fuel_drop > drop_threshold:
            message = f"Sudden fuel drop detected for vehicle {self.vehicle_id}! Drop of {fuel_drop} units."
            asyncio.run(send_telegram_alert(message))
            send_email_alert("Sudden Fuel Drop Alert", message)
            return True

        return False
