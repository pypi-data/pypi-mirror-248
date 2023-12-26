from app.app_log import app_log
from app.main.apirequest import request_post

def create_saved_query(newId, user_id, conn_id, question_text, query_text, my_query_text):
    url = '/api/create_saved_query'
    data = {
        'id': newId,
        'user_id': user_id,
        'conn_id': conn_id,
        'question_text': question_text,
        'query_text': query_text,
        'my_query_text': my_query_text
    }
    return request_post(url, data)

def create_favorite_query(newId, is_delete, user_id, conn_id, favorite_text, query_text, my_query_text):
    url = '/api/create_favorite_query'
    data = {
        'id': newId,
        'user_id': user_id,
        'conn_id': conn_id,
        'favorite_text': favorite_text,
        'query_text': query_text,
        'my_query_text': my_query_text,
        'is_delete': is_delete
    }
    return request_post(url, data)

def get_saved_queries(user_id, conn_id):
    url = '/api/get_saved_queries'
    data = { 
        'user_id': user_id,
        'conn_id': conn_id
    }    
    return request_post(url, data)

def update_saved_query(query_id, user_id, conn_id, question_text, query_text, my_query_text):
    url = '/api/update_saved_query'
    data = { 
        'query_id': query_id,
        'user_id': user_id,
        'conn_id': conn_id,
        'question_text': question_text,
        'query_text': query_text,
        'my_query_text': my_query_text
    }    
    return request_post(url, data)

def delete_saved_query(query_id):
    url = '/api/delete_saved_query'
    data = { 
        'query_id': query_id
    }    
    return request_post(url, data)
