from datetime import datetime
from models.project import Project
from models.user import User
from app import db

class ProjectService:
    @staticmethod
    def create_project(user_id: int, name: str, description: str = None):
        """Crée un nouveau projet"""
        if not User.query.get(user_id):
            return {"error": "User not found"}, 404
            
        new_project = Project(
            name=name,
            description=description,
            owner_id=user_id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_project)
        db.session.commit()
        
        return {
            "message": "Project created",
            "project_id": new_project.id
        }, 201

    @staticmethod
    def get_user_projects(user_id: int):
        """Liste tous les projets d'un utilisateur"""
        projects = Project.query.filter_by(owner_id=user_id).all()
        
        return {
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "created_at": p.created_at.isoformat()
                } for p in projects
            ]
        }, 200

    @staticmethod
    def update_project(project_id: int, user_id: int, **kwargs):
        """Met à jour un projet existant"""
        project = Project.query.filter_by(
            id=project_id,
            owner_id=user_id
        ).first()
        
        if not project:
            return {"error": "Project not found or unauthorized"}, 404
            
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
                
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return {"message": "Project updated"}, 200

    @staticmethod
    def delete_project(project_id: int, user_id: int):
        """Supprime un projet"""
        project = Project.query.filter_by(
            id=project_id,
            owner_id=user_id
        ).first()
        
        if not project:
            return {"error": "Project not found or unauthorized"}, 404
            
        db.session.delete(project)
        db.session.commit()
        
        return {"message": "Project deleted"}, 200