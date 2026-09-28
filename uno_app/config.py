class BaseConfig(object):
    DEBUG = False
    TESTING = False

class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    USE_RELOADER = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    WTF_CSRF_ENABLED = False