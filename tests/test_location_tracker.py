import unittest
from src.location_tracker import LocationTracker

class TestLocationTracker(unittest.TestCase):

    def test_get_live_location(self):
        tracker = LocationTracker("test_vehicle")
        initial_location = tracker.location
        new_location = tracker.get_live_location()
        self.assertNotEqual(initial_location, new_location)

    def test_estimate_mileage(self):
        tracker = LocationTracker("test_vehicle")
        self.assertEqual(tracker.estimate_mileage(10, 100), 10)
        self.assertEqual(tracker.estimate_mileage(0, 100), 0)

if __name__ == '__main__':
    unittest.main()
