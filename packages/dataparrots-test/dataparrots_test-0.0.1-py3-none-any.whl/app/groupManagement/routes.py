from app.groupManagement.models import *
from app.groupManagement import bp
from app import db, siwa
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models import User, DBConnection
from app.common import Result, pageUtils
from sqlalchemy import or_
from datetime import datetime
from sqlalchemy.sql import text
from app.main.apirequest import request_post
from flask_login import current_user, login_required
from flask import Flask, request, current_app


class SearchVo(BaseModel):
    keyword: str = Field(default=None, title="关键词", description='关键词')


@bp.route('/userList', methods=['GET'])
@login_required
@siwa.doc(summary='用户下拉列表', tags=['groupManagement'], query=SearchVo)
def get_user_list(query: SearchVo):
    keyword = query.keyword
    users = User.query.filter(User.is_delete == 0, User.user_status == 1,
                              User.username.like(f'%{keyword}%') if keyword else True).all()
    roles = list(set(user.user_role for user in users if user.user_role != 'admin'))
    data_list = []
    for role in roles:
        role_users = [user for user in users if user.user_role == role]
        user_vos = []
        for role_user in role_users:
            user_vo = {
                'value': role_user.id,
                'label': role_user.username
            }
            user_vos.append(user_vo)
        data = {
            'value': role,
            'label': modify_role_string(role),
            'children': user_vos
        }
        data_list.append(data)
    return Result.success(data_list)


def modify_role_string(s):
    role_string = ''
    if s == 'admin':
        role_string = 'Admin'
    if s == 'professional':
        role_string = 'Pro User'
    if s == 'general':
        role_string = 'User'
    return role_string


class CreateGroupVo(BaseModel):
    id: Optional[int]
    group_name: Optional[str]
    conn_ids: Optional[List[int]]
    user_ids: Optional[List[int]]


@bp.route('/addOrEdit', methods=['POST'])
@login_required
@siwa.doc(body=CreateGroupVo, summary='新增/编辑分组', tags=['groupManagement'])
def add_edit_group(body: CreateGroupVo):
    try:
        groupId = body.id
        groupName = body.group_name
        conn_ids = body.conn_ids
        user_ids = body.user_ids
        now = datetime.now()
        if not groupId:
            # group
            if Group.query.filter(Group.is_delete == 0, Group.group_name == groupName).first():
                return Result.common(400, 'The group_name already exists.')
            group = Group(group_name=groupName, create_time=now, update_time=now)
            db.session.add(group)
            db.session.commit()
            groupId = group.id
        else:
            # group
            entity = Group.query.filter(Group.is_delete == 0, Group.id == groupId).first()
            if entity:
                entity.group_name = groupName
                entity.update_time = now
                db.session.commit()
            GroupConn.query.filter(GroupConn.group_id == groupId).delete()
            db.session.commit()
            GroupUser.query.filter(GroupUser.group_id == groupId).delete()
            db.session.commit()
        # group-conn
        if conn_ids is not None and len(conn_ids) > 0:
            for conn_id in conn_ids:
                group_conn = GroupConn(group_id=groupId, conn_id=conn_id)
                db.session.add(group_conn)
            db.session.commit()
        # group-user
        if user_ids is not None and len(user_ids) > 0:
            for user_id in user_ids:
                group_user = GroupUser(group_id=groupId, user_id=user_id)
                db.session.add(group_user)
            db.session.commit()
        # 同步分组到admin端
        api_url = "/api/save_group"
        data = {
            'group_id': groupId,
            'group_name': groupName,
            'conn_ids': conn_ids,
            'user_ids': user_ids
        }
        response = request_post(api_url, data)
        if response['status'] == 0:
            return Result.success()
        else:
            return Result.common(400, response['result'])
    except Exception as error:
        current_app.logger.error(f'Save group error! Error: {error}')
        return Result.common(500, str(error))


@bp.route('/delete/<int:groupId>', methods=['DELETE'])
@login_required
@siwa.doc(summary='删除分组', tags=['groupManagement'])
def delete_group(groupId):
    try:
        entity = Group.query.filter(Group.id == groupId, Group.is_delete == 0).first()
        GroupConn.query.filter(GroupConn.group_id == groupId).delete()
        db.session.commit()
        GroupUser.query.filter(GroupUser.group_id == groupId).delete()
        db.session.commit()
        entity.is_delete = 1
        entity.update_time = datetime.now()
        db.session.commit()
        # 同步到admin端
        api_url = "/api/delete_group"
        data = {
            'group_id': groupId
        }
        response = request_post(api_url, data)
        if response['status'] == 0:
            return Result.success()
        else:
            return Result.common(400, response['result'])
    except Exception as error:
        current_app.logger.error(f'Delete group error! Error: {error}')
        return Result.common(500, str(error))


@bp.route('/list', methods=['GET'])
@login_required
@siwa.doc(summary='分组列表', tags=['groupManagement'], query=SearchVo)
def get_group_list(query: SearchVo):
    keyword = query.keyword
    likeStr = 'a.group_name LIKE \'%{}%\''
    result = db.session.execute(text(f"SELECT a.id, a.group_name, "
                                     f"strftime('%Y/%m/%d %H:%M:%S', a.create_time) create_time, "
                                     f"strftime('%Y/%m/%d %H:%M:%S', a.update_time) update_time, "
                                     f"GROUP_CONCAT(DISTINCT b.conn_id) conn_ids, "
                                     f"GROUP_CONCAT(DISTINCT c.user_id) user_ids "
                                     f"FROM \"group\" a "
                                     f"LEFT JOIN group_conn b ON a.id = b.group_id "
                                     f"LEFT JOIN group_user c ON a.id = c.group_id "
                                     f"WHERE a.is_delete = 0 AND {likeStr.format(keyword) if keyword else 1} "
                                     f"GROUP BY a.id"))
    rows = result.fetchall()
    if rows:
        data_list = []
        for row in rows:
            conn_by_ids = get_conn_by_ids(row.conn_ids.split(",")) if row.conn_ids else []
            user_by_ids = get_user_by_ids(row.user_ids.split(",")) if row.user_ids else []
            data = {
                'group_id': row.id,
                'group_name': row.group_name,
                'amount': len(conn_by_ids),
                'assigned_users': len(user_by_ids),
                'database': conn_by_ids,
                'users': user_by_ids,
                'register_time': row.create_time,
                'last_modified': row.update_time
            }
            data_list.append(data)
        result_data = {
            'data': data_list,
            'total': len(rows)
        }
        return Result.success(result_data)
    return Result.success()


def get_conn_by_ids(ids):
    conn_list = (DBConnection.query.with_entities(DBConnection.id, DBConnection.name)
                 .filter(DBConnection.is_delete == 0, DBConnection.state == 1, DBConnection.id.in_(ids)).all())
    data_list = []
    for conn in conn_list:
        data = {
            'id': conn.id,
            'name': conn.name
        }
        data_list.append(data)
    return data_list


def get_user_by_ids(ids):
    user_list = (User.query.with_entities(User.id, User.username, User.user_role)
                 .filter(User.is_delete == 0, User.user_status == 1, User.id.in_(ids)).all())
    data_list = []
    for user in user_list:
        data = {
            'id': user.id,
            'username': user.username,
            'role_label': modify_role_string(user.user_role),
            'role_value': user.user_role
        }
        data_list.append(data)
    return data_list
