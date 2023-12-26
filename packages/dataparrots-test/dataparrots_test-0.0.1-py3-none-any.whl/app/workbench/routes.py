from app.workbench import bp
from flask import request, current_app
from app import db, siwa
from pydantic import BaseModel, Field
from app.models import DBConnection, User
from app.workbench.models import SavedQuery, FavoriteQuery, OpenAiUsage, RelatedQuestions
from app.common import Result
import sqlite3
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from app.main.dbexec import get_db_schema_imp, exec_db_query_imp, exec_db_query_json_imp, get_db_size_imp, \
    exec_db_query_json_imp_new
import re
from config import Config
from app.access_token import AccessToken
import requests
import json
import datetime
import yaml
from io import BytesIO
import xlsxwriter
from flask import make_response
import math
import uuid
from app.main.apirequest import request_post
from app.main.saved_queries import create_saved_query, create_favorite_query, update_saved_query, delete_saved_query


@bp.route('/connections', methods=['GET'])
@login_required
@siwa.doc(summary='获取用户可以查询的所有的数据库连接', tags=['workbench'])
def get_connections():
    username = current_user.username
    role = current_user.user_role
    # username = 'admin'
    connections = []
    if 'admin' == role:
        all_conn = db.session.execute(text(
            f'SELECT * FROM db_connection where is_delete = 0 AND state = 1'))
    else:
        con = db.session.execute(text(
            f"SELECT a.* FROM db_connection a JOIN connection_user b ON a.id = b.conn_id JOIN user c ON c.id = b.user_id  WHERE c.username = '{username}' AND a.is_delete = 0 AND a.state = 1 GROUP BY a.id")).fetchall()
        # 用户所在group的数据库
        result = db.session.execute(text(f"SELECT DISTINCT a.* FROM db_connection a "
                                         f"LEFT JOIN group_conn b ON a.id = b.conn_id "
                                         f"LEFT JOIN group_user c ON b.group_id = c.group_id "
                                         f"WHERE c.user_id = {current_user.id} AND a.state = 1 AND a.is_delete = 0"))
        rows = result.fetchall()
        unique_set = set(con)
        unique_set.update(rows)
        all_conn = list(unique_set)
    for row in all_conn:
        connection = {
            'id': row[0],
            'name': row[1],
            'db_type': row[2],
            'db_name': row[3],
            'username': row[4],
            'password': row[5],
            'ip_address': row[6],
            'port_number': row[7],
            'ds_name': row[8],
            'db_summary': row[9],
            'database_file': row[10],
            'state': row[11],
            'is_delete': row[12]
        }
        connections.append(connection)
    return {"status": 0, "result": connections}


class ConnectionIdModel(BaseModel):
    id: int = Field(None)
    db_name: str = Field(description='数据库名')
    db_type: str = Field(description='数据库类型')
    ds_name: str
    ip_address: str = Field(description='数据库连接地址')
    username: str = Field(description='用户名')
    password: str = Field(description='密码')
    port_number: str = Field(description='端口')
    database_file: str = Field(description='添加sqlite时的文件地址', default='')


@bp.route('/get_db_msg', methods=['POST'])
@login_required
@siwa.doc(summary='获取数据库详情(表,字段信息,简介)', tags=['workbench'], body=ConnectionIdModel)
def get_db_msg(body: ConnectionIdModel):
    try:

        conn_id = body.id
        if conn_id is not None:
            conn = DBConnection.query.filter_by(is_delete=0, state=1, id=conn_id).first()
            if conn is None:
                return Result.common(400, 'Database unavailable!')

        result = get_db_schema_imp(request)

        table = result['db_schema_human']
        human = yaml.load(table, yaml.SafeLoader)
        treeList = []
        for item in human:
            columnList = item['columns']
            newColumnList = []
            tree = {
                'title': item['table'],
            }
            for column in columnList:
                leaf = {
                    'title': column
                }
                newColumnList.append(leaf)
            tree['children'] = newColumnList
            treeList.append(tree)
        result['db_schema_human'] = treeList
        result['schema_size'] = len(result['db_schema'])
        db_schema = result['db_schema']
        if len(db_schema) == 0:
            return Result.common(500, 'The connection information is incorrect')
        return Result.success(result)
    except Exception as error:
        current_app.logger.error(error)
        return Result.common(500, 'The connection information is incorrect')


