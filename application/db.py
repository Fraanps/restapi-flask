from flask_mongoengine import MongoEngine

db = MongoEngine()


# configurações do banco
def init_db(app):
    db.init_app(app)
