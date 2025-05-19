import pytest
from models.user import User
from models.project import Project
from models.module import Module, ActiveModule
from datetime import datetime

def test_user_model():
    """Test le modèle User"""
    user = User(email='test@kaizenflow.com')
    user.set_password('Test123!')
    
    assert user.email == 'test@kaizenflow.com'
    assert user.check_password('Test123!') is True
    assert user.check_password('Wrong') is False
    assert isinstance(user.created_at, datetime)

def test_project_model():
    """Test le modèle Project"""
    project = Project(name='Kaizen Project', description='Test project')
    
    assert project.name == 'Kaizen Project'
    assert project.description == 'Test project'
    assert project.created_at is not None

def test_module_activation():
    """Test la relation Project-Module"""
    user = User(email='admin@kaizenflow.com')
    project = Project(name='Test Project', owner=user)
    module = Module(name='Kanban', is_core=True)
    
    activation = ActiveModule(project=project, module=module)
    
    assert activation.is_active is True
    assert activation.project == project
    assert activation.module == module