@bp.route('/get_db_msg_when_add', methods=['POST'])
@login_required
@siwa.doc(summary='添加注册数据库连接时获取数据库详情(表,字段信息,简介)', tags=['workbench'], body=ConnectionIdModel)
def get_db_msg_when_add(body: ConnectionIdModel):
    try:
        result = get_db_schema_imp(request)
        # conn_id = body.id
        # if conn_id is not None:
        #     conn = DBConnection.query.filter_by(id=conn_id).first()
        #     db_summary = conn.db_summary
        #     if db_summary is not None and len(db_summary) != 0 and db_summary != '' and db_summary != ' ':
        #         result['db_summary'] = db_summary
        #     else:
        #         database_schema = result['db_schema']
        #         data = {'database_schema': database_schema}
        #         api_url = Config.API_ROOT + "/get_db_summary"
        #         token = AccessToken().get_access_token()
        #         headers = {'Authorization': "Bearer {}".format(token)}
        #         response = requests.post(api_url, json=data, headers=headers)
        #         summary = response.json()['result']
        #         result['db_summary'] = summary
        #         conn.db_summary = summary
        #         db.session.commit()
        # else:
        #     database_schema = result['db_schema']
        #     data = {'database_schema': database_schema}
        #     api_url = Config.API_ROOT + "/get_db_summary"
        #     token = AccessToken().get_access_token()
        #     headers = {'Authorization': "Bearer {}".format(token)}
        #     response = requests.post(api_url, json=data, headers=headers)
        #     result['db_summary'] = response.json()['result']

        result['schema_size'] = len(result['db_schema'])
        # result.pop('db_schema')
        return Result.success(result)
    except Exception as error:
        current_app.logger.error(error)
        return Result.common(500, 'The connection information is incorrect')


class GetSqlModel(BaseModel):
    database_schema: str = Field(description='数据库模型结构')
    db_type: str = Field(description='数据库类型')
    user_question: str
    conn_id: int = Field(description='数据库连接id')


@bp.route('/get_sql', methods=['POST'])
@login_required
@siwa.doc(summary='获取sql语句', tags=['workbench'], body=GetSqlModel)
def get_sql(body: GetSqlModel):
    data = request.get_json()
    data['portal_username'] = Config.API_USER_NAME
    data['user_id'] = current_user.id
    database_schema = body.database_schema
    user_question = body.user_question

    # 保存Sql的记录

    user_id = current_user.id

    oldSaveQuery = SavedQuery.query.filter_by(user_id=user_id, conn_id=body.conn_id,
                                              question_text=body.user_question).filter(
        SavedQuery.my_query_text.isnot(None)).order_by(
        SavedQuery.create_time.desc()).first()
    nowDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    savedQuery = SavedQuery()
    if oldSaveQuery is not None:
        savedQuery.my_query_text = oldSaveQuery.my_query_text
    savedQuery.conn_id = body.conn_id
    savedQuery.question_text = user_question
    savedQuery.user_id = user_id
    savedQuery.create_time = nowDateTime
    savedQuery.update_time = nowDateTime
    savedQuery.is_delete = 0
    db.session.add(savedQuery)
    db.session.flush()
    newId = savedQuery.id
    data['saved_query_id'] = newId
    db.session.commit()

    try:
        api_url = Config.API_ROOT + "/get_all_query_commendation"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        response = requests.post(api_url, json=data, headers=headers)
        result = response.json()
        status = result['status']
        if status == 0:
            sqlJson = result['result']['candidates']
            savedQuery.query_text = str(sqlJson)
            savedQuery.update_time = nowDateTime
            db.session.commit()
            firstSql = sqlJson[0]['query']
            if 'SELECT' in firstSql.upper():

                # 保存query
                response_json = create_saved_query(newId=newId, user_id=user_id, conn_id=body.conn_id,
                                                   question_text=user_question,
                                                   query_text=str(sqlJson), my_query_text=None)
                if response_json['status'] == 0:
                    current_app.logger.info('Query is saved!')
                else:
                    current_app.logger.error(f'{response_json}')
                # try:
                #     # 保存usage记录
                #     usageJson = result['result']['usage']
                #     from app.main.db_connections import create_usage
                #     create_usage(Config.API_USER_NAME, body.conn_id, user_id, user_question, 1,
                #                  usageJson['total_tokens'],
                #                  usageJson['prompt_tokens'], usageJson['completion_tokens'])
                # except Exception as err:
                #     error_string = f"{err}"
                #     current_app.logger.error('Create usage exception: ' + error_string)

                sqlJson.sort(key=lambda x: x['score'], reverse=True)
                resultMap = {
                    'sql': sqlJson,
                    'saved_query_id': newId
                }
                return Result.success(resultMap)
            else:
                sqlJson.sort(key=lambda x: x['score'], reverse=True)
                resultMap = {
                    'sql': sqlJson,
                    'saved_query_id': newId
                }
                return Result.success(resultMap)
        else:
            return Result.common(400, result['result'])
    except Exception as error:
        current_app.logger.error(error)
        return Result.common(500, f'{"error", error}')


