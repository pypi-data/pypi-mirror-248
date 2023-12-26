import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    LOG_DIR = os.environ.get('LOG_DIR')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_ROOT = os.environ.get('API_ROOT')
    LOCAL_DOMAIN = os.environ.get('LOCAL_DOMAIN')
    
    API_USER_NAME = os.environ.get('API_USER_NAME')
    API_PASSWORD = os.environ.get('API_PASSWORD')
    ACCESS_TOKENMAP_FILENAME = os.path.join(basedir, os.environ.get('ACCESS_TOKENMAP_FILENAME'))
    TIMELAP = int(os.environ.get('TIMELAP'))

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    
print("running module", __name__)    
for x in Config.__dict__:
    print(f'{x}={Config.__dict__[x]}')
    