"""
Module contenant les fonctions de calcul pour les indicateurs de santé.

Ce module fournit des fonctions pour calculer :
- L'Indice de Masse Corporelle (IMC/BMI)
- Le Métabolisme de Base (BMR)
"""

def calculate_bmi(height: float, weight: float) -> float:
    """
    Calcule l'Indice de Masse Corporelle (IMC/BMI).

    Args:
        height (float): Taille en mètres
        weight (float): Poids en kilogrammes

    Returns:
        float: Valeur de l'IMC

    Raises:
        ValueError: Si height ou weight sont négatifs ou nuls
    """
    if height <= 0 or weight <= 0:
        raise ValueError("La taille et le poids doivent être positifs")
    return weight / (height**2)


def calculate_bmr(height: float, weight: float, age: int, gender: str) -> float:
    """
    Calcule le Métabolisme de Base (BMR) selon l'équation de Mifflin-St Jeor.

    Args:
        height (float): Taille en centimètres
        weight (float): Poids en kilogrammes
        age (int): Âge en années
        gender (str): Genre ('male' ou 'female')

    Returns:
        float: Valeur du BMR en calories par jour

    Raises:
        ValueError: Si les paramètres sont invalides
    """
    if height <= 0 or weight <= 0 or age <= 0:
        raise ValueError("La taille, le poids et l'âge doivent être positifs")
        
    if gender.lower() not in ["male", "female"]:
        raise ValueError("Le genre doit être 'male' ou 'female'")

    if gender.lower() == "male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:  # female
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
