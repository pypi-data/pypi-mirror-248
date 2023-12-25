from sqlalchemy import create_engine
from sqlalchemy import text
from app.app_log import app_log
from app.main.db_base import db_base

# requires 'pip install ibm_db_sa'
# not tested
class db2(db_base):
    @classmethod
    def get_schema(cls, db_connection_string):
        app_log.logger().info(f"db2/get_schema called")
        return "DB2 not yet supported"

    @classmethod
    def get_connection_string(cls, username, password, ip_address, port_number, db_name, **kwargs):
        str = f'db2+ibm_db://{username}:{password}@{ip_address}:{port_number}/{db_name}'
        return str

    @classmethod
    def _get_tables_query(cls, db_name):
        return f"""
SELECT TABNAME
FROM SYSCAT.TABLES
WHERE TABSCHEMA NOT LIKE 'SYS%'
  AND TABSCHEMA NOT LIKE 'SYSCAT%'
  AND TABSCHEMA NOT LIKE 'SYSIBM%'
  AND TABSCHEMA NOT LIKE 'SYSSTAT%'
  AND TABSCHEMA NOT LIKE 'SYSTOOLS%'
  AND TABSCHEMA NOT LIKE 'SYSTOOLSTMP%'
  AND TYPE = 'T'
  AND TABNAME NOT LIKE 'SQL%'
"""
        
    @classmethod
    def _get_columns_query(cls, table_name):
        return f"""
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE
FROM SYSIBM.COLUMNS
WHERE TABLE_NAME = '{table_name}'
"""
