from app import create_app, db
from config import Config
from datetime import datetime
flask_app = create_app()

from app import db
from app.models import User

with flask_app.app_context():
    print("initial setup")
    
    try:
        user = User.query.filter_by(username='admin').first()
        if user == None:
            print('adding admin user')
            user = User(username='admin', email='admin@admin.com')
            user.set_password('admin')
            db.session.add(user)
            db.session.commit()    
    except Exception as error:
        print(f'Failed adding admin user: {error}')


#from app.app_log import app_log
#if not flask_app.debug and not flask_app.testing:
#    app_log.info("flaskwx is initialized")    
    
@flask_app.cli.command()
def init_db():
    db.drop_all()
    db.create_all()
    # 初始化admin用户
    user = User(username='admin', email=Config.ADMIN_EMAIL, user_role='admin', register_time=datetime.now())
    user.set_password('admin')
    db.session.add(user)
    db.session.commit()