class GetExecuteSqlModel(BaseModel):
    database_schema: str = Field(description='数据库模型结构')
    db_type: str = Field(description='数据库类型')
    user_question: str
    conn_id: int = Field(description='数据库连接id')
    database_file: str = Field(description='添加sqlite时的文件地址', default='')


@bp.route('/get_execute_sql', methods=['POST'])
@login_required
@siwa.doc(summary='获取并执行sql语句', tags=['workbench'], body=GetExecuteSqlModel)
def get_execute_sql(body: GetExecuteSqlModel):
    data = request.get_json()
    data['portal_username'] = Config.API_USER_NAME
    data['user_id'] = current_user.id
    database_schema = body.database_schema
    user_question = body.user_question

    # 保存Sql的记录
    user_id = current_user.id
    nowDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    savedQuery = SavedQuery()
    savedQuery.conn_id = body.conn_id
    savedQuery.question_text = user_question
    savedQuery.user_id = user_id
    savedQuery.create_time = nowDateTime
    savedQuery.update_time = nowDateTime
    savedQuery.is_delete = 0
    db.session.add(savedQuery)
    db.session.flush()
    newId = savedQuery.id
    data['saved_query_id'] = newId
    db.session.commit()

    try:
        api_url = Config.API_ROOT + "/get_all_query_commendation"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        response = requests.post(api_url, json=data, headers=headers)
        result = response.json()
        status = result['status']
        if status == 0:
            sqlJson = result['result']['candidates']
            savedQuery.query_text = str(sqlJson)
            savedQuery.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()

            # 保存query
            response_json = create_saved_query(newId=newId, user_id=user_id, conn_id=body.conn_id,
                                               question_text=user_question,
                                               query_text=sqlJson, my_query_text=None)
            if response_json['status'] == 0:
                current_app.logger.info('Query is saved!')

            query_sql = str(sqlJson[0]['query'])
            if len(query_sql) == 0:
                return Result.common(400, 'Query is empty.')
            connectionId = body.conn_id
            conn = DBConnection.query.filter_by(id=connectionId).first()
            requestData = {
                'query_text': query_sql,
                'db_type': conn.db_type,
                'username': conn.username,
                'password': conn.password,
                'ip_address': conn.ip_address,
                'ds_name': conn.ds_name,
                'db_name': conn.db_name,
                'port_number': conn.port_number,
                'database_file': conn.database_file
            }
            result = exec_db_query_json_imp_new(requestData, True)
            resultList = [json.loads(item) for item in result]
            # return Result.success(resultList)
            resultData = {'result': resultList, 'query_text': sqlJson, 'saved_query_id': newId}
            return Result.success(resultData)
        else:
            return Result.common(400, result['result'])
    except Exception as error:
        current_app.logger.error(error)
        return Result.common(500, f'{"error", error}')


