import unittest
from src.vehicle_manager import VehicleManager

class TestInputValidation(unittest.TestCase):

    def setUp(self):
        self.manager = VehicleManager(data_file='tests/test_input.json')

    def test_invalid_fuel_level(self):
        self.manager.register_vehicle('test_vehicle')
        self.assertFalse(self.manager.record_daily_update('test_vehicle', -10))
        self.assertFalse(self.manager.record_daily_update('test_vehicle', 150))

    def test_empty_vehicle_id(self):
        self.assertFalse(self.manager.register_vehicle(''))
        self.assertFalse(self.manager.register_vehicle(None))

    def test_non_numeric_fuel(self):
        self.manager.register_vehicle('test_vehicle')
        self.assertFalse(self.manager.record_daily_update('test_vehicle', 'invalid'))

if __name__ == '__main__':
    unittest.main()