import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

db = SQLAlchemy()

def configure_database(app):
    """Configure la connexion à la base de données avec optimisations"""
    
    # Configuration PostgreSQL avec pool de connexions
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/kaizenflow')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_pre_ping': True,  # Vérifie les connexions avant utilisation
        'pool_recycle': 3600    # Recyclage des connexions toutes les heures
    }
    
    # Désactive le tracking des modifications (améliore les performances)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation de l'extension
    db.init_app(app)
    
    # Configuration spécifique pour SQLite (dev) / PostgreSQL (prod)
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        configure_sqlite_pragmas()

@event.listens_for(Engine, "connect")
def set_sqlite_pragmas(dbapi_connection, connection_record):
    """Active les optimisations SQLite si utilisé en développement"""
    if 'sqlite' in os.getenv('DATABASE_URL', ''):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()

def configure_sqlite_pragmas():
    """Configure les pragmas SQLite au niveau du moteur"""
    from sqlalchemy import create_engine
    engine = create_engine(os.getenv('DATABASE_URL'))
    with engine.connect() as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA journal_mode=WAL")

def health_check():
    """Vérifie que la connexion à la base est active"""
    try:
        db.session.execute('SELECT 1')
        return True, "Database connection OK"
    except Exception as e:
        return False, str(e)