class ExecuteSqlModel(BaseModel):
    db_name: str = Field(description='数据库名')
    db_type: str = Field(description='数据库类型')
    ds_name: str
    ip_address: str = Field(description='数据库连接地址')
    username: str = Field(description='用户名')
    password: str = Field(description='密码')
    port_number: str = Field(description='端口')
    query_text: str = Field(description='sql语句')
    database_file: str = Field(description='添加sqlite时的文件地址', default='')


@bp.route('/execute_sql', methods=['POST'])
@login_required
@siwa.doc(summary='执行sql语句获取结果', tags=['workbench'], body=ExecuteSqlModel)
def execute_sql(body: ExecuteSqlModel):
    try:
        query_sql = body.query_text
        if len(query_sql) == 0:
            return Result.common(400, 'Query is empty.')
        result = exec_db_query_json_imp(request, True)
        if result == 'Query to change database is not allowed':
            return Result.common(400, result)
        else:
            resultList = [json.loads(item) for item in result]
            return Result.success(resultList)
    except Exception as err:
        current_app.logger.error('execute_sql: ' + str(err))
        return Result.common(500, str(err))


class GetQueryHistoryModel(BaseModel):
    conn_id: int = Field(None, description='数据库连接id,传了获取对应数据库的查询历史,不传获取所有的历史')
    page: int = Field(None)
    size: int = Field(None)


@bp.route('/get_query_history', methods=['GET'])
@login_required
@siwa.doc(summary='获取查询历史', tags=['workbench'], query=GetQueryHistoryModel)
def get_query_history(query: GetQueryHistoryModel):
    connId = request.args.get('conn_id')
    page = query.page
    size = query.size
    start = (int(page) - 1) * int(size)
    user_id = current_user.id if current_user.id is not None else 0
    if connId is None:
        allHistory = db.session.execute(text(
            f'SELECT a.* FROM saved_query a JOIN db_connection b ON a.conn_id = b.id WHERE b.is_delete = 0 and b.state = 1 AND a.is_delete = 0 and a.user_id = {user_id}'))
        queryHistory = db.session.execute(text(
            f'SELECT a.* FROM saved_query a JOIN db_connection b ON a.conn_id = b.id WHERE b.is_delete = 0 and b.state = 1 AND a.is_delete = 0 and a.user_id = {user_id} order by a.update_time desc limit {size} OFFSET {start}'))
    else:
        allHistory = db.session.execute(text(
            f'SELECT a.* FROM saved_query a JOIN db_connection b ON a.conn_id = b.id WHERE b.is_delete = 0 and b.state = 1 AND a.id IN ( SELECT MAX( id ) FROM saved_query WHERE user_id = {user_id} AND conn_id = {connId} AND is_delete = 0 GROUP BY question_text )'))
        queryHistory = db.session.execute(text(
            f'SELECT a.* FROM saved_query a JOIN db_connection b ON a.conn_id = b.id WHERE b.is_delete = 0 and b.state = 1 AND a.id IN ( SELECT MAX( id ) FROM saved_query WHERE user_id = {user_id} AND conn_id = {connId} AND is_delete = 0 GROUP BY question_text ) order by a.update_time desc limit {size} OFFSET {start}'))

    queryList = []
    connIdList = []
    for row in queryHistory:
        query = {
            'id': row[0],
            'user_id': row[1],
            'conn_id': row[2],
            'question_text': row[3],
            'query_text': eval(str(row[4]) if '[' in str(row[4]) and ']' in str(row[4]) else '[]'),
            'my_query_text': row[5],
            'is_delete': row[6],
            'create_time': row[7],
            'update_time': row[8]
        }
        queryList.append(query)
        connIdList.append(row[2])
    db_msg = DBConnection.query.filter(DBConnection.id.in_(connIdList)).all()
    # 获取收藏记录
    favoriteList = FavoriteQuery.query.filter_by(user_id=user_id, conn_id=connId, is_delete=0).all()

    for a in queryList:
        a['is_collect'] = 0
        for b in db_msg:
            if a['conn_id'] == b.id:
                a['db_msg'] = {
                    'id': b.id,
                    'name': b.name,
                    'db_type': b.db_type,
                    'db_name': b.db_name,
                    'username': b.username,
                    'password': b.password,
                    'ip_address': b.ip_address,
                    'port_number': b.port_number,
                    'ds_name': b.ds_name,
                    'db_summary': b.db_summary,
                    'database_file': b.database_file
                }
                break
        for c in favoriteList:
            if a['question_text'] == c.favorite_text:
                a['is_collect'] = 1
                break

    allCount = 0
    for item in allHistory:
        allCount += 1
    if len(queryList) > 0:
        allPage = math.ceil(allCount / int(size))
    else:
        allPage = 0

    return Result.successWithPage(queryList, allPage, page, allCount)


