from sqlalchemy import create_engine
from sqlalchemy import text
from app.app_log import app_log
from app.main.db_base import db_base

# requires pip install psycopg2
# not tested
class postgresql(db_base):
    @classmethod
    def get_schema(cls, db_connection_string):
        # app_log.logger().info(f"postgresql/get_schema called")
        # return "Postgresql not yet supported"
        return db_base.get_schema(db_connection_string)
        
    @classmethod
    def get_connection_string(cls, username, password, ip_address, port_number, db_name, **kwargs):
        str = f'postgresql://{username}:{password}@{ip_address}:{port_number}/{db_name}'
        return str        

    @classmethod
    def _get_tables_query(cls, db_name):
        return f"""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '{db_name}'
  AND table_type = 'BASE TABLE'
  AND table_name NOT LIKE 'pg_%'
  AND table_name NOT LIKE 'sql_%'
"""
        
    @classmethod
    def _get_columns_query(cls, table_name):
        return f"""
SELECT column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_name = '{table_name}'
"""
