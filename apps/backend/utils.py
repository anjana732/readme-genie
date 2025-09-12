import os
import sys
import time
import pandas as pd
import config
from db_connection import DB
from handle_exception import handle_exception
from logger_file import logger
from dotenv import load_dotenv
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "readme_backend")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
def replacing_at_char_from_password(connection_str):
    return connection_str.split('@', 1)[0].replace('@', '%40') + '@' + connection_str.split('@', 1)[1]


def get_data_from_db(query: str, db_name: str, params=None):
    df = None
    db_connection_str = replacing_at_char_from_password(DATABASE_URL)
    for _ in range(config.RETRY_TIMES):
        try:
            db_connection = DB.get_connection(db_connection_str, db_name)
            df = pd.read_sql_query(query, db_connection, params=params)

            return True, df
        except Exception as e:
            logger.info("Error : Cannot connect to sql")
            handle_exception("get_data_from_db", sys.exc_info(), e)
            time.sleep(1)
            DB.reset_db_connection(db_connection_str, db_name)
            continue

    return False, df
