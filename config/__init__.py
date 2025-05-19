import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Initialisation des extensions
db = SQLAlchemy()

def init_config(app):
    """Charge la configuration de l'application"""
    # Chargement des variables d'environnement
    load_dotenv()
    
    # Configuration de base
    app.config.from_mapping(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    )
    
    # Configuration DB
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    # Initialisation des extensions
    db.init_app(app)