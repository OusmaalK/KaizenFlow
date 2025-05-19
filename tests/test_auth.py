import pytest
from app import create_app
from models.user import User
from config.database import db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_user_registration(client):
    """Test l'enregistrement d'un nouvel utilisateur"""
    response = client.post('/auth/register', json={
        'email': 'test@kaizenflow.com',
        'password': 'Secure123!'
    })
    assert response.status_code == 201
    assert 'user_id' in response.json

def test_duplicate_registration(client):
    """Test la prévention des doublons"""
    client.post('/auth/register', json={
        'email': 'test@kaizenflow.com', 
        'password': 'Secure123!'
    })
    response = client.post('/auth/register', json={
        'email': 'test@kaizenflow.com',
        'password': 'AnotherPass123!'
    })
    assert response.status_code == 400
    assert 'already exists' in response.json['error']

def test_valid_login(client, test_user):
    """Test la connexion valide"""
    response = client.post('/auth/login', json={
        'email': test_user.email,
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_invalid_login(client, test_user):
    """Test la connexion invalide"""
    response = client.post('/auth/login', json={
        'email': test_user.email,
        'password': 'wrongpassword'
    })
    assert response.status_code == 401