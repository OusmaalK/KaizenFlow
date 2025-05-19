from app import db

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    modules = db.relationship(
        'Module',
        secondary='active_modules',
        back_populates='projects'
    )
    
    active_module_associations = db.relationship(
        'ActiveModule', 
        back_populates='project'
    )

