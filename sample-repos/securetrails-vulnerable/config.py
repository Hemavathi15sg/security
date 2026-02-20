# VULNERABILITY: Secrets in production code
import os

class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'super-secret-key-12345'  # Hardcoded!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///securetrails.db'
    
class DevelopmentConfig(Config):
    DEBUG = True
    API_KEY = 'sk_test_12345'  # Hardcoded test key
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://user:password@localhost/securetrails'
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-unsafe-key')  # Unsafe default
