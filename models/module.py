from app import db
from datetime import datetime

class Module(db.Model):
    """Modèle représentant un module fonctionnel de KaizenFlow™"""
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_core = db.Column(db.Boolean, default=False)  # Module système ou personnalisé
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relation many-to-many avec les projets (via table d'association)
    projects = db.relationship(
        'Project',
        secondary='active_modules',
        back_populates='modules'
    )

    def __repr__(self):
        return f'<Module {self.name}>'

    def to_dict(self):
        """Sérialise l'objet en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_core': self.is_core,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    active_project_associations = db.relationship(
        'ActiveModule', 
        back_populates='module'
    )


class ActiveModule(db.Model):
    """Table d'association pour les modules activés par projet"""
    __tablename__ = 'active_modules'

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    activated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations explicites (optionnel mais recommandé)
    project = db.relationship('Project', back_populates='active_module_associations')
    module = db.relationship('Module', back_populates='active_project_associations')

    def __repr__(self):
        return f'<ActiveModule P{self.project_id}-M{self.module_id}>'