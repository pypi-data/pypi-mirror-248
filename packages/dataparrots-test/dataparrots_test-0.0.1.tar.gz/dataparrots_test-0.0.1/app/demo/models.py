from app import db


# 定义数据表模型-用户demo演示
class UserDemo(db.Model):
    __tablename__ = 'user_demo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(50))
    sex = db.Column(db.Integer)