@bp.route('/delete_query_history/<int:saveQueryId>', methods=['PUT'])
@login_required
@siwa.doc(summary='删除查询历史,saveQueryId: 历史查询id', tags=['workbench'])
def delete_query_history(saveQueryId):
    saveQuery = SavedQuery.query.filter_by(id=saveQueryId).first()
    saveQuery.is_delete = 1
    db.session.commit()
    return Result.success()


class MySqlQueryModel(BaseModel):
    conn_id: int = Field(description='数据库连接id')
    question_text: str = Field(description='查询问题')
    my_sql_query: str = Field(description='自己的sql语句')


@bp.route('/save_my_sql_query', methods=['POST'])
@login_required
@siwa.doc(summary='保存自己的sql语句', tags=['workbench'], body=MySqlQueryModel)
def save_my_sql_query(body: MySqlQueryModel):
    user_id = current_user.id
    saveQuery = SavedQuery.query.filter_by(user_id=user_id, conn_id=body.conn_id,
                                           question_text=body.question_text).order_by(
        SavedQuery.create_time.desc()).first()
    favorite = FavoriteQuery.query.filter_by(user_id=user_id, conn_id=body.conn_id,
                                             favorite_text=body.question_text).first()
    saveQuery.my_query_text = body.my_sql_query
    if favorite is not None:
        favorite.my_query_text = body.my_sql_query
    newId = saveQuery.id
    response_json = update_saved_query(query_id=newId, user_id=user_id, conn_id=body.conn_id,
                                       question_text=body.question_text,
                                       query_text=saveQuery.query_text, my_query_text=body.my_sql_query)
    if response_json['status'] == 0:
        current_app.logger.info('Query is saved!')
    else:
        current_app.logger.error(f'{response_json}')

    # saveQuery.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()
    return Result.success()


class AddFavoriteQueryModel(BaseModel):
    conn_id: int = Field(description='数据库连接id')
    favorite_text: str = Field(description='收藏的问题')
    query_text: str = Field(description='sql语句')
    my_query_text: str = Field(description='自己写的sql语句')


