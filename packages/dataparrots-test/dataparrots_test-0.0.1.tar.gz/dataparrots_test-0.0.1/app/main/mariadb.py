from sqlalchemy import create_engine
from sqlalchemy import text
from app.app_log import app_log
from app.main.db_base import db_base

# pip install pymysql
# not tested
class mariadb(db_base):
    @classmethod
    def get_schema(cls, db_connection_string):
        return db_base.get_schema(db_connection_string)

    @classmethod
    def get_connection_string(cls, username, password, ip_address, port_number, db_name, **kwargs):
        str = f'mariadb+pymysql://{username}:{password}@{ip_address}:{port_number}/{db_name}'
        return str
