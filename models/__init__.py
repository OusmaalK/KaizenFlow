from .user import User
from .project import Project
from .module import Module, ActiveModule
from .. import db

__all__ = ['User', 'Project', 'Module', 'ActiveModule']

# Initialisation des relations
def init_relationships():
    """Établit les relations entre modèles"""
    from .user import User
    from .project import Project
    from .module import Module
    
    # Relations User-Project
    User.projects = db.relationship('Project', backref='owner', lazy=True)
    
    # Relations Project-Module (many-to-many)
    Project.modules = db.relationship(
        'Module',
        secondary='active_modules',
        back_populates='projects'
    )
    
    Module.projects = db.relationship(
        'Project',
        secondary='active_modules',
        back_populates='modules'
    )