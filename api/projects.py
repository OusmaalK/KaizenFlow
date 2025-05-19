from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.project_service import ProjectService
from schemas import ProjectCreateSchema, ProjectUpdateSchema

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """Création d'un nouveau projet"""
    user_id = get_jwt_identity()
    data = ProjectCreateSchema().load(request.get_json())
    return ProjectService.create_project(user_id=user_id, **data)

@projects_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    """Liste les projets de l'utilisateur"""
    user_id = get_jwt_identity()
    return ProjectService.get_user_projects(user_id)

@projects_bp.route('/<int:project_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def project_operations(project_id):
    """Opérations CRUD sur un projet spécifique"""
    user_id = get_jwt_identity()
    
    if request.method == 'GET':
        return ProjectService.get_project_details(project_id, user_id)
    elif request.method == 'PUT':
        data = ProjectUpdateSchema().load(request.get_json())
        return ProjectService.update_project(project_id, user_id, **data)
    elif request.method == 'DELETE':
        return ProjectService.delete_project(project_id, user_id)