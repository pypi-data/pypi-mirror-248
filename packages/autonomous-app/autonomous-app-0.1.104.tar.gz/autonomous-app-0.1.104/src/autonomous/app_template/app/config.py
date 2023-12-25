import os


#################################################################
#                         CONFIGURATION                         #
#################################################################
class Config:
    APP_NAME = os.environ.get("APP_NAME", __name__)
    HOST = os.environ.get("APP_HOST", "0.0.0.0")
    PORT = os.environ.get("APP_PORT", 5000)
    SECRET_KEY = os.environ.get("SECRET_KEY", "NATASHA")
    DEBUG = os.environ.get("DEBUG", False)
    TESTING = os.environ.get("TESTING", False)
    TRAP_HTTP_EXCEPTIONS = os.environ.get("TRAP_HTTP_EXCEPTIONS", False)


class APIConfig(Config):
    APP_NAME = os.environ.get("APP_NAME", __name__) + "API"
    RQ_DASHBOARD_REDIS_URL = f"redis://{os.environ.get('REDIS_HOST', 'redis')}:{os.environ.get('REDIS_PORT', '6379')}"
