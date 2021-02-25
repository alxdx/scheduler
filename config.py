import os 

class Config(object):
    DEBUG = False
    TESTING = False
    
    MONGODATABASE=os.environ.get("MONGODATABASE")
    MONGODB_SETTINGS={
        "host":MONGODATABASE
    }
    DEVELOPMENT_JWT_KEY=os.environ.get("DEVELOPMENT_JWT_KEY")
    JWT_SECRET_KEY=DEVELOPMENT_JWT_KEY

class ProductionConfig(Config):
    PRODUCTION_JWT_KEY=os.environ.get("PRODUCTION_JWT_KEY")
    JWT_SECRET_KEY=PRODUCTION_JWT_KEY
    
class DevelopmentConfig(Config):
    ENV="development"
    DEBUG = True

class TestingConfig(Config):
    TESTING = True




