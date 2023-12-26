from app.userManagement.models import ConnectionUser
from app.userManagement import bp
from app import db, siwa
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models import User, DBConnection
from app.common import Result, pageUtils
from sqlalchemy import or_
from datetime import datetime
from app.main.apirequest import request_post
from flask_login import current_user, login_required
from flask import Flask, request, current_app, jsonify
from app.groupManagement.models import *
from sqlalchemy.sql import text


class GetPageModel(BaseModel):
    page: int = Field(default=1, title="当前页", description='当前页')
    size: int = Field(default=10, title="每页数量", description='每页数量', ge=1, le=20)
    keyword: str = Field(default=None, title="关键词", description='关键词')
    role: Optional[List[str]]
    data_base: Optional[List[int]]
    state: Optional[List[int]]


@bp.route('/list', methods=['GET'])
@login_required
@siwa.doc(summary='查询用户列表', tags=['UserManagement'], query=GetPageModel)
def get_user_list(query: GetPageModel):
    try:
        page = query.page
        size = query.size
        keyword = query.keyword
        role = query.role
        data_base = query.data_base
        state = query.state
        if data_base is None or len(data_base) == 0:
            querySql = User.query.filter(User.is_delete == 0)
        else:
            rel_list = ConnectionUser.query.filter(ConnectionUser.conn_id.in_(data_base)).all()
            user_ids = [rel.user_id for rel in rel_list]
            querySql = User.query.filter(User.is_delete == 0, User.id.in_(user_ids))
        if keyword is not None and keyword != '':
            querySql = querySql.filter(or_(User.username.like(f'%{keyword}%'), User.email.like(f'%{keyword}%')))
        if role is not None and len(role) > 0:
            querySql = querySql.filter(User.user_role.in_(role))
        if state is not None and len(state) > 0:
            querySql = querySql.filter(User.user_status.in_(state))
        querySql = querySql.order_by(User.id.desc())
        dataList, totalElements, totalPages = pageUtils(querySql, page, size)
        data_list = []
        if len(dataList) > 0:
            for user in dataList:
                assigned_conns, total_conns = get_conn_by_userId(user.id)
                group_list = get_group_by_userId(user.id)
                entity = {
                    'id': str(user.id),
                    'register_time': format_time(str(user.register_time)),
                    'username': user.username,
                    'role': user.user_role,
                    'email': user.email,
                    'status': user.user_status,
                    'conn_list': total_conns,
                    'group_list': group_list,
                    'assigned_conns': assigned_conns
                }
                data_list.append(entity)
        return Result.successWithPage(data_list, totalPages, page, totalElements)
    except Exception as error:
        current_app.logger.error(f'Internal error! Error: {error}')
        return Result.common(500, str(error))


class SaveOrUpdateUserVo(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: Optional[str]
    repeat_password: Optional[str]
    role: str
    conn_ids: Optional[List[int]]
    group_ids: Optional[List[int]]


@bp.route('/addOrEdit', methods=['POST'])
@login_required
@siwa.doc(body=SaveOrUpdateUserVo, summary='新增/编辑用户', tags=['UserManagement'])
def add_edit_user(body: SaveOrUpdateUserVo):
    userId = body.id
    username = body.username
    email = body.email
    try:
        now = datetime.now()
        registerTime = now
        if userId is None:
            if User.query.filter(User.username == username, User.is_delete == 0).first():
                return Result.common(400, "The username already exists!")
            if User.query.filter(User.email == email, User.is_delete == 0).first():
                return Result.common(400, "The email already exists!")
            new_user = User()
            new_user.username = username
            new_user.email = email
            new_user.set_password(body.password)
            new_user.user_role = body.role
            new_user.register_time = now
            new_user.update_time = now
            db.session.add(new_user)
            db.session.commit()
            userId = new_user.id
        else:
            user = User.query.get(userId)
            if user is not None:
                if User.query.filter(User.id != userId, User.username == username, User.is_delete == 0).first():
                    return Result.common(400, "The username already exists!")
                if User.query.filter(User.id != userId, User.email == email, User.is_delete == 0).first():
                    return Result.common(400, "The email already exists!")
                registerTime = user.register_time
                if body.password is not None and body.password != '':
                    user.set_password(body.password)
                user.username = username
                user.email = email
                user.user_role = body.role
                user.update_time = now
                db.session.commit()
            else:
                return Result.common(400, "User not found!")
            ConnectionUser.query.filter(ConnectionUser.user_id == userId).delete()
            GroupUser.query.filter(GroupUser.user_id == userId).delete()
            db.session.commit()
        # user-conn
        conn_id_array = body.conn_ids
        if conn_id_array is not None and len(conn_id_array) > 0:
            for item in conn_id_array:
                connection_user = ConnectionUser(user_id=userId, conn_id=item)
                db.session.add(connection_user)
            db.session.commit()
        # user-group
        group_ids = body.group_ids
        if group_ids is not None and len(group_ids) > 0:
            for group_id in group_ids:
                group_user = GroupUser(group_id=group_id, user_id=userId)
                db.session.add(group_user)
            db.session.commit()
        # 用户同步到admin端
        api_url = "/api/create_user"
        data = {
            'user_id': userId,
            'username': username,
            'email': email,
            'role': body.role,
            'register_time': str(registerTime),
            'update_time': str(now),
            'conn_ids': conn_id_array,
            'group_ids': group_ids
        }
        response = request_post(api_url, data)
        if response['status'] == 0:
            return Result.success()
        else:
            return Result.common(400, response['result'])
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f'Save user error! Error: {error}')
        return Result.common(500, str(error))


