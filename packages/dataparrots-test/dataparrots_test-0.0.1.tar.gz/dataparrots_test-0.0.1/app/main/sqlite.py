from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect
from app.app_log import app_log
from app.main.db_base import db_base

class sqlite(db_base):
    @classmethod
    def has_table_comment(cls):
        return False

    @classmethod
    def has_column_comment(cls):
        return False
        
    @classmethod
    def get_connection_string(cls, database_file, username, password, ip_address, port_number, db_name, **kwargs):
        return cls.get_connection_string_dsn(database_file)

    @classmethod
    def get_connection_string_dsn(cls, filename):
        return f"sqlite:///{filename}"

