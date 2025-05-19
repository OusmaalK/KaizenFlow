from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.module_service import ModuleService
from schemas import ModuleCreateSchema

modules_bp = Blueprint('modules', __name__, url_prefix='/modules')

@modules_bp.route('', methods=['POST'])
@jwt_required()
def create_module():
    """Création d'un nouveau module (Admin uniquement)"""
    data = ModuleCreateSchema().load(request.get_json())
    return ModuleService.create_module(**data)

@modules_bp.route('', methods=['GET'])
def get_modules():
    """Liste tous les modules disponibles"""
    return ModuleService.get_all_modules()

@modules_bp.route('/<int:module_id>/projects/<int:project_id>', methods=['PATCH'])
@jwt_required()
def toggle_module(module_id, project_id):
    """Active/désactive un module pour un projet spécifique"""
    data = request.get_json()
    return ModuleService.toggle_module_for_project(
        project_id=project_id,
        module_id=module_id,
        activate=data.get('activate', True)
    )