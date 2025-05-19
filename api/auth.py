from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from services.auth_service import AuthService
from schemas import UserLoginSchema, UserRegisterSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Enregistrement d'un nouvel utilisateur"""
    data = UserRegisterSchema().load(request.get_json())
    return AuthService.register_user(data['email'], data['password'])

@auth_bp.route('/login', methods=['POST'])
def login():
    """Connexion et génération du token JWT"""
    data = UserLoginSchema().load(request.get_json())
    return AuthService.login_user(data['email'], data['password'])

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Récupération du profil utilisateur (protégé par JWT)"""
    user_id = get_jwt_identity()
    return AuthService.get_user_profile(user_id)