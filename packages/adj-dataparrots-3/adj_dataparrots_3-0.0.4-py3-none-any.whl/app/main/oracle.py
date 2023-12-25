import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect
from app.app_log import app_log
from app.main.db_base import db_base


class oracle(db_base):
    @classmethod
    def get_schema(cls, db_connection_string):
        username = cls.get_username(db_connection_string)
        db_schema = ''
        db_schema_human = '['
        engine = create_engine(db_connection_string, echo=False)

        insp = inspect(engine)
        with engine.connect() as conn:
            db_schema = "database_type:Oracle\n\n"
            for t in conn.execute(text(f"SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = '{username}'")):
                table_name = t[0]
                table_comment = cls.get_table_comment(table_name, conn)
                table_comment = f', comment: {table_comment}' if table_comment else ''
                db_schema += f"table:{table_name}{table_comment}\n"
                db_schema_human += "\n{" + f"'table': {table_name},\n'columns':["
                columns_human_str = ''

                for c in conn.execute(text(f"SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH FROM USER_TAB_COLUMNS "
                                           f"WHERE TABLE_NAME = '{table_name}'")):
                    column_name = c[0]
                    data_type = c[1]
                    data_length = c[2]
                    db_schema += f"({column_name}, {data_type}, {data_length})\n"
                    columns_human_str += f"'{column_name.strip()}',"

                db_schema_human += columns_human_str.rstrip(',') + ']},'

                primary_key_str = 'Primary Key:'
                p = insp.get_pk_constraint(table_name)
                if p.get('constrained_columns'):
                    primary_key_str += f"{p['constrained_columns']}"
                db_schema += f"{primary_key_str}\n"

                foreign_key_str = 'Foreign Keys:'
                for f in insp.get_foreign_keys(table_name):
                    foreign_key_str += f"\n({table_name}:{f['constrained_columns']} - {f['referred_table']}:{f['referred_columns']})"
                db_schema += f"{foreign_key_str}\n"

                db_schema += "\n"

        db_schema_human = db_schema_human.rstrip(',') + '\n]'
        app_log.logger().info(f"get_db_schema_imp:schema=\n{db_schema}\n{db_schema_human}")
        return {'db_schema': db_schema, 'db_schema_human': db_schema_human}

    @classmethod
    def get_connection_string(cls, username, password, ip_address, port_number, db_name, **kwargs):
        return f'oracle+cx_oracle://{username}:{password}@{ip_address}:{port_number}/{db_name}'

    @classmethod
    def get_table_comment(cls, table, conn):
        sql = f"SELECT COMMENTS FROM USER_TAB_COMMENTS WHERE TABLE_NAME = '{table}'"
        comments = conn.execute(text(sql))
        for c in comments:
            return c[0]

    @classmethod
    def get_username(cls, conn_string):
        username = conn_string.split('://')[1].split(':')[0]
        return username.upper()

