import sys
import time

import pandas as pd

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
def insert_data_to_db(query: str, db_name: str, params=None) -> bool:
    """
    Insert/update/delete data into the database with retry mechanism.

    :param query: SQL query to execute (INSERT/UPDATE/DELETE)
    :param db_name: Database name
    :param params: Optional parameters for parameterized query
    :return: True if successful, False if failed
    """
    db_connection_str = replacing_at_char_from_password(DATABASE_URL)

    for _ in range(config.RETRY_TIMES):
        try:
            db_connection = DB.get_connection(db_connection_str, db_name)

            with db_connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                db_connection.commit()  # commit the transaction

            return True

        except Exception as e:
            logger.info("Error: Cannot execute insert/update query")
            handle_exception("insert_data_to_db", sys.exc_info(), e)
            time.sleep(1)
            DB.reset_db_connection(db_connection_str, db_name)
            continue

    return False