@bp.route('/add_favorite_query', methods=['POST'])
@login_required
@siwa.doc(summary='收藏查询记录', tags=['workbench'], body=AddFavoriteQueryModel)
def add_favorite_query(body: AddFavoriteQueryModel):
    userId = current_user.id
    favorite = FavoriteQuery.query.filter_by(user_id=userId, conn_id=body.conn_id,
                                             favorite_text=body.favorite_text).first()
    if favorite is None:
        favoriteQuery = FavoriteQuery()
        favoriteQuery.query_text = body.query_text
        favoriteQuery.my_query_text = body.my_query_text
        favoriteQuery.is_delete = 0
        favoriteQuery.user_id = userId
        favoriteQuery.conn_id = body.conn_id
        favoriteQuery.favorite_text = body.favorite_text
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        favoriteQuery.create_time = now
        favoriteQuery.update_time = now
        db.session.add(favoriteQuery)
        db.session.flush()
        newId = favoriteQuery.id
        db.session.commit()

        # 保存favorite query
        response_json = create_favorite_query(newId=newId, is_delete=0, user_id=userId, conn_id=body.conn_id,
                                              favorite_text=body.favorite_text,
                                              query_text=body.query_text, my_query_text=body.my_query_text)
        if response_json['status'] == 0:
            current_app.logger.info('Favorite query is saved!')

        return Result.common(200, 'Add favorite success')
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if favorite.is_delete == 0:
            favorite.is_delete = 1
            favorite.update_time = now
            favorite.query_text = body.query_text
            favorite.my_query_text = body.my_query_text
            db.session.commit()

            # 保存favorite query
            response_json = create_favorite_query(newId=favorite.id, is_delete=1, user_id=userId, conn_id=body.conn_id,
                                                  favorite_text=body.favorite_text,
                                                  query_text=body.query_text, my_query_text=body.my_query_text)
            if response_json['status'] == 0:
                current_app.logger.info('Favorite query is saved!')

            return Result.common(200, 'Cancel favorite success')
        else:
            favorite.is_delete = 0
            favorite.update_time = now
            favorite.query_text = body.query_text
            favorite.my_query_text = body.my_query_text
            db.session.commit()

            # 保存favorite query
            response_json = create_favorite_query(newId=favorite.id, is_delete=0, user_id=userId, conn_id=body.conn_id,
                                                  favorite_text=body.favorite_text,
                                                  query_text=body.query_text, my_query_text=body.my_query_text)
            if response_json['status'] == 0:
                current_app.logger.info('Favorite query is saved!')

            return Result.common(200, 'Add favorite success')


@bp.route('/delete_favorite_query/<int:favoriteQueryId>', methods=['PUT'])
@login_required
# @siwa.doc(summary='删除收藏记录,favoriteQueryId: 收藏记录id', tags=['workbench'])
def delete_favorite_query(favoriteQueryId):
    favoriteQuery = FavoriteQuery.query.filter_by(id=favoriteQueryId).first()
    favoriteQuery.is_delete = 1
    db.session.commit()
    return Result.success()


class FavoriteQueryModel(BaseModel):
    conn_id: int = Field(None, description='数据库连接id,传了获取对应数据库的收藏爱好,不传获取所有的收藏爱好')
    page: int = Field(None)
    size: int = Field(None)


@bp.route('/get_favorite_query', methods=['GET'])
@login_required
@siwa.doc(summary='获取收藏记录', tags=['workbench'], query=FavoriteQueryModel)
def get_favorite_query(query: FavoriteQueryModel):
    page = query.page
    size = query.size
    start = (int(page) - 1) * int(size)

    userId = current_user.id if current_user.id is not None else 0
    if query.conn_id is None:
        allFavoriteQuery = db.session.execute(text(
            f'SELECT a.* from favorite_query a JOIN db_connection b on a.conn_id = b.id WHERE a.is_delete = 0 and b.is_delete = 0 and a.user_id = {userId}'))
        favoriteQuery = db.session.execute(text(
            f'SELECT a.* from favorite_query a JOIN db_connection b on a.conn_id = b.id WHERE a.is_delete = 0 and b.is_delete = 0 and a.user_id = {userId} order by a.update_time desc limit {size} OFFSET {start}'))
    else:
        allFavoriteQuery = db.session.execute(text(
            f'SELECT a.* from favorite_query a JOIN db_connection b on a.conn_id = b.id WHERE a.is_delete = 0 and b.is_delete = 0 and a.user_id = {userId} and a.conn_id = {query.conn_id}'))
        favoriteQuery = db.session.execute(text(
            f'SELECT a.* from favorite_query a JOIN db_connection b on a.conn_id = b.id WHERE a.is_delete = 0 and b.is_delete = 0 and a.user_id = {userId} and a.conn_id = {query.conn_id} order by a.update_time desc limit {size} OFFSET {start}'))
    conns = DBConnection.query.filter_by(is_delete=0).all()
    queryList = []
    for row in favoriteQuery:
        query = {
            'id': row[0],
            'user_id': row[1],
            'conn_id': row[2],
            'favorite_text': row[3],
            'query_text': eval(str(row[4]) if '[' in str(row[4]) else '[]'),
            'my_query_text': row[5],
            'is_delete': row[6],
            'create_time': row[7],
            'update_time': row[8],
            'is_collect': 1
        }
        for b in conns:
            if query['conn_id'] == b.id:
                query['db_msg'] = {
                    'id': b.id,
                    'name': b.name,
                    'db_type': b.db_type,
                    'db_name': b.db_name,
                    'username': b.username,
                    'password': b.password,
                    'ip_address': b.ip_address,
                    'port_number': b.port_number,
                    'ds_name': b.ds_name,
                    'db_summary': b.db_summary,
                    'database_file': b.database_file
                }
                break
        queryList.append(query)
    allCount = 0
    for item in allFavoriteQuery:
        allCount += 1
    if len(queryList) > 0:
        allPage = math.ceil(allCount / int(size))
    else:
        allPage = 0

    return Result.successWithPage(queryList, allPage, page, allCount)


