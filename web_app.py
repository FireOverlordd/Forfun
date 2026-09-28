import os

from uno_app.factory import create_app

env = os.environ.get('FLASK_ENV', 'dev')

app = create_app('uno_app.config.%sConfig' % env.capitalize())

app.run()