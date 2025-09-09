import threading

class DbConnection:

    def __init__(self):
        self.thread_local = threading.local()

    def get_connection(self, conn_string: str, db: str):
        connection_pool = getattr(self.thread_local, 'connection_pool', None)
        connection_string = conn_string + "_" + db
        if connection_string in connection_pool and connection_pool[connection_string] is not None:
            return connection_pool[connection_string]
        else:
            rconn = self.reset_db_connection(conn_string, db)
            return rconn

    def reset_db_connection(self, conn_string: str, db: str):
        connection = None
        connection_string = conn_string + "_" + db
        connection_pool = getattr(self.thread_local, 'connection_pool', None)