@bp.route('/updateStatus/<int:user_id>/<int:status>', methods=['PUT'])
@login_required
@siwa.doc(summary='更改用户状态，1：active/0：inactive', tags=['UserManagement'])
def update_status(user_id, status):
    try:
        user = User.query.get(user_id)
        if user is None:
            return Result.common(400, "User not found!")
        if user.username == 'admin':
            return Result.common(400, "Built-in administrator users are forbidden to edit!")
        user.user_status = status
        user.update_time = datetime.now()
        db.session.commit()
        # 用户状态同步到admin端
        api_url = "/api/disable_user"
        data = {
            'user_id': user_id,
            'disabled': 1 if status == 0 else 0
        }
        response = request_post(api_url, data)
        if response['status'] == 0:
            return Result.success()
        else:
            return Result.common(400, response['result'])
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f'Save error! Error: {error}')
        return Result.common(500, str(error))


@bp.route('/delete/<int:userId>', methods=['DELETE'])
@login_required
@siwa.doc(summary='删除用户', tags=['UserManagement'])
def delete(userId):
    try:
        user = User.query.get(userId)
        if user is None:
            return Result.common(400, "User not found!")
        if user.username == 'admin':
            return Result.common(400, "Built-in administrator users are forbidden to delete!")
        user.is_delete = 1
        db.session.commit()
        # 删除关联表
        ConnectionUser.query.filter(ConnectionUser.user_id == userId).delete()
        db.session.commit()
        # 在admin端删除用户
        api_url = '/api/delete_user'
        data = {
            'user_id': userId
        }
        response = request_post(api_url, data)
        if response['status'] == 0:
            return Result.success()
        else:
            return Result.common(400, response['result'])
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f'Internal error! Error: {error}')
        return Result.common(500, str(error))


@bp.route('/getConnList', methods=['GET'])
@login_required
@siwa.doc(summary='获取数据库列表', tags=['UserManagement'])
def get_conn_list():
    try:
        conn_list = DBConnection.query.with_entities(DBConnection.id, DBConnection.name).filter(
            DBConnection.state == 1, DBConnection.is_delete == 0)
        conn_list_json = []
        for conn in conn_list:
            entity = {
                'id': conn.id,
                'name': conn.name
            }
            conn_list_json.append(entity)
        return Result.success(conn_list_json)
    except Exception as error:
        current_app.logger.error(f'Internal error! Error: {error}')
        return Result.common(500, str(error))


@bp.route('/getGroupList', methods=['GET'])
@login_required
@siwa.doc(summary='获取分组列表', tags=['UserManagement'])
def get_group_list():
    try:
        group_list = Group.query.with_entities(Group.id, Group.group_name).filter(Group.is_delete == 0)
        group_list_json = []
        for group in group_list:
            entity = {
                'id': group.id,
                'name': group.group_name
            }
            group_list_json.append(entity)
        return Result.success(group_list_json)
    except Exception as error:
        current_app.logger.error(f'Internal error! Error: {error}')
        return Result.common(500, str(error))


