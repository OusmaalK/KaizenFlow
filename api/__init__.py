from flask import Blueprint
from flask_jwt_extended import JWTManager

api_bp = Blueprint('api', __name__, url_prefix='/api')

def init_api(app):
    """Enregistre tous les blueprints d'API"""
    from .auth import auth_bp
    from .projects import projects_bp
    from .modules import modules_bp
    
    # Enregistrement des blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(modules_bp)
    
    # Configuration JWT
    jwt = JWTManager(app)
    
    # Callbacks JWT personnalisés
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from ..models.user import User
        identity = jwt_data["sub"]
        return User.query.get(identity)