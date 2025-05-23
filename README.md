# KaizenFlow Project
# KaizenFlow™ - Optimisation Continue des Processus Métiers

![CI Status](https://github.com/OusmaalK/KaizenFlow/actions/workflows/python-ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> Plateforme d'amélioration continue pour la gestion agile des projets et modules métiers

## 🚀 Fonctionnalités Clés
- **Gestion des Projets** : Création, suivi et analyse des projets
- **Modules Customisables** : Activation/désactivation des fonctionnalités par projet
- **Workflow Kaizen** : Implémentation des méthodologies PDCA (Plan-Do-Check-Act)
- **Tableau de Bord** : Visualisation des indicateurs de performance (KPI)

## 📦 Installation
### Prérequis
- Python 3.10+
- PostgreSQL 13+
- Git

### Configuration
```bash
# Cloner le dépôt
git clone https://github.com/OusmaalK/KaizenFlow.git
cd KaizenFlow

# Configurer l'environnement
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Configurer la base de données
flask db upgrade