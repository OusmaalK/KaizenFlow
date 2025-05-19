import pytest
from app import create_app
from models.user import User
from models.project import Project
from config.database import db

@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(email='test@kaizenflow.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        return user

def test_project_creation(client, test_user):
    """Test la création de projet"""
    login_resp = client.post('/auth/login', json={
        'email': 'test@kaizenflow.com',
        'password': 'testpassword'
    })
    token = login_resp.json['access_token']
    
    response = client.post('/projects', 
        json={'name': 'New Project'},
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 201
    assert 'project_id' in response.json

def test_project_access_control(client, test_user):
    """Test les permissions des projets"""
    # Création d'un projet par l'utilisateur
    login_resp = client.post('/auth/login', json={
        'email': 'test@kaizenflow.com',
        'password': 'testpassword'
    })
    token = login_resp.json['access_token']
    
    create_resp = client.post('/projects', 
        json={'name': 'Private Project'},
        headers={'Authorization': f'Bearer {token}'}
    )
    project_id = create_resp.json['project_id']
    
    # Tentative d'accès non autorisé
    response = client.get(f'/projects/{project_id}')
    assert response.status_code == 401  # Non authentifié