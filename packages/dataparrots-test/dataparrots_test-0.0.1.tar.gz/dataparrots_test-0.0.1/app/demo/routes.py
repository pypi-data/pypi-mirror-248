from app.demo import bp
from app.demo.models import UserDemo as User
from flask import request
from app.common import Result, pageUtils
from app import db, siwa
from pydantic import BaseModel, Field
from flask_login import current_user, login_required


# 查询所有，不分页
@bp.route('/', methods=['GET'])
@siwa.doc(summary='查询所有', tags=['demo'])
@login_required
def getAll():
    print('---id----' + str(current_user.id))
    print('---username----'+current_user.username)
    print('---email----' + current_user.email)
    print('---password_hash----' + current_user.password_hash)
    users = User.query.all()
    if len(users) > 0:
        data = [
            {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "age": str(user.age),
                "password": user.password
            } for user in users
        ]
        return Result.success(data)
    return Result.success(users)


class PageQueryModel(BaseModel):
    page: int = Field(default=1, title="当前页", description='当前页')
    size: int = Field(default=10, title="每页数量", description='每页数量', ge=1, le=20)
    username: str = Field(title="用户名", description='用户名')


# 分页查询
@bp.route('/list', methods=['GET'])
@siwa.doc(summary='分页查询列表', tags=['demo'], query=PageQueryModel)
def listByPage(query: PageQueryModel):
    # 获取get请求URL拼接参数
    page = query.page
    size = query.size
    keyword = query.username
    # 构造查询
    if keyword:
        querySql = User.query.filter(User.name.like(f'%{keyword}%'))
    else:
        querySql = User.query
    dataList, totalElements, totalPages = pageUtils(querySql, page, size)
    if len(dataList) > 0:
        dataList = [
            {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "age": str(user.age),
                "password": user.password
            } for user in dataList
        ]
    return Result.successWithPage(dataList, totalPages, page, totalElements)


# 根据用户名查询用户信息
@bp.route('/username/<string:username>', methods=['GET'])
@siwa.doc(summary='根据用户名查询用户信息', tags=['demo'])
def getByUsername(username):
    # user = User.query.filter_by(name=username).first()
    users = User.query.filter(User.name.like(f'%{username}%')).all()  # 模糊查询
    if len(users) > 0:
        data = [
            {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "age": str(user.age),
                "password": user.password
            } for user in users
        ]
        return Result.success(data)
    return Result.success()


# 根据主键查询用户信息
@bp.route('/<int:userId>', methods=['GET'])
@siwa.doc(summary='根据主键查询用户信息', tags=['demo'])
def getById(userId):
    user = User.query.get(userId)
    if user:
        data = {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "age": str(user.age),
            "password": user.password
        }
        return Result.success(data)
    return Result.common(400, 'user not exist!')


class SaveUserVo(BaseModel):
    name: str = Field(description='姓名')
    email: str
    age: int
    password: str


# 新增用户
@bp.route('/', methods=['POST'])
@siwa.doc(summary='新增用户', tags=['demo'], form=SaveUserVo)
def post(form: SaveUserVo):
    # 获取FORM表单参数
    print(form.name)
    data = request.form
    user = User()
    user.name = data.get('name')
    user.email = data.get('email')
    user.age = data.get('age')
    user.password = data.get('password')
    db.session.add(user)
    db.session.commit()
    return Result.success()


class UpdateUserVo(BaseModel):
    id: int
    name: str = Field(description='姓名')
    email: str
    age: int
    password: str


# 更新用户
@bp.route('/', methods=['PUT'])
@siwa.doc(summary='更新用户', tags=['demo'], body=UpdateUserVo)
def put(body: UpdateUserVo):
    print(body.name)
    # 获取请求体JSON参数
    data = request.json
    user: User = User.query.get(data.get('id'))
    user.name = data.get('name')
    user.email = data.get('email')
    user.age = data.get('age')
    user.password = data.get('password')
    db.session.commit()
    return Result.success()


# 删除操作
@bp.route('/<int:userId>', methods=['DELETE'])
@siwa.doc(summary='删除用户', tags=['demo'])  # 接口文档最基础写法
def delete(userId):
    user: User = User.query.get(userId)
    db.session.delete(user)
    db.session.commit()
    return Result.success()