class RelatedQuestionModel(BaseModel):
    database_schema: str
    user_question: str = Field(description='用户问题')
    sql_query: str = Field(description='sql语句')
    number_of_questions: int = Field(description='获取相关问题的数量')
    conn_id: int = Field(description='数据库连接id')
    saved_query_id: int = Field(None, description="查询的历史记录id")


@bp.route('/related_questions', methods=['POST'])
@login_required
@siwa.doc(summary='获取相关问题', tags=['workbench'], body=RelatedQuestionModel)
def get_related_questions(body: RelatedQuestionModel):
    data = request.get_json()
    # database_schema = data['database_schema']
    # sql_query = data['sql_query']
    # number_of_questions = data['number_of_questions'] or 5
    user_question = data['user_question']
    userId = current_user.id
    data['user_id'] = userId
    data['portal_username'] = Config.API_USER_NAME

    try:
        if len(user_question) == 0 or data['saved_query_id'] == 0:
            relatedQuestions = db.session.execute(text(
                f'SELECT * from related_questions WHERE id in (SELECT MAX(id) from related_questions WHERE user_id = {userId} and conn_id = {body.conn_id} GROUP BY question ORDER BY id desc LIMIT 15) ORDER BY id desc')).all()
            questionList = []
            for rq in relatedQuestions:
                questionList.append(rq.question)
            return Result.success(questionList)
        else:
            api_url = Config.API_ROOT + "/generate_related_questions"
            token = AccessToken().get_access_token()
            headers = {'Authorization': "Bearer {}".format(token)}
            response = requests.post(api_url, json=data, headers=headers)
            result = response.json()

            if result['status'] == 0:
                # 保存related questions
                newRelatedQuestions = result['result']
                for item in newRelatedQuestions:
                    from app.main.db_connections import create_relation_questions_new
                    create_relation_questions_new(userId, body.conn_id, item)
                # 保存usage记录
                # usageJson = result['usage']
                # from app.main.db_connections import create_usage
                # create_usage(Config.API_USER_NAME, body.conn_id, current_user.id, user_question, 3,
                #              usageJson['total_tokens'],
                #              usageJson['prompt_tokens'], usageJson['completion_tokens'])

                relatedQuestions = db.session.execute(text(
                    f'SELECT * from related_questions WHERE id in (SELECT MAX(id) from related_questions WHERE user_id = {userId} and conn_id = {body.conn_id} GROUP BY question ORDER BY id desc LIMIT 15) ORDER BY id desc')).all()
                questionList = []
                for rq in relatedQuestions:
                    questionList.append(rq.question)
                return Result.success(questionList)

            else:
                return Result.common(400, result['result'])
    except Exception as err:
        error_string = f"{err}"
        current_app.logger.error(error_string)
        return Result.common(500, error_string)


class DownloadModel(BaseModel):
    db_name: str = Field(description='数据库名')
    db_type: str = Field(description='数据库类型')
    ds_name: str
    ip_address: str = Field(description='数据库连接地址')
    username: str = Field(description='用户名')
    password: str = Field(description='密码')
    port_number: str = Field(description='端口')
    query_text: str = Field(description='sql语句')
    database_file: str = Field(description='添加sqlite时的文件地址', default='')


