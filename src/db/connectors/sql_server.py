import pyodbc
import threading
from queue import Queue
from threading import Semaphore

from sqlalchemy import create_engine, QueuePool

from src.utils.logger import LOGGER

pyodbc.pooling = False


class SQLServerConnectorPool:
    def __init__(self, dns, max_conn, min_conn):
        self.dns = dns
        self.max_conn = max_conn
        self.min_conn = min_conn
        self.engine = create_engine(
            # DNS,
            "mssql+pyodbc://",
            poolclass=QueuePool,
            pool_pre_ping=True,
            pool_size=self.max_conn - self.min_conn,
            max_overflow=self.min_conn,
            pool_timeout=60 * 60,
            creator=self.__get_conn__,
            fast_executemany=True,
        )
        try:
            session = self.get()
            self.put(session)
            LOGGER.info("Successfully create connection...")
        except Exception as e:
            LOGGER.error(f"Could not create connection to {dns}", e)
            pass

    def __get_conn__(self):
        c = pyodbc.connect(self.dns)
        return c

    def get(self):
        return self.engine.connect()

    @classmethod
    def put(cls, session):
        session.close()
