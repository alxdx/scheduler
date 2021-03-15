import os

class Config(object):
    DEBUG=False
    TESTING= False
    MONGODATABASE=os.environ.get("MONGODATABASE")
    MONGODB_HOST=MONGODATABASE
class Local(Config):
    MONGODB_HOST="mongodb://localhost/scheduler"
