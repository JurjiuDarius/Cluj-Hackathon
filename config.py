import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
    MIGRATIONS_DIR = os.environ["MIGRATIONS_DIR"]
    BASIC_AUTH_REALM = ""
    BASIC_AUTH_FORCE = True


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
