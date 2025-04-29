"""
API REST pour le calcul d'indicateurs de santé.

Cette API fournit des endpoints pour calculer :
- L'Indice de Masse Corporelle (IMC/BMI)
- Le Métabolisme de Base (BMR)

La documentation Swagger est disponible à /api
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flasgger import Swagger, swag_from
import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.health_utils import calculate_bmi, calculate_bmr

# Obtenir le chemin absolu du dossier src
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)

# Initialisation de l'application Flask avec le bon chemin pour les templates
template_dir = os.path.abspath(os.path.join(SRC_DIR, 'templates'))
static_dir = os.path.abspath(os.path.join(SRC_DIR, 'static'))

# Initialisation de l'application Flask
app = Flask(__name__,
           template_folder=template_dir,
           static_folder=static_dir,
           static_url_path='/static')

# Configuration de Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Health Calculator API",
        "description": "API pour le calcul d'indicateurs de santé",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Configuration CORS
CORS(app)

# Route pour l'interface utilisateur
@app.route('/')
def index():
    """Page d'accueil avec l'interface utilisateur."""
    return render_template('index.html')

# Route pour servir les fichiers statiques
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Sert les fichiers statiques."""
    return send_from_directory(app.static_folder, filename)

# Route pour vérifier l'état de l'API
@app.route('/api/health')
@swag_from({
    'responses': {
        200: {
            'description': 'État de l\'API',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'}
                }
            }
        }
    }
})
def health():
    """Vérifie l'état de l'API."""
    return jsonify({"status": "healthy"})

# Route pour le calcul de l'IMC
@app.route('/api/bmi', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'height': {'type': 'number', 'description': 'Taille en mètres'},
                    'weight': {'type': 'number', 'description': 'Poids en kilogrammes'}
                },
                'required': ['height', 'weight']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'IMC calculé',
            'schema': {
                'type': 'object',
                'properties': {
                    'bmi': {'type': 'number'}
                }
            }
        },
        400: {
            'description': 'Erreur de validation',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def bmi():
    """Calcule l'Indice de Masse Corporelle (IMC)."""
    try:
        data = request.get_json()
        height = data.get("height")
        weight = data.get("weight")

        if not height or not weight:
            return jsonify({"error": "Les champs height et weight sont requis"}), 400

        if height <= 0 or weight <= 0:
            return jsonify({"error": "Les valeurs doivent être positives"}), 400

        bmi_value = calculate_bmi(height, weight)
        return jsonify({"bmi": bmi_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route pour le calcul du BMR
@app.route('/api/bmr', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'height': {'type': 'number', 'description': 'Taille en mètres'},
                    'weight': {'type': 'number', 'description': 'Poids en kilogrammes'},
                    'age': {'type': 'integer', 'description': 'Âge en années'},
                    'gender': {'type': 'string', 'description': 'Genre (male/female)'}
                },
                'required': ['height', 'weight', 'age', 'gender']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'BMR calculé',
            'schema': {
                'type': 'object',
                'properties': {
                    'bmr': {'type': 'number'}
                }
            }
        },
        400: {
            'description': 'Erreur de validation',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def bmr():
    """Calcule le Métabolisme de Base (BMR)."""
    try:
        data = request.get_json()
        height = data.get("height")
        weight = data.get("weight")
        age = data.get("age")
        gender = data.get("gender")

        if not all([height, weight, age, gender]):
            return jsonify({"error": "Tous les champs sont requis"}), 400

        if height <= 0 or weight <= 0 or age <= 0:
            return jsonify({"error": "Les valeurs doivent être positives"}), 400

        if gender.lower() not in ["male", "female"]:
            return jsonify({"error": "Le genre doit être 'male' ou 'female'"}), 400

        bmr_value = calculate_bmr(height, weight, age, gender)
        return jsonify({"bmr": bmr_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)