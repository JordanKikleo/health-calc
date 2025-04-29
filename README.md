# Health Calculator API

Une API REST pour calculer l'IMC (BMI) et le métabolisme de base (BMR).

## Fonctionnalités

- Calcul de l'IMC (BMI)
- Calcul du métabolisme de base (BMR)
- Interface utilisateur web
- Tests automatisés
- Containerisation Docker
- Pipeline CI/CD avec GitHub Actions

## Prérequis

- Python 3.8+
- Docker (optionnel)
- Make (optionnel)

## Installation

### Installation locale

1. Cloner le repository :
```bash
git clone https://github.com/votre-username/health-calc.git
cd health-calc
```

2. Créer et activer un environnement virtuel :

#### Sur Linux/macOS :
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate
```

#### Sur Windows :
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\activate
```

3. Installer les dépendances :

#### Méthode 1 : Utilisation de Make (recommandée)
```bash
# S'assurer que l'environnement virtuel est activé
make init
```

#### Méthode 2 : Installation manuelle
```bash
# S'assurer que l'environnement virtuel est activé
pip install -r requirements.txt
```

4. Vérifier l'installation :
```bash
# Vérifier que les packages sont bien installés
pip list
```

Vous devriez voir les packages suivants installés :
- Flask==2.3.2
- Flask-cors==4.0.0
- Werkzeug==2.3.4
- pytest==7.3.1

### Installation avec Docker

```bash
make build
```

## Utilisation

### Démarrer l'API

#### Localement
```bash
# S'assurer que l'environnement virtuel est activé
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows

# Lancer l'API
make run
```

#### Avec Docker
```bash
docker run -p 5000:5000 health-calculator-service
```

### Accéder à l'interface utilisateur

Ouvrez votre navigateur et accédez à :
```
http://localhost:5000/
```

### Endpoints API

#### Vérifier l'état de l'API
```bash
curl http://localhost:5000/api/health
```

#### Calcul de l'IMC (BMI)
```bash
curl -X POST http://localhost:5000/api/bmi \
  -H "Content-Type: application/json" \
  -d '{"height": 1.75, "weight": 70}'
```

#### Calcul du BMR
```bash
curl -X POST http://localhost:5000/api/bmr \
  -H "Content-Type: application/json" \
  -d '{"height": 175, "weight": 70, "age": 30, "gender": "male"}'
```

## Tests

Exécuter les tests :
```bash
# S'assurer que l'environnement virtuel est activé
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows

# Lancer les tests
make test
```

## Développement

### Structure du projet
```
.
├── src/
│   ├── api/
│   │   └── app.py              # Application principale
│   ├── utils/
│   │   └── health_utils.py     # Fonctions de calcul
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Styles CSS
│   │   └── js/
│   │       └── script.js       # JavaScript
│   └── templates/
│       └── index.html          # Template HTML
├── tests/
│   └── test.py                 # Tests unitaires
├── Dockerfile                  # Configuration Docker
├── Makefile                    # Commandes d'automatisation
└── requirements.txt            # Dépendances Python
```

### Commandes Make disponibles

- `make init` : Installer les dépendances
- `make run` : Démarrer l'API
- `make test` : Exécuter les tests
- `make build` : Construire l'image Docker
- `make clean` : Nettoyer les fichiers temporaires

### Désactiver l'environnement virtuel

Quand vous avez terminé de travailler sur le projet, vous pouvez désactiver l'environnement virtuel :

```bash
deactivate
```

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.