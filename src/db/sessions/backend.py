import os
import threading
from contextlib import contextmanager
from typing import ContextManager

from flask import session as flask_session
from sqlalchemy.orm import Session

from src.db.connectors import SQLServerConnectorPool
from src.utils.logger import LOGGER

PREFIX = "BACKEND"
LOCAL_SESSION = {}
DNS = os.environ.get(f"{PREFIX}_DNS", None)
MIN_CONN = 2
MAX_CONN = 4

POOL = SQLServerConnectorPool(dns=DNS, max_conn=MAX_CONN, min_conn=MIN_CONN)


def get_unique_thread_key():
    thread_id = threading.get_ident()
    process_id = os.getpid()
    unique_thread_key = str(process_id) + "-" + str(thread_id)
    return unique_thread_key


def set_session(session):
    try:
        flask_session[f"{PREFIX}_SESSION"] = session
    except:
        global LOCAL_SESSION
        if session is None:
            try:
                LOCAL_SESSION.pop(get_unique_thread_key())
            except:
                pass
        else:
            LOCAL_SESSION[get_unique_thread_key()] = session


def get_session():
    try:
        return flask_session[f"{PREFIX}_SESSION"]
    except:
        global LOCAL_SESSION
        return LOCAL_SESSION.get(get_unique_thread_key(), None)


@contextmanager
def backend_session_scope() -> ContextManager[Session]:
    """
    Provide a transactional scope around a series of operations.
    Shouldn't keep session alive too long, it will block a connection of pool connections.
    """
    session: Session
    reuse_session = get_session()
    if reuse_session is None:
        session = POOL.get()
        set_session(session=session)
    else:
        session = reuse_session
    try:
        yield session
        if reuse_session is None:
            session.commit()
    except Exception as exception:
        LOGGER.error(exception, exc_info=True)
        if reuse_session is None:
            session.rollback()
        raise exception
    finally:
        if reuse_session is None:
            POOL.put(session)
            set_session(session=None)
