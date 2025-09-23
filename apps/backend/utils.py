import sys
import time
from typing import Tuple, Any, Union
import pandas as pd
from sqlalchemy import text
import config
from config import DATABASE_URL
from db_connection import DB
from handle_exception import handle_exception
from logger_file import logger


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


# TODO : Need to update the insertion logic as this is very old one
def insert_data_to_db(query: str, db_name: str, params=None) -> Tuple[bool, Any]:
    db_connection_str = replacing_at_char_from_password(DATABASE_URL)
      # returns Engine
    auto_id = config.INVALID_LOG_ID
    qry_status = False
    for _ in range(config.RETRY_TIMES):
        try:
            db_conn = DB.get_connection(db_connection_str, db_name)
            with db_conn.begin() as connection:
                result = connection.execute(text(query), params or {})
                auto_id = result.lastrowid

            qry_status = True
            break

        except Exception as e:
            logger.info("Error: Cannot execute insert/update query")
            handle_exception("insert_data_to_db", sys.exc_info(), e)
            time.sleep(1)
            DB.reset_db_connection(db_connection_str, db_name)
            continue

    return qry_status, auto_id

