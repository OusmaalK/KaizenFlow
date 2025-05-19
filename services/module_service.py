from datetime import datetime
from typing import List, Dict, Optional
from app import db
from models.module import Module, ActiveModule
from models.project import Project

class ModuleService:
    @staticmethod
    def create_module(name: str, description: str = None, is_core: bool = False) -> Dict:
        """Crée un nouveau module"""
        if Module.query.filter_by(name=name).first():
            return {"error": "Module name already exists"}, 400

        new_module = Module(
            name=name,
            description=description,
            is_core=is_core
        )
        db.session.add(new_module)
        db.session.commit()

        return {
            "message": "Module created successfully",
            "module_id": new_module.id,
            "module": new_module.to_dict()
        }, 201

    @staticmethod
    def get_all_modules() -> List[Dict]:
        """Récupère tous les modules disponibles"""
        modules = Module.query.all()
        return [module.to_dict() for module in modules], 200

    @staticmethod
    def toggle_module_for_project(project_id: int, module_id: int, activate: bool) -> Dict:
        """Active/désactive un module pour un projet spécifique"""
        project = Project.query.get(project_id)
        module = Module.query.get(module_id)

        if not project or not module:
            return {"error": "Project or Module not found"}, 404

        # Vérifie si l'association existe déjà
        association = ActiveModule.query.filter_by(
            project_id=project_id,
            module_id=module_id
        ).first()

        if activate:
            if association:
                if association.is_active:
                    return {"message": "Module already active for this project"}, 200
                association.is_active = True
            else:
                association = ActiveModule(
                    project_id=project_id,
                    module_id=module_id,
                    is_active=True
                )
                db.session.add(association)
        else:
            if not association or not association.is_active:
                return {"message": "Module already inactive for this project"}, 200
            association.is_active = False

        db.session.commit()
        return {"message": f"Module {'activated' if activate else 'deactivated'} successfully"}, 200

    @staticmethod
    def get_project_modules(project_id: int, only_active: bool = True) -> List[Dict]:
        """Récupère les modules d'un projet avec statut d'activation"""
        project = Project.query.get(project_id)
        if not project:
            return {"error": "Project not found"}, 404

        query = db.session.query(Module, ActiveModule.is_active).\
            join(ActiveModule, Module.id == ActiveModule.module_id).\
            filter(ActiveModule.project_id == project_id)

        if only_active:
            query = query.filter(ActiveModule.is_active == True)

        results = query.all()
        
        return [{
            **module.to_dict(),
            "is_active": is_active,
            "activated_at": association.activated_at.isoformat() if association else None
        } for module, is_active, association in results], 200

    @staticmethod
    def update_module(module_id: int, **kwargs) -> Dict:
        """Met à jour les informations d'un module"""
        module = Module.query.get(module_id)
        if not module:
            return {"error": "Module not found"}, 404

        updatable_fields = ['name', 'description']
        for field, value in kwargs.items():
            if field in updatable_fields and hasattr(module, field):
                setattr(module, field, value)

        module.updated_at = datetime.utcnow()
        db.session.commit()

        return {
            "message": "Module updated successfully",
            "module": module.to_dict()
        }, 200

    @staticmethod
    def get_module_analytics(module_id: int) -> Dict:
        """Récupère les statistiques d'utilisation d'un module"""
        active_projects_count = ActiveModule.query.filter_by(
            module_id=module_id,
            is_active=True
        ).count()

        total_projects_count = ActiveModule.query.filter_by(
            module_id=module_id
        ).count()

        return {
            "module_id": module_id,
            "active_projects": active_projects_count,
            "total_activations": total_projects_count,
            "adoption_rate": f"{(active_projects_count/max(1, total_projects_count)*100):.2f}%"
        }, 200