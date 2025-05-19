import pytest
from app import create_app
from config.database import db
from models.user import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(email='test@kaizenflow.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        return user