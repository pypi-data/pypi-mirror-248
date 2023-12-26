import importlib
from sqlalchemy import create_engine
from sqlalchemy import text
from app.app_log import app_log

def get_dbclass_connection_string_from_request(request_data):
    db_type = request_data['db_type']
    class_name = class_for_name('app.main.'+db_type, db_type)
    return class_name, class_name.get_connection_string(**request_data)

def get_db_schema_imp(request):
    print("get_db_schema_imp")

    data = request.get_json()
    class_type, db_connection_string = get_dbclass_connection_string_from_request(data)
    schema = class_type.get_schema(db_connection_string)
        
    return schema


def get_db_schema_imp_new(data):

    class_type, db_connection_string = get_dbclass_connection_string_from_request(data)
    schema = class_type.get_schema(db_connection_string)

    return schema
    
def get_db_size_imp(request):
    print("get_db_size_imp")
    
    data = request.get_json()
    class_type, db_connection_string = get_dbclass_connection_string_from_request(data)
    db_size_str = class_type.get_db_size(db_connection_string)
        
    return db_size_str    


def exec_db_query_json_imp(request, is_limit_page):
    print("exec_db_query_json_imp")
    
    data = request.get_json()
    query_text = data['query_text']
    if len(query_text) == 0:
        return 'Query is empty.'

    # change to the database are not allowed to avoid mistakes
    bad_kw = ('add', 'create', 'drop', 'alter', 'update', 'delete', 'insert', 'truncate')
    query_text_lower = query_text.lower()
    if any(word in bad_kw for word in query_text_lower.split()):
        return 'Query to change database is not allowed'

    class_type, db_connection_string = get_dbclass_connection_string_from_request(data)
    queryList = query_text.split(';')
    resultList = []
    for query in queryList:
        if query is not None and query != '' and query != ' ' and len(query) != 0 and query != '\n':
            result = class_type.exec_query_json(db_connection_string, query, data['db_type'], is_limit_page)
            resultList.append(result)

    return resultList


def exec_db_query_json_imp_new(data, is_limit_page):
    print("exec_db_query_json_imp_new")

    # data = request.get_json()
    query_text = data['query_text']
    if len(query_text) == 0:
        return 'Query is empty.'

    # change to the database are not allowed to avoid mistakes
    bad_kw = ('add', 'create', 'drop', 'alter', 'update', 'delete', 'insert', 'truncate')
    query_text_lower = query_text.lower()
    if any(word in bad_kw for word in query_text_lower.split()):
        return 'Query to change database is not allowed'

    class_type, db_connection_string = get_dbclass_connection_string_from_request(data)
    queryList = query_text.split(';')
    resultList = []
    for query in queryList:
        if query is not None and query != '' and query != ' ' and len(query) != 0 and query != '\n':
            result = class_type.exec_query_json(db_connection_string, query, data['db_type'], is_limit_page)
            resultList.append(result)

    return resultList

def exec_db_query_imp(request):
    print("exec_db_query_imp")

    data = request.get_json()
    query_text = data['query_text']
    if len(query_text) == 0:
        return 'Query is empty.'

    # change to the database are not allowed to avoid mistakes
    bad_kw = ('add', 'create', 'drop', 'alter', 'update', 'delete', 'insert', 'truncate')
    query_text_lower = query_text.lower()
    if any(word in bad_kw for word in query_text_lower.split()):
        return 'Query to change database is not allowed'

    class_type, db_connection_string = get_dbclass_connection_string_from_request(data)
    result = class_type.exec_query(db_connection_string, query_text)

    return result

def get_db_schema_from_connection_string_imp(db_connection_string):
    if len(db_connection_string) < 10:
        return "Bad connection string."

    try:
        class_type = server_class_from_connection_string(db_connection_string)
        schema = class_type.get_schema(db_connection_string)
    except Exception as err:
        error_string = f"{err}"
        app_log.logger().info(error_string)
        return error_string
        
    return schema

def exec_db_query_from_connection_string_imp(db_connection_string, query_text):
    if len(db_connection_string) < 10:
        return "Bad connection string."

    try:
        class_type = server_class_from_connection_string(db_connection_string)
        result = class_type.exec_query(db_connection_string, query_text)
    except Exception as err:
        error_string = f"{err}"
        app_log.logger().info(error_string)
        return error_string

    return result

def server_class_from_connection_string(db_connection_string):
    server_type_enum = ('mysql', 'mssql', 'oracle', 'postgresql', 'sqlite', 'sybase', 'mariadb', 'db2')
    for x in server_type_enum:
        server_type = x if db_connection_string.startswith(x) == True else server_type
    
    return class_for_name('app.main.'+server_type, server_type)
    
def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c    
       

"""
SQL Server
Select column_name From INFORMATION_SCHEMA.COLUMNS Where TABLE_NAME = 'TABLENAME'
SELECT TOP 0 * FROM table_name

It depends from the database you use. Here is an incomplete list:

sqlite3: .schema table_name
Postgres (psql): \d table_name
SQL Server: sp_help table_name (or sp_columns table_name for only columns)
Oracle DB2: desc table_name or describe table_name
MySQL: describe table_name (or show columns from table_name for only columns)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://username:password@localhost:port/DBNAME"

DECLARE @tableName nvarchar(100)
SET @tableName = N'members' -- change with table name
SELECT
    [column].*,
    COLUMNPROPERTY(object_id([column].[TABLE_NAME]), [column].[COLUMN_NAME], 'IsIdentity') AS [identity]
FROM 
    INFORMATION_SCHEMA.COLUMNS [column] 
WHERE
    [column].[Table_Name] = @tableName
"""

"""
SQL Server 2000, 2005, 2008, 2012, 2014, 2016, 2017 or 2019:

SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'
To show only tables from a particular database

SELECT TABLE_NAME 
FROM [<DATABASE_NAME>].INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
Or,

SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE' 
    AND TABLE_CATALOG='dbName' --(for MySql, use: TABLE_SCHEMA='dbName' )
PS: For SQL Server 2000:

SELECT * FROM sysobjects WHERE xtype='U' 
"""

""" MySQL get primary key
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'actor' AND CONSTRAINT_NAME = 'PRIMARY';"""

"""
To get all the tables in a SQL Server database, you can use the following query:

```sql
SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
```

This query retrieves all the tables from the `INFORMATION_SCHEMA.TABLES` view where the `TABLE_TYPE` is `'BASE TABLE'`. The result will include the table name, schema name, and other information about each table in the database.
"""