class ChangePasswordVo(BaseModel):
    old_password: str
    new_password: str


@bp.route('/changePassword', methods=['POST'])
@login_required
@siwa.doc(body=ChangePasswordVo, summary='用户修改密码', tags=['UserManagement'])
def change_password(body: ChangePasswordVo):
    try:
        user = User.query.get(current_user.id)
        if not user.check_password(body.old_password):
            return Result.common(400, "Incorrect old_password!")
        if body.new_password == body.old_password:
            return Result.common(400, "The new password is the same as the old one!")
        user.set_password(body.new_password)
        user.update_time = datetime.now()
        db.session.commit()
        return Result.success()
    except Exception as error:
        current_app.logger.error(f'Internal error! Error: {error}')
        return Result.common(500, str(error))


@bp.route('/mightLikeOrNot/<int:onOff>', methods=['PUT'])
@login_required
@siwa.doc(summary='用户开/关喜好推荐按钮，1：开启，0：关闭', tags=['UserManagement'])
def might_like_or_not(onOff):
    try:
        user = User.query.get(current_user.id)
        user.might_like = onOff
        user.update_time = datetime.now()
        db.session.commit()
        # 用户喜好设置同步到admin端
        api_url = "/api/set_might_like"
        data = {
            'user_id': current_user.id,
            'might_like': onOff
        }
        response = request_post(api_url, data)
        if response['status'] == 0:
            return Result.success()
        else:
            return Result.common(400, response['result'])
    except Exception as error:
        current_app.logger.error(f'Internal error! Error: {error}')
        return Result.common(500, str(error))


@bp.route('/getUserInfo', methods=['GET'])
@login_required
@siwa.doc(summary='获取登录用户的信息', tags=['UserManagement'])
def get_user_info():
    try:
        user_info = {
            'username': current_user.username,
            'email': current_user.email,
            'user_role': current_user.user_role,
            'might_like': current_user.might_like
        }
        return Result.success(user_info)
    except Exception as error:
        current_app.logger.error(f'Internal error! Error: {error}')
        return Result.common(500, str(error))


def format_time(time_str):
    try:
        if time_str is None or time_str == '':
            return None
        time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
        formatted_time = time_obj.strftime("%Y/%m/%d %H:%M")
        return formatted_time
    except Exception as error:
        current_app.logger.error(f'The time string format conversion is abnormal! Error: {error}')
        return None


def get_conn_by_userId(userId):
    # 分配的数据库
    rel_list = ConnectionUser.query.filter(ConnectionUser.user_id == userId).all()
    conn_ids = [rel.conn_id for rel in rel_list]
    conn_list = (DBConnection.query.with_entities(DBConnection.id, DBConnection.name)
                 .filter(DBConnection.id.in_(conn_ids), DBConnection.state == 1,
                         DBConnection.is_delete == 0).all())
    assigned_conns = [
        {
            "id": conn.id,
            "name": conn.name
        } for conn in conn_list
    ]
    # 用户所在group的数据库
    result = db.session.execute(text(f"SELECT DISTINCT a.id, a.name FROM db_connection a "
                                     f"LEFT JOIN group_conn b ON a.id = b.conn_id "
                                     f"LEFT JOIN group_user c ON b.group_id = c.group_id "
                                     f"WHERE c.user_id = {userId} AND a.state = 1 AND a.is_delete = 0"))
    rows = result.fetchall()
    # merge
    unique_set = set(conn_list)
    unique_set.update(rows)
    all_conn_list = list(unique_set)
    total_conns = [
        {
            "id": conn.id,
            "name": conn.name
        } for conn in all_conn_list
    ]
    return assigned_conns, total_conns


def get_group_by_userId(userId):
    rel_list = GroupUser.query.filter(GroupUser.user_id == userId).all()
    group_ids = [rel.group_id for rel in rel_list]
    group_list = (Group.query.with_entities(Group.id, Group.group_name)
                  .filter(Group.id.in_(group_ids), Group.is_delete == 0).all())
    group_list_json = [
        {
            "id": group.id,
            "name": group.group_name
        } for group in group_list
    ]
    return group_list_json
