from app.workbench import bp
from flask import request, current_app
from app import db, siwa
from pydantic import BaseModel, Field
from app.models import DBConnection, User
from app.common import Result
from sqlalchemy.sql import text
from flask_login import current_user, login_required
import datetime
from app.main.db_connections import create_db_connection_new, get_db_connections_new, update_db_connection
from app.main.db_connections import delte_db_connection, update_db_connection_state
from app.main.dbexec import get_db_schema_imp, exec_db_query_imp, exec_db_query_json_imp, get_db_size_imp, \
    exec_db_query_json_imp_new


class SaveDBConnectionVo(BaseModel):
    name: str = Field(description='连接名')
    db_type: str = Field(description='数据库类型')
    db_name: str = Field(description='数据库名')
    username: str = Field(description='用户名')
    password: str = Field(description='密码')
    ip_address: str = Field(description='数据库连接地址')
    port_number: str = Field(description='端口')
    db_summary: str = Field(description='简介')
    ds_name: str = Field(description='data source name')
    database_file: str = Field(description='添加sqlite时的文件地址', default='')


@bp.route('/add_db_connection', methods=['POST'])
@login_required
@siwa.doc(summary='新增数据库连接', tags=['databaseManagement'], form=SaveDBConnectionVo)
def add_db_connection(form: SaveDBConnectionVo):
    user_role = current_user.user_role
    # user_role = 'admin'
    # userIds = []
    # if user_role == 'admin':
    #     users = User.query.filter_by(user_role=user_role, is_delete=0).all()
    #     for row in users:
    #         userIds.append(row.id)

    name = form.name
    db_type = form.db_type
    db_name = form.db_name
    username = form.username
    password = form.password
    # ip_address = form.ip_address if db_type != 'mssql' else ''
    # port_number = form.port_number if db_type != 'mssql' else ''
    # ds_name = form.db_name if db_type == 'mssql' else ''
    ip_address = form.ip_address
    port_number = form.port_number
    ds_name = form.ds_name
    db_summary = form.db_summary
    database_file = form.database_file

    requestData = {
        'user_id': current_user.id,
        'db_type': db_type,
        'db_name': db_name,
        'username': username,
        'password': password,
        'ip_address': ip_address,
        'port_number': port_number,
        'ds_name': ds_name,
        'database_file': database_file
    }

    if name is None or name == '':
        return Result.common(400, 'Please specify database name for the connection')

    if db_type is None or db_type == '':
        return Result.common(400, 'Please specify database type for the connection')

    try:
        response_json = create_db_connection_new(requestData, database_file,
                                                 name,
                                                 db_type, db_name,
                                                 username,
                                                 password, ip_address, port_number,
                                                 ds_name, db_summary)
        if response_json['status'] == 0:
            return Result.success()
        else:
            current_app.logger.error(response_json['error'])
            return Result.common(400, f'Failed to register connection! Error: {response_json["error"]}')
    except Exception as error:
        current_app.logger.error(error)
        return Result.common(500, f'Failed to register connection! Error: {error}')


class DatabasePageModel(BaseModel):
    db_type: str = Field(title='数据库类型')
    page: int = Field(default=1, title="当前页", description='当前页')
    size: int = Field(default=10, title="每页数量", description='每页数量', ge=1, le=20)
    state: list[int] = Field(None, description='状态筛选')
    keyword: str = Field(None, description='关键字搜索')


@bp.route('/connection_list', methods=['POST'])
@login_required
@siwa.doc(summary='获取所有的数据库连接', tags=['databaseManagement'], body=DatabasePageModel)
def get_all_db_connections(body: DatabasePageModel):
    dbType = body.db_type
    page = body.page
    size = body.size
    start = (int(page) - 1) * int(size)
    state = body.state
    keyword = body.keyword
    result = get_db_connections_new(dbType, int(page), start, int(size), state, keyword)
    return result


@bp.route('/delete/<int:connectionId>', methods=['PUT'])
@login_required
@siwa.doc(summary='删除数据库连接', tags=['databaseManagement'])
def delete_connection(connectionId):
    result = delte_db_connection(connectionId)
    if result['status'] == 0:
        return Result.success()
    else:
        return Result.common(400, result['error'])


class UpdateDBConnectionVo(BaseModel):
    id: int
    name: str = Field(description='连接名')
    db_type: str = Field(description='数据库类型')
    db_name: str = Field(description='数据库名')
    username: str = Field(description='用户名')
    password: str = Field(description='密码')
    ip_address: str = Field(description='数据库连接地址')
    port_number: str = Field(description='端口')
    ds_name: str
    db_summary: str = Field(description='简介')
    database_file: str = Field(description='添加sqlite时的文件地址', default='')


@bp.route('/update', methods=['POST'])
@login_required
@siwa.doc(summary='修改数据库连接', tags=['databaseManagement'], form=UpdateDBConnectionVo)
def update_connection(form: UpdateDBConnectionVo):
    result = update_db_connection(form.id, form.name, form.db_type, form.db_name, form.username, form.password,
                                  form.ip_address, form.port_number, form.ds_name, form.db_summary, form.database_file)
    if result['status'] == 0:
        return Result.success()
    else:
        return Result.common(400, result['error'])


@bp.route('/update_state/<int:connectionId>/<int:state>', methods=['PUT'])
@login_required
@siwa.doc(summary='修改state状态,state(1,normal/0,stop)', tags=['databaseManagement'])
def update_state(connectionId, state):
    try:
        db_conn = DBConnection.query.filter_by(id=connectionId).first()
        db_conn.state = state
        db_conn.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()

        update_db_connection_state(connectionId, state)

        return Result.success()
    except Exception as error:
        current_app.logger.error(error)
        return Result.common(500, error)


class DbTypeMode(BaseModel):
    state: list[int] = Field(None, description='状态筛选')
    keyword: str = Field(description='关键字搜索', default="")


@bp.route('/get_db_type', methods=['POST'])
@login_required
@siwa.doc(summary='获取数据库类型', tags=['databaseManagement'], body=DbTypeMode)
def get_db_type(body: DbTypeMode):
    state = body.state
    keyword = body.keyword
    if len(state) > 0:
        db_conns = DBConnection().query.filter(DBConnection.name.like("%" + keyword + "%"),
                                               keyword is not None).filter(DBConnection.state.in_(state)).filter_by(
            is_delete=0)
    else:
        db_conns = DBConnection().query.filter(DBConnection.name.like("%" + keyword + "%"),
                                               keyword is not None).filter_by(
            is_delete=0)

    connList = [{'db_type': 'MySQL', 'value': 'mysql', 'count': 0},
                {'db_type': 'SQL Server', 'value': 'mssql', 'count': 0},
                {'db_type': 'SQLite', 'value': 'sqlite', 'count': 0},
                {'db_type': 'MariaDB', 'value': 'mariadb', 'count': 0},
                {'db_type': 'Oracle', 'value': 'oracle', 'count': 0},
                {'db_type': 'PostgreSQL', 'value': 'postgresql', 'count': 0}
                ]
    for row in db_conns:
        for conn in connList:
            if conn['value'] == row.db_type:
                conn['count'] += 1

    return Result.success(connList)
