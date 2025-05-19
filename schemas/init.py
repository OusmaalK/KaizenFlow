from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class ProjectCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=3))
    description = fields.String()

class ModuleCreateSchema(Schema):
    name = fields.String(required=True)
    description = fields.String()
    is_core = fields.Boolean(default=False)