import unittest
import unittest.mock
from src.tank_monitor import TankMonitor

class TestTankMonitor(unittest.TestCase):

    def test_initial_fuel_level(self):
        tank = TankMonitor("test_vehicle")
        self.assertEqual(tank.fuel_level, 100)

    def test_get_reading(self):
        tank = TankMonitor("test_vehicle")
        initial_level = tank.fuel_level
        new_level = tank.get_reading()
        self.assertLess(new_level, initial_level)

    def test_sudden_drop(self):
        with unittest.mock.patch('src.tank_monitor.send_telegram_alert') as mock_send_telegram_alert, \
             unittest.mock.patch('src.tank_monitor.send_email_alert') as mock_send_email_alert:
            tank = TankMonitor("test_vehicle")
            tank.fuel_level = 80
            tank.readings.append((0, 80))
            tank.fuel_level = 60
            tank.readings.append((1, 60))
            self.assertTrue(tank.check_for_sudden_drop(drop_threshold=15))
            mock_send_telegram_alert.assert_called_once()
            mock_send_email_alert.assert_called_once()

            # Reset the mocks for the next assertion
            mock_send_telegram_alert.reset_mock()
            mock_send_email_alert.reset_mock()

            self.assertFalse(tank.check_for_sudden_drop(drop_threshold=25))
            mock_send_telegram_alert.assert_not_called()
            mock_send_email_alert.assert_not_called()

if __name__ == '__main__':
    unittest.main()
