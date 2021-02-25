class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS={
        "host":"mongodb+srv://servidor_social:elhuesodeduraznomelapelax4@schedulerbackend.lhw5y.mongodb.net/scheduler?retryWrites=true&w=majority"
}	
    JWT_SECRET_KEY="elhuesodeduraznomelapelax3"

class ProductionConfig(Config):
    JWT_SECRET_KEY="enProduccion3lHuesoTambienmeL4p3l4"
    
class DevelopmentConfig(Config):
    ENV="development"
    DEBUG = True

class TestingConfig(Config):
    TESTING = True




