"""
Tests unitaires pour l'API de calcul d'indicateurs de santé.

Ce module contient les tests pour :
- Les fonctions de calcul (health_utils.py)
- Les endpoints de l'API (app.py)
- Les templates et l'interface utilisateur
"""

import unittest
import os
from src.utils.health_utils import calculate_bmi, calculate_bmr
from src.api.app import app
import json


class TestHealthUtils(unittest.TestCase):
    """Tests pour les fonctions de calcul dans health_utils.py."""

    def test_calculate_bmi(self):
        """Test du calcul de l'IMC avec des valeurs valides."""
        self.assertAlmostEqual(calculate_bmi(1.75, 70), 22.86, places=2)

    def test_calculate_bmr_male(self):
        """Test du calcul du BMR pour un homme."""
        self.assertAlmostEqual(calculate_bmr(175, 70, 25, "male"), 1724.05, places=2)

    def test_calculate_bmr_female(self):
        """Test du calcul du BMR pour une femme."""
        self.assertAlmostEqual(calculate_bmr(165, 60, 30, "female"), 1383.68, places=2)


class TestHealthAPI(unittest.TestCase):
    """Tests pour les endpoints de l'API."""

    def setUp(self):
        """Configuration initiale pour les tests d'API."""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        """Test de l'endpoint de santé."""
        response = self.app.get("/api/health")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "healthy")

    def test_bmi_valid_input(self):
        """Test du calcul de l'IMC avec des entrées valides."""
        data = {"height": 1.75, "weight": 70}
        response = self.app.post(
            "/api/bmi", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("bmi", data)

    def test_bmi_missing_fields(self):
        """Test du calcul de l'IMC avec des champs manquants."""
        data = {"height": 1.75}
        response = self.app.post(
            "/api/bmi", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_bmi_negative_values(self):
        """Test du calcul de l'IMC avec des valeurs négatives."""
        data = {"height": -1.75, "weight": 70}
        response = self.app.post(
            "/api/bmi", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_bmr_valid_input(self):
        """Test du calcul du BMR avec des entrées valides."""
        data = {"height": 175, "weight": 70, "age": 30, "gender": "male"}
        response = self.app.post(
            "/api/bmr", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("bmr", data)

    def test_bmr_missing_fields(self):
        """Test du calcul du BMR avec des champs manquants."""
        data = {"height": 175, "weight": 70}
        response = self.app.post(
            "/api/bmr", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_bmr_invalid_gender(self):
        """Test du calcul du BMR avec un genre invalide."""
        data = {"height": 175, "weight": 70, "age": 30, "gender": "invalid"}
        response = self.app.post(
            "/api/bmr", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)


class TestApp(unittest.TestCase):
    """Tests pour l'application Flask."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.app = app.test_client()
        self.app.testing = True

    def test_template_exists(self):
        """Test si le template index.html existe."""
        template_path = os.path.join(app.template_folder, 'index.html')
        self.assertTrue(os.path.exists(template_path), f"Le template n'existe pas: {template_path}")

    def test_index_route(self):
        """Test de la route /."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
