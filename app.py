from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config.database import db, configure_database
from dotenv import load_dotenv
import os
from datetime import timedelta

import models

# Chargement des variables d'environnement
load_dotenv()

def create_app():
    """Factory principale de l'application Flask"""
    
    # Initialisation de Flask
    app = Flask(__name__)
    
    # Configuration de base
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-change-me')
    
    # Configuration JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    
    # Initialisation des extensions
    configure_database(app)
    jwt = JWTManager(app)
    
    # Import des blueprints
    from api.auth import auth_bp
    from api.projects import projects_bp
    from api.modules import modules_bp
    
    # Enregistrement des blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(modules_bp)
    
    # Gestion des erreurs globales
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    # Health Check
    @app.route('/health')
    def health():
        from config.database import health_check
        db_status, db_message = health_check()
        return jsonify({
            "status": "OK",
            "database": db_message,
            "components": ["auth", "projects", "modules"]
        })
    
    # Shell Context
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': models.user.User,
            'Project': models.project.Project,
            'Module': models.module.Module
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', True))