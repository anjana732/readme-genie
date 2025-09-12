import sys
import threading
from sqlalchemy import create_engine
from handle_exception import handle_exception

class DbConnection:
    def __init__(self):
        self.thread_local = threading.local()

    def get_connection(self, conn_string: str, db: str = ""):
        if not hasattr(self.thread_local, 'connection_pool'):
            self.thread_local.connection_pool = {}

        connection_pool = self.thread_local.connection_pool
        connection_string = conn_string + "_" + db

        try:
            if connection_string in connection_pool and connection_pool[connection_string] is not None:
                return connection_pool[connection_string]
            else:
                return self.reset_db_connection(conn_string, db)
        except Exception as e:
            handle_exception("get_connection", sys.exc_info(), e)

    def reset_db_connection(self, conn_string: str, db: str):
        if not hasattr(self.thread_local, 'connection_pool'):
            self.thread_local.connection_pool = {}

        connection_pool = self.thread_local.connection_pool
        connection_string = conn_string + "_" + db

        try:
            if connection_string in connection_pool and connection_pool[connection_string] is not None:
                connection_pool[connection_string].dispose()
        except Exception as e:
            handle_exception("reset_db_connection", sys.exc_info(), e)

        connection = None
        for _ in range(3):
            try:
                connection = create_engine(conn_string)
                break
            except Exception as e:
                handle_exception("reset_db_connection", sys.exc_info(), e)
                connection = None
                continue

        if connection is not None:
            connection_pool[connection_string] = connection

        return connection


DB = DbConnection()