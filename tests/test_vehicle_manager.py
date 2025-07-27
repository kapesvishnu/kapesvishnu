import unittest
import os
import json
from src.vehicle_manager import VehicleManager

class TestVehicleManager(unittest.TestCase):

    def setUp(self):
        self.data_file = 'tests/test_vehicles.json'
        self.manager = VehicleManager(data_file=self.data_file)

    def tearDown(self):
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    def test_register_vehicle(self):
        self.assertTrue(self.manager.register_vehicle('test_vehicle_1'))
        self.assertIn('test_vehicle_1', self.manager.vehicles)
        self.assertFalse(self.manager.register_vehicle('test_vehicle_1'))

    def test_record_daily_update(self):
        self.manager.register_vehicle('test_vehicle_1')
        self.assertTrue(self.manager.record_daily_update('test_vehicle_1', 80))
        self.assertEqual(len(self.manager.vehicles['test_vehicle_1']['readings']), 1)
        self.assertFalse(self.manager.record_daily_update('test_vehicle_2', 80))

if __name__ == '__main__':
    unittest.main()
