# 下面是对session的装饰

from contextlib import contextmanager

from sqlalchemy.orm import Session

from .connector import SessionLocal

from functools import wraps

from app.configs import LoggerOperation

logger = LoggerOperation().get_logger("database")


@contextmanager
def session_scope() -> Session:
    """
    用于获取session

    Returns:

    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error("操作数据库出错:%s", e)
        session.rollback()
        raise
    finally:
        session.close()


def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            # 移除了提交和回滚的逻辑
            return f(session, *args, **kwargs)

    return wrapper


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
