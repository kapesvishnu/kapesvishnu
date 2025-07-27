import unittest
from src.dashboard import app

class TestDashboard(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_dashboard_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Diesel Tank Monitoring Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()
