class BaseConfig:
    DEBUG = False
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/edtech-dev-db"
    AlGORITHM = "HS256"
    SECRET_KEY = "705820c71516170c962a301c2952075cfd4358f25f24a037a63455054c510eaf"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    BASE_URL = "http://localhost:8000"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    
class ProductionConfig(BaseConfig):
    DEBUG = False


settings = BaseConfig()
prod_settings = ProductionConfig()
dev_settings = DevelopmentConfig()