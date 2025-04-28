"""
API REST pour le calcul d'indicateurs de santé.

Cette API fournit des endpoints pour calculer :
- L'Indice de Masse Corporelle (IMC/BMI)
- Le Métabolisme de Base (BMR)

La documentation Swagger est disponible à la racine de l'API.
"""

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from src.utils.health_utils import calculate_bmi, calculate_bmr

# Initialisation de l'application Flask
app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Health Calculator API",
    description="Une API pour calculer l'IMC et le BMR",
)

# Modèles de données pour Swagger
bmi_model = api.model(
    "BMI",
    {
        "height": fields.Float(required=True, description="Taille en mètres"),
        "weight": fields.Float(required=True, description="Poids en kilogrammes"),
    },
)

bmr_model = api.model(
    "BMR",
    {
        "height": fields.Float(required=True, description="Taille en centimètres"),
        "weight": fields.Float(required=True, description="Poids en kilogrammes"),
        "age": fields.Integer(required=True, description="Âge en années"),
        "gender": fields.String(required=True, description="Genre (male/female)"),
    },
)


@api.route("/health")
class Health(Resource):
    """Endpoint pour vérifier l'état de l'API."""

    def get(self):
        """
        Vérifie l'état de l'API.

        Returns:
            dict: Statut de l'API
        """
        return {"status": "healthy"}


@api.route("/bmi")
class BMI(Resource):
    """Endpoint pour le calcul de l'IMC."""

    @api.expect(bmi_model)
    @api.response(200, "Succès")
    @api.response(400, "Données invalides")
    def post(self):
        """
        Calcule l'Indice de Masse Corporelle (IMC).

        Returns:
            dict: Valeur de l'IMC ou message d'erreur
        """
        try:
            data = request.get_json()
            height = data.get("height")
            weight = data.get("weight")

            if not height or not weight:
                return {"error": "Les champs height et weight sont requis"}, 400

            if height <= 0 or weight <= 0:
                return {"error": "Les valeurs doivent être positives"}, 400

            bmi_value = calculate_bmi(height, weight)
            return {"bmi": bmi_value}
        except Exception as e:
            return {"error": str(e)}, 400


@api.route("/bmr")
class BMR(Resource):
    """Endpoint pour le calcul du BMR."""

    @api.expect(bmr_model)
    @api.response(200, "Succès")
    @api.response(400, "Données invalides")
    def post(self):
        """
        Calcule le Métabolisme de Base (BMR).

        Returns:
            dict: Valeur du BMR ou message d'erreur
        """
        try:
            data = request.get_json()
            height = data.get("height")
            weight = data.get("weight")
            age = data.get("age")
            gender = data.get("gender")

            if not all([height, weight, age, gender]):
                return {"error": "Tous les champs sont requis"}, 400

            if height <= 0 or weight <= 0 or age <= 0:
                return {"error": "Les valeurs doivent être positives"}, 400

            if gender.lower() not in ["male", "female"]:
                return {"error": "Le genre doit être 'male' ou 'female'"}, 400

            bmr_value = calculate_bmr(height, weight, age, gender)
            return {"bmr": bmr_value}
        except Exception as e:
            return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
