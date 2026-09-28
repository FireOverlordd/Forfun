class BaseConfig(object):
    DEBUG = False
    TESTING = False

class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    USE_RELOADER = False
    MONGODB_SETTINGS = {'db': 'uno_rangliste'}
    SECRET_KEY = 'flask+mongo=<3'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    WTF_CSRF_ENABLED = False