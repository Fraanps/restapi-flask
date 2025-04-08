from flask_mongoengine import MongoEngine
from mongoengine import connect, disconnect

db = MongoEngine()


# configurações do banco
def init_db(app, use_mock=False):

    if use_mock:
        import mongomock
        disconnect()
        connect(
            db=app.config['MONGODB_SETTINGS']['db'],
            mongo_client_class=mongomock.MongoClient,
            alias='default'
        )
    else:
        db.init_app(app)
