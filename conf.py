import os

SECRET_KEY = 'SECRET_KEY'

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
