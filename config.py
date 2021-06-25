import os 

class Config(object):
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII= False    
    MONGODATABASE=os.environ.get("MONGODATABASE")
    MONGODB_HOST=MONGODATABASE
    DEVELOPMENT_JWT_KEY=os.environ.get("DEVELOPMENT_JWT_KEY")
    JWT_SECRET_KEY=DEVELOPMENT_JWT_KEY

class ProductionConfig(Config):
    PRODUCTION_JWT_KEY = os.environ.get("PRODUCTION_JWT_KEY")
    JWT_SECRET_KEY = PRODUCTION_JWT_KEY
    PROPAGATE_EXCEPTIONS = True

class DevelopmentConfig(Config):
    ENV="development"
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEGUB = True
    MONGODB_HOST = "mongodb://localhost/scheduler"



