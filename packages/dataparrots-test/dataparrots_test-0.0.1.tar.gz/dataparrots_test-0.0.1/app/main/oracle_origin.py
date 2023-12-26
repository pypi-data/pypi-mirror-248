from sqlalchemy import create_engine
from sqlalchemy import text
from app.app_log import app_log
from app.main.db_base import db_base

# not tested
class oracle(db_base):
    @classmethod
    def get_schema(cls, db_connection_string):
        app_log.logger().info(f"oracle/get_schema called")
        return "Oracle not yet supported"

    @classmethod
    def get_connection_string(cls, username, password, ip_address, port_number, db_name, **kwargs):
        str = f'oracle://{username}:{password}@{ip_address}:{port_number}/{db_name}'
        return str
        
    @classmethod
    def _get_tables_query(cls, db_name):
        return f"""
SELECT table_name
FROM all_tables
WHERE owner NOT IN ('SYS', 'SYSTEM')
"""
        
    @classmethod
    def _get_columns_query(cls, table_name):
        return f"""
SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, NULLABLE
FROM ALL_TAB_COLUMNS
WHERE TABLE_NAME = '{table_name}';
"""
        