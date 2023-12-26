import os
import openai
from flask import render_template, request, current_app, flash, redirect, url_for
import requests
from flask_login import current_user, login_required
from config import Config
from app.app_log import app_log
from app.main import bp
from app.main.dbexec import get_db_schema_imp, exec_db_query_imp, exec_db_query_json_imp, get_db_size_imp
from app.access_token import AccessToken
from app.main.forms import RegisterConnectionForm
from app import db
from app.main.db_connections import create_db_connection, get_db_connections, update_db_connection, delte_db_connection
from app.main.saved_queries import create_saved_query, get_saved_queries, update_saved_query, delete_saved_query

"""html views"""
@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@bp.route('/dbsql', methods=['GET'])
@login_required
def index():
    print('dbsql.html')
    return render_template('dbsql.html', title='Workbench')

@bp.route('/manage', methods=['GET'])
@login_required
def manage():
    if current_user.username != 'admin':
        return redirect(url_for('main.index'))

    return render_template('manage.html', title='Management')

@bp.route('/completion', methods=['GET'])
@login_required
def completion():
    return render_template('completion.html', title='Completion')

@bp.route('/connection_list', methods=['GET'])
@login_required
def connection_list():
    current_app.logger.info('GET connection_list called')
    
    db_conns = []
    response = get_db_connections()
    print(response)
    if response['status'] == 0:
        db_conns = response['result']
    
    return render_template('connection_list.html', title='Databases', db_conns=db_conns)

@bp.route('/register_connection', methods=['GET'])
@login_required
def register_connection():
    current_app.logger.info('GET register_connection called')
    if current_user.username != 'admin':
        return redirect(url_for('main.index'))
        
    return render_template('register_connection.html', title='Register Database')

@bp.route('/register_connection_post', methods=['POST'])
@login_required
def register_connection_post():
    current_app.logger.info('POST register_connection_post called')
    if current_user.username != 'admin':
        return redirect(url_for('main.index'))

    name = request.form['conn_name']
    db_type = request.form['db_type']
    db_name = request.form['db_name']
    username = request.form['username']
    password = request.form['password']
    ip_address = request.form['ip_address'] if db_type != 'mssql' else ''
    port_number = request.form['port_number'] if db_type != 'mssql' else ''
    ds_name = request.form['ds_name'] if db_type == 'mssql' else ''
    db_summary = request.form['database_summary']
    
    if name == None or name == '':
        flash('Please provide a name for the connection')
        return render_template('register_connection.html', title='Register')

    if db_type == None or db_type == '':
        flash('Please specify database type for the connection')
        return render_template('register_connection.html', title='Register')

    try:
        response_json = create_db_connection(name=name, db_type=db_type, db_name=db_name, username=username, password=password, ip_address=ip_address, port_number=port_number, ds_name=ds_name, db_summary=db_summary)
        if response_json['status'] == 0:
            flash('Connection Registered!')
        else:
            flash(f'Failed to register connection! Error: {response_json["error"]}')
    except Exception as error:
        flash(f'Failed to register connection! Error: {error}')
        
    return render_template('register_connection.html', title='Register Database')

""" APIs  """
@bp.route('/get_completion', methods=['POST'])
@login_required
def get_completion():
    print('get_completion')

    data = request.get_json()
    system_input = data['system_input']
    user_input = data['user_input']
    
    app_log.logger().info(f'SYSTEM_MESSAGE:{system_input}')
    app_log.logger().info(f'USER_MESSSAGE:{user_input}')

    try:
        api_url = Config.API_ROOT + "/get_completion"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        response = requests.post(api_url, json=data, headers=headers)
        return response.json()
    except Exception as error:
        app_log.logger().info(f'An error occured: {error}')
        return {"status": 1, "result": f"Error: {error}"}
    
@bp.route('/get_query_commendation', methods=['POST'])
@login_required
def get_query_commendation():
    print('get_query_commendation')

    data = request.get_json()
    database_schema = data['database_schema']
    user_question = data['user_question']
    #data['number_of_queries']=3
    #data['number_of_retries']=3
    
    app_log.logger().info(f'database_schema:{database_schema}')
    app_log.logger().info(f'user_question:{user_question}')
    
    try:
        api_url = Config.API_ROOT + "/get_query_commendation"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        response = requests.post(api_url, json=data, headers=headers)
        return response.json()
    except Exception as error:
        error_string = f"{error}"
        app_log.logger().info(error_string)
        return {"status": 1, "query": error_string, 'score':0}
        
@bp.route('/generate_related_queries', methods=['POST'])
@login_required
def generate_related_queries():
    print('generate_related_queries')

    data = request.get_json()
    database_schema = data['database_schema']
    user_question = data['user_question']
    sql_query = data['sql_query']
    number_of_queries = data['number_of_queries'] or 5
    
    app_log.logger().info(f'database_schema:{database_schema}')
    app_log.logger().info(f'user_question:{user_question}')
    app_log.logger().info(f'sql_query:{sql_query}')
    
    try:
        api_url = Config.API_ROOT + "/generate_related_queries"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        response = requests.post(api_url, json=data, headers=headers)
        app_log.logger().info(f'response:{response.json()}')
        return response.json()
    except Exception as err:
        error_string = f"{err}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}

