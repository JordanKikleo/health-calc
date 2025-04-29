"""
Test de l'application Flask.
"""

import os
import sys
import unittest

# Ajouter le répertoire courant au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestApp(unittest.TestCase):
    """Test de l'application Flask."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        self.app = app.test_client()
        self.app.testing = True

    def test_template_exists(self):
        """Test si le template index.html existe."""
        template_path = os.path.join(app.template_folder, 'index.html')
        print(f"Template path: {template_path}")
        self.assertTrue(os.path.exists(template_path), f"Le template n'existe pas: {template_path}")

    def test_index_route(self):
        """Test de la route /."""
        response = self.app.get('/')
        print(f"Response: {response.data}")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main() 