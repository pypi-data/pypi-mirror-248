from sqlalchemy import create_engine
from sqlalchemy import text
from app.app_log import app_log
from app.main.db_base import db_base

# pip install sqlalchemy-sybase<2.0.0
# not tested
class sybase(db_base):
    @classmethod
    def get_schema(cls, db_connection_string):
        app_log.logger().info(f"sybase/get_schema called")
        return "sybase not yet supported"

    @classmethod
    def get_connection_string(cls, username, password, ip_address, port_number, db_name, **kwargs):
        str = f'sybase+pyodbc://{username}:{password}@{ip_address}:{port_number}/{db_name}'
        print(f'connection string = {str}')
        return str

    @classmethod
    def _get_tables_query(cls, db_name):
        return f"""
SELECT name
FROM sysobjects
WHERE type = 'U' AND sysstat & 0xf = 0
"""
        
    @classmethod
    def _get_columns_query(cls, table_name):
        return f"""
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = '{table_name}'
"""
        