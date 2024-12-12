from .db import db


# inicialização do banco
class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.EmailField(required=True)
    birth_date = db.DateTimeField(required=True)
