from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect
from app.app_log import app_log
from app.main.db_base import db_base
import json

class mssql(db_base):
    @classmethod
    def exec_query_json(cls, db_connection_string, query_text, db_type, is_limit_page):
        db_name = db_connection_string.split('/')[-1]
        
        if '?' in db_name:                  # DSN less, remove from db_name ? and parameters after it. Not tested.
            db_name = db_name.split('?')[0] 
        else:                               # DSN, remove db_name from connection string
            db_connection_string = db_connection_string[:-len(db_name)-1]
        
        return super(cls, cls).exec_query_json(db_connection_string, query_text, db_type, is_limit_page)
        
    @classmethod
    def get_schema(cls, db_connection_string):
        db_name = db_connection_string.split('/')[-1]
        
        if '?' in db_name:                  # DSN less, remove from db_name ? and parameters after it
            db_name = db_name.split('?')[0] 
        else:                               # DSN, remove db_name from connection string
            db_connection_string = db_connection_string[:-len(db_name)-1]
        
        return super(cls, cls).get_schema(db_connection_string)

    @classmethod
    def get_headers_and_fields(cls, query_text):
        """ sqlglot does not support SQL Server dialect. Hack the SQL statement for now. """
        tokens = query_text.split()
        if (tokens[0].lower() == 'select') and (tokens[1].lower() == 'top'):
            tokens.pop(1)
            tokens.pop(1)

        for i in range(len(tokens)):
            tokens[i] = tokens[i].replace('[', '')
            tokens[i] = tokens[i].replace(']', '')
            
        query_text = " ".join(tokens)
        
        return super(cls, cls).get_headers_and_fields(query_text)
        
    @classmethod
    def get_db_size(cls, db_connection_string):
        db_name = db_connection_string.split('/')[-1]
        
        if '?' in db_name:                  # DSN less, remove from db_name ? and parameters after it
            db_name = db_name.split('?')[0] 
        else:                               # DSN, remove db_name from connection string
            db_connection_string = db_connection_string[:-len(db_name)-1]

        db_size_str = ''
        engine = create_engine(db_connection_string, echo=False)
        insp = inspect(engine)
        with engine.connect() as conn:
            for t in insp.get_table_names():
                result = conn.execute(text(f'select count(*) from [{t}]'))
                for x in result:
                    db_size_str += f'\n{t}({x[0]})'

        app_log.logger().info(f"get_db_size:db_size_str=\n{db_size_str}")
        return db_size_str
        
    @classmethod
    def get_connection_string(cls, username, password, ip_address, port_number, db_name, **kwargs):
        if kwargs.get('ds_name') != None:
            ds_name = kwargs['ds_name']
            if len(ds_name) > 0:
                return cls.get_connection_string_dsn(username, password, ds_name, db_name)
        
        if (ip_address == 'localhost' or ip_address == '127.0.0.1'):
            ip_address = '(local)'
            
        str = f'mssql+pyodbc://{username}:{password}@{ip_address},{port_number}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server'
        return str

    @classmethod
    def get_connection_string_dsn(cls, username, password, ds_name, db_name):
        str = f'mssql+pyodbc://{username}:{password}@{ds_name}/{db_name}'
        return str

    @classmethod
    def _get_tables_query(cls, db_name):
        return f"""
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE' 
    AND TABLE_CATALOG = '{db_name}'
    AND TABLE_SCHEMA != 'sys'
"""
        
    @classmethod
    def _get_columns_query(cls, table_name):
        return f"""
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = '{table_name}'
"""
