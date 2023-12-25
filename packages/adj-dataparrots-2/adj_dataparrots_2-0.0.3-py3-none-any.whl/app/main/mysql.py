import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect
from app.app_log import app_log
from app.main.db_base import db_base

class mysql(db_base):
    @classmethod
    def get_schema(cls, db_connection_string):
        db_schema = ''
        db_schema_human = '['
        engine = create_engine(db_connection_string, echo=False)

        insp = inspect(engine)
        with engine.connect() as conn:
            for t in conn.execute(text("show tables")):
                table_comment = cls.get_table_comment(t[0], conn)
                table_comment = f', comment: {table_comment}' if table_comment != '' else ''
                db_schema += f"table:{t[0]}{table_comment}\n"
                db_schema_human += "\n{" + f"'table':{t[0]},\n'columns':["
                columns_human_str = ''

                for c in conn.execute(text(f"show full columns from {t[0]}")):
                    column_comment = c[8]
                    column_comment = f', comment: {column_comment}' if column_comment != '' else ''
                    db_schema += f"({c[0]}, {c[1]}{column_comment})\n"
                    columns_human_str += f"""{c[0].strip("'")},"""

                db_schema_human += columns_human_str.strip(',') + ']},'

                primary_key_str = 'Primary Key:'
                p = insp.get_pk_constraint(t[0])
                primary_key_str += f"{p['constrained_columns']},"
                db_schema +=primary_key_str.strip(',')

                foreign_key_str = '\nForeign Keys: ['
                for f in insp.get_foreign_keys(t[0]):
                    foreign_key_str += f"\n({t[0]}:{f['constrained_columns']},{f['referred_table']}:{f['referred_columns']}),"
                db_schema +=foreign_key_str.strip(',') + ']'

                db_schema += "\n\n"

        db_schema_human = db_schema_human.strip(',') + '\n]'
        #print(db_schema)
        #print(db_schema_human)
        app_log.logger().info(f"get_db_schema_imp:schema=\n{db_schema}\n{db_schema_human}")
        return {'db_schema':db_schema, 'db_schema_human':db_schema_human}
        

    @classmethod
    def get_connection_string(cls, username, password, ip_address, port_number, db_name, **kwargs):
        str = f'mysql://{username}:{password}@{ip_address}:{port_number}/{db_name}'
        return str

    @classmethod
    def get_table_comment(cls, table, conn):
        sql=f"SELECT table_comment FROM INFORMATION_SCHEMA.TABLES WHERE table_name='{table}'"
        comments = conn.execute(text(sql))
        for c in comments:
            return c[0]