@bp.route('/generate_related_questions', methods=['POST'])
@login_required
def generate_related_questions():
    print('generate_related_questions')

    data = request.get_json()
    database_schema = data['database_schema']
    user_question = data['user_question']
    sql_query = data['sql_query']
    number_of_questions = data['number_of_questions'] or 5
    
    app_log.logger().info(f'database_schema:{database_schema}')
    app_log.logger().info(f'user_question:{user_question}')
    app_log.logger().info(f'sql_query:{sql_query}')
    
    try:
        api_url = Config.API_ROOT + "/generate_related_questions"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        response = requests.post(api_url, json=data, headers=headers)
        app_log.logger().info(f'response:{response.json()}')
        return response.json()
    except Exception as err:
        error_string = f"{err}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}
        
@bp.route('/get_db_schema', methods=['POST'])
@login_required
def get_db_schema():
    print('get_db_schema')
    
    try:
        result = get_db_schema_imp(request)
        return {"status": 0, "result": result}
    except Exception as err:
        error_string = f"get_db_schema: {err}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}

@bp.route('/get_db_summary', methods=['POST'])
@login_required
def get_db_summary():
    print('get_db_summary')

    data = request.get_json()
    database_schema = data['database_schema']
    
    app_log.logger().info(f'database_schema:{database_schema}')
    try:
        api_url = Config.API_ROOT + "/get_db_summary"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        response = requests.post(api_url, json=data, headers=headers)
        return response.json()
    except Exception as error:
        error_string = f"get_db_summary: {error}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}

@bp.route('/get_db_size', methods=['POST'])
@login_required
def get_db_size():
    print('get_db_size')
    
    try:
        result = get_db_size_imp(request)
        return {"status": 0, "result": result}
    except Exception as err:
        error_string = f"get_db_size: {err}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}

@bp.route('/db_connections', methods=['GET'])
@login_required
def db_connections():
    current_app.logger.info('GET db_connections called')
    connections = []
    return get_db_connections()

@bp.route('/exec_db_query', methods=['POST'])
@login_required
def exec_db_query():
    print('exec_db_query')

    try:
        result = exec_db_query_imp(request)
        return {"status": 0, "result": result}
    except Exception as err:
        error_string = f"exec_db_query: {err}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}

@bp.route('/exec_db_query_json', methods=['POST'])
@login_required
def exec_db_query_json():
    print('exec_db_query_json')

    try:
        result = exec_db_query_json_imp(request)
        return {"status": 0, "result": result}
    except Exception as err:
        error_string = f"exec_db_query_json: {err}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}

@bp.route('/get_saved_db_queries', methods=['POST'])
@login_required
def get_saved_db_queries():
    current_app.logger.info('POST get_saved_db_queries called')

    data = request.get_json()
    conn_id = int(data['conn_id'])    

    user_queriesJson = []
    response_json = get_saved_queries(current_user.id, conn_id)
    if response_json['status'] == 0:
        user_queries = response_json['result']
        for q in user_queries:
            query = {
                'id':q['id'],
                'question':q['question_text'],
                'query':q['query_text']
                }
            user_queriesJson.append(query)
        
    app_log.logger().info(user_queriesJson)
    
    return {"status": 0, "result": user_queriesJson}

@bp.route('/save_db_query', methods=['POST'])
@login_required
def save_db_query():
    print('save_db_query')

    try:
        data = request.get_json()
        conn_id = int(data['conn_id'])
        question = data['question']
        query = data['query']

        response_json = create_saved_query(user_id=current_user.id, conn_id=conn_id, question_text=question, query_text=query)
        if response_json['status'] == 0:
            response_json['result'] = 'Query is saved!'
            
        return response_json
        
    except Exception as error:
        error_string = f"save_db_query: {error}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}

def get_db_schema_by_connection_string():
    print('get_db_schema_by_connection_string')
    
    try:
        data = request.get_json()
        db_connection_string = data['db_connection_string']
        if len(db_connection_string) == 0:
            return {"status": 1, "result": "Connection string is empty."}
        
        result = get_db_schema_imp(db_connection_string)
        return {"status": 0, "result": result}
    except Exception as err:
        error_string = f"{err}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}

def exec_db_query_by_connection_string():
    print('exec_db_query_by_connection_string')

    try:
        data = request.get_json()
        db_connection_string = data['db_connection_string']
        if len(db_connection_string) == 0:
            return {"status": 1, "result": "Connection string is empty."}

        query_text = data['query_text']
        if len(query_text) == 0:
            return {"status": 1, "result": "Query is empty."}

        # change to the database are not allowed to avoid mistakes
        bad_kw = ('add', 'create', 'drop', 'alter', 'update', 'delete', 'insert', 'truncate')
        query_text_lower = query_text.lower()
        if any(word in bad_kw for word in query_text_lower.split()):
            return {"status": 1, "result": 'Query to change database is not allowed'}
        
        result = exec_db_query_imp(db_connection_string, query_text)
        return {"status": 0, "result": result}
    except Exception as err:
        error_string = f"{err}"
        app_log.logger().info(error_string)
        return {"status": 1, "result": error_string}
