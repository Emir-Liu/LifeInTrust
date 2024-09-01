from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.configs import DATABASE_URL, BOOL_ECHO, LoggerOperation

logger = LoggerOperation().get_logger("database")

# 构建engine
engine = create_engine(DATABASE_URL, echo=BOOL_ECHO)

# 建立session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


# 需要注意sqlite数据库，需要显式设置外键约束
# https://segmentfault.com/a/1190000045109095
# import re
# import sqlite3
# from sqlalchemy import Engine, event


# def is_sqlite(db_uri):
#     """检查数据库 URI 是否为 SQLite"""
#     return bool(re.match(r"sqlite:///", db_uri))


# # 每次建立新连接时执行 set_sqlite_pragma（仅在使用 SQLite 时）
# if is_sqlite(DATABASE_URL):

#     @event.listens_for(Engine, "connect")
#     def set_sqlite_pragma(dbapi_connection: sqlite3.Connection, _):
#         """启用 SQLite 的外键约束"""
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON")
#         cursor.close()