@bp.route('/download', methods=['POST'])
@login_required
@siwa.doc(summary='download', tags=['workbench'], body=DownloadModel)
def download(body: DownloadModel):
    try:
        query_sql = body.query_text
        if len(query_sql) == 0:
            return Result.common(400, 'Query is empty.')
        result = exec_db_query_json_imp(request, False)
        resultList = [json.loads(item) for item in result]

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheetCount = 0
        for sheet in resultList:
            sheetCount += 1
            # jsonString = json.loads(sheet)

            sheet1 = workbook.add_worksheet('sheet' + str(sheetCount))
            columns = sheet['columns']
            rows = sheet['rows']
            fields = [item['name'] for item in columns]
            # 写入数据到A1一列
            sheet1.write_row('A1', fields)
            for row in rows:
                rowKeys = row.keys()
                for col in columns:
                    for key in rowKeys:
                        if col['prop'] == key:
                            row[col['name']] = row.pop(key)
                            break
            for i in range(len(rows)):
                for x in range(len(fields)):
                    key = [key for key in rows[i].keys()]
                    sheet1.write(i + 1, x, rows[i][key[x]])
        workbook.close()  # 需要关闭
        output.seek(0)  # 找到流的起始位置
        resp = make_response(output.getvalue())
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        basename = f'{filename}.xlsx'

        # 转码，支持中文名称
        resp.headers["Content-Disposition"] = f"attachment; filename={basename}"

        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp
    except Exception as err:
        current_app.logger.error('download: ' + str(err))
        return Result.common(500, {err})


# class GetSummaryModel(BaseModel):
#     conn_id: int = Field(None, description='数据库连接id,编辑的时候传,添加数据库的时候不传')
#     database_schema: str = Field(description='数据库模型结构')


class GetSummaryModel(BaseModel):
    db_name: str = Field(description='数据库名')
    db_type: str = Field(description='数据库类型')
    ds_name: str
    ip_address: str = Field(description='数据库连接地址')
    username: str = Field(description='用户名')
    password: str = Field(description='密码')
    port_number: str = Field(description='端口')
    database_file: str = Field(description='添加sqlite时的文件地址', default='')
    conn_id: int = Field(None, description='数据库连接id,编辑时上传,新增时不上传')


@bp.route('/get_summary', methods=['POST'])
@login_required
@siwa.doc(summary='获取summary', tags=['workbench'], body=GetSummaryModel)
def get_summary(body: GetSummaryModel):
    result = get_db_schema_imp(request)
    database_schema = result['db_schema']
    data = {
        'database_schema': database_schema,
        'user_id': current_user.id,
        'portal_username': Config.API_USER_NAME,
        'ip_address': body.ip_address,
        'db_name': body.db_name
    }
    if body.conn_id is not None:
        data['conn_id'] = body.conn_id
    api_url = Config.API_ROOT + "/get_db_summary"
    token = AccessToken().get_access_token()
    headers = {'Authorization': "Bearer {}".format(token)}
    response = requests.post(api_url, json=data, headers=headers)
    return Result.success(response.json()['result'])


class FeedbackModel(BaseModel):
    conn_id: int = Field(description='数据库连接id')
    question: str = Field(description='问题')
    sql: str = Field(description='sql语句')
    error_msg: str = Field(description='错误信息')


@bp.route('/feedback', methods=['POST'])
@login_required
@siwa.doc(summary='反馈', tags=['workbench'], body=FeedbackModel)
def feedback(body: FeedbackModel):
    data = {
        'conn_id': body.conn_id,
        'question': body.question,
        'sql': body.sql,
        'error_msg': body.error_msg,
        'portal_username': Config.API_USER_NAME,
        'user_id': current_user.id,
        'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    api_url = Config.API_ROOT + "/api/feedback"
    token = AccessToken().get_access_token()
    headers = {'Authorization': "Bearer {}".format(token)}
    response = requests.post(api_url, json=data, headers=headers)
    result = response.json()['status']
    if result == 0:
        return Result.success()
    else:
        return Result.common(400, 'Feedback failure')
