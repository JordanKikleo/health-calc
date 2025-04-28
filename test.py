import unittest
from health_utils import calculate_bmi, calculate_bmr
from app import app
import json


class TestHealthUtils(unittest.TestCase):
    def test_calculate_bmi(self):
        self.assertAlmostEqual(calculate_bmi(1.75, 70), 22.86, places=2)

    def test_calculate_bmr_male(self):
        self.assertAlmostEqual(calculate_bmr(175, 70, 25, "male"), 1724.05, places=2)

    def test_calculate_bmr_female(self):
        self.assertAlmostEqual(calculate_bmr(165, 60, 30, "female"), 1383.68, places=2)


class TestHealthAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        response = self.app.get("/health")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "healthy")

    def test_bmi_valid_input(self):
        data = {"height": 1.75, "weight": 70}
        response = self.app.post(
            "/bmi", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("bmi", data)

    def test_bmi_missing_fields(self):
        data = {"height": 1.75}
        response = self.app.post(
            "/bmi", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_bmi_negative_values(self):
        data = {"height": -1.75, "weight": 70}
        response = self.app.post(
            "/bmi", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_bmr_valid_input(self):
        data = {"height": 175, "weight": 70, "age": 30, "gender": "male"}
        response = self.app.post(
            "/bmr", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("bmr", data)

    def test_bmr_missing_fields(self):
        data = {"height": 175, "weight": 70}
        response = self.app.post(
            "/bmr", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_bmr_invalid_gender(self):
        data = {"height": 175, "weight": 70, "age": 30, "gender": "invalid"}
        response = self.app.post(
            "/bmr", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
