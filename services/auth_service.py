import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from models.user import User
from app import db

class AuthService:
    @staticmethod
    def register_user(email: str, password: str):
        """Enregistre un nouvel utilisateur"""
        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 400
        
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return {
            "message": "User created successfully",
            "user_id": new_user.id
        }, 201

    @staticmethod
    def login_user(email: str, password: str):
        """Connecte un utilisateur et retourne un JWT"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return {"error": "Invalid credentials"}, 401
        
        # Création du token JWT valable 24h
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24),
            additional_claims={"email": user.email}
        )
        
        return {
            "access_token": access_token,
            "user_id": user.id
        }, 200

    @staticmethod
    def get_user_profile(user_id: int):
        """Récupère le profil utilisateur"""
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
            
        return {
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        }, 200