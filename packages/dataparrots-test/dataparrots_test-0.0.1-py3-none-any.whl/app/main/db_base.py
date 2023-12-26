from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect
from app.app_log import app_log
from app.main.apirequest import request_post
import json
from sqlglot import parse_one, exp


class db_base:
    @classmethod
    def get_schema(cls, db_connection_string):
        db_schema = ''
        db_schema_human = '['
        engine = create_engine(db_connection_string, echo=False)
        insp = inspect(engine)

        for t in insp.get_table_names():
            tb_comment_str = insp.get_table_comment(t)['text'] if cls.has_table_comment() else ''
            tb_comment_str = f", Comment:{tb_comment_str}" if tb_comment_str != None else ''
            db_schema += f"Table: {t}{tb_comment_str}"
            db_schema_human += "\n{" + f"'table':{t},\n'columns':["
            columns_str = ''
            columns_human_str = ''
            for c in insp.get_columns(t):
                if cls.has_column_comment():
                    col_comment_str = f", Comment:{c['comment']}" if c['comment'] != None else ''
                else:
                    col_comment_str = ''
                c_type = f"{c['type']}"
                c_type = c_type.split(' ')[0]
                c_type = c_type.split('(')[0]
                columns_str += f"\n({c['name']}, {c_type}{col_comment_str})"
                columns_human_str += f"""{c['name'].strip("'")},"""
            db_schema += columns_str.strip(',')
            db_schema_human += columns_human_str.strip(',') + ']},'

            primary_key_str = '\nPrimary Key:'
            p = insp.get_pk_constraint(t)
            primary_key_str += f"{p['constrained_columns']},"
            db_schema += primary_key_str.strip(',') + ''

            foreign_key_str = '\nForeign Keys: ['
            for f in insp.get_foreign_keys(t):
                foreign_key_str += f"\n({t}, {f['constrained_columns']}, {f['referred_table']}, {f['referred_columns']}),"
            db_schema += foreign_key_str.strip(',') + ']'

            db_schema += "\n\n"

        db_schema_human = db_schema_human.strip(',') + '\n]'
        # print(db_schema)
        app_log.logger().info(f"get_db_schema_imp:schema=\n{db_schema}\n{db_schema_human}")
        return {'db_schema': db_schema, 'db_schema_human': db_schema_human}

    @classmethod
    def has_table_comment(cls):
        return True

    @classmethod
    def has_column_comment(cls):
        return True

    @classmethod
    def get_db_size(cls, db_connection_string):
        db_size_str = ''
        # print(db_connection_string)
        engine = create_engine(db_connection_string, echo=False)
        insp = inspect(engine)
        with engine.connect() as conn:
            for t in insp.get_table_names():
                result = conn.execute(text(f'select count(*) from {t}'))
                for x in result:
                    db_size_str += f'\n{t}({x[0]})'

        app_log.logger().info(f"get_db_size:db_size_str=\n{db_size_str}")
        return db_size_str

    @classmethod
    def exec_query(cls, db_connection_string, query_text):
        query_result = ''
        engine = create_engine(db_connection_string, echo=False)
        with engine.connect() as conn:
            result = conn.execute(text(query_text))
            for x in result:
                query_result += f'{x}\n'

        app_log.logger().info(f"exec_db_query_imp:result=\n{query_result}")
        return query_result

    @classmethod
    def exec_query_json(cls, db_connection_string, query_text, db_type, is_limit_page):
        query_result = {}
        engine = create_engine(db_connection_string, echo=False)
        with engine.connect() as conn:
            conn.text_factory = str
            if is_limit_page:
                # 设置分页 防止数据量太大
                query_text = cls.pageHandle(query_text, db_type)
            value_list = conn.execute(text(query_text))
            columns = []
            fields = value_list.keys()
            for field in fields:
                e = {'name': field, 'prop': field}
                columns.append(e)
            rows = []
            for row in value_list:
                e = dict(((field, str(value)) for field, value in zip(fields, row)))
                rows.append(e)
            query_result['columns'] = columns
            query_result['rows'] = rows
        app_log.logger().info(f"exec_db_query_imp:result=\n{query_result}")
        return json.dumps(query_result)

    @staticmethod
    def pageHandle(query_text, db_type):
        query_text_lower = query_text.lower()
        if 'mysql' == db_type or 'sqlite' == db_type or 'mariadb' == db_type or 'postgresql' == db_type:
            if 'limit ' not in query_text_lower:
                query_text = query_text.strip()
                if query_text[-2:] == '\n':
                    query_text = query_text[:-2]
                if query_text[-1:] == ';':
                    query_text = query_text[:-1]
                query_text = query_text + ' limit 200;'
        elif 'mssql' == db_type:
            if ' top ' not in query_text_lower:
                if ' distinct ' not in query_text_lower:
                    query_text = query_text.replace('select ', 'select top 200 ')
                    query_text = query_text.replace('select\n', 'select top 200 ')
                    query_text = query_text.replace('SELECT ', 'SELECT top 200 ')
                    query_text = query_text.replace('SELECT\n', 'SELECT top 200 ')
                    query_text = query_text.replace('Select ', 'Select top 200 ')
                    query_text = query_text.replace('Select\n', 'Select top 200 ')
                else:
                    query_text = query_text.replace('select distinct', 'select distinct top 200 ')
                    query_text = query_text.replace('SELECT DISTINCT', 'SELECT DISTINCT top 200 ')
                    query_text = query_text.replace('Select Distinct', 'Select Distinct top 200 ')
        elif db_type == 'oracle':
            if 'rownum' not in query_text_lower:
                query_text = query_text.strip()
                if query_text[-2:] == '\n':
                    query_text = query_text[:-2]
                if query_text[-1:] == ';':
                    query_text = query_text[:-1]
                query_text = 'SELECT * FROM (' + query_text + ') WHERE ROWNUM <= 200'
        return query_text

    @classmethod
    def get_connection_string(cls, database_file, username, password, ip_address, port_number, db_name, **kwargs):
        str = f"{kwargs['db_type']}://{username}:{password}@{ip_address}:{port_number}/{db_name}"
        return str

    @classmethod
    def get_headers_and_fields(cls, query_text):
        header_list = []
        for select in parse_one(query_text).find_all(exp.Select):
            for projection in select.expressions:
                header_list.append(projection.alias_or_name)
            break

        if len(header_list) == 0:  # Fix for non 'select' queries such as PRAGMA
            header_list.append('*')

        while header_list[-1] == '*' and len(header_list) > 1:
            header_list.pop()

        field_list = [f'f{index + 1}' for index, _ in enumerate(header_list)]

        return header_list, field_list


"""
It depends from the database you use. Here is an incomplete list:

sqlite3: .schema table_name
Postgres (psql): \d table_name
SQL Server: sp_help table_name (or sp_columns table_name for only columns)
Oracle DB2: desc table_name or describe table_name
MySQL: describe table_name (or show columns from table_name for only columns)
"""
