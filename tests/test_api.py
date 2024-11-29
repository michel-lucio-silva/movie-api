import unittest
from app import create_app, load_csv_to_db

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        with self.app.app_context():
            load_csv_to_db('data/movies.csv')

    def test_award_intervals(self):
        with self.app.test_client() as client:
            response = client.get('/producers/award-intervals')
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertIn("min", data)
            self.assertIn("max", data)

if __name__ == '__main__':
    unittest.main()
