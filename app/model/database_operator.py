from app.configs import LoggerOperation

from datetime import datetime
import uuid
from uuid import UUID
from typing import Optional, Union
from .task_model import TaskModel  # noqa
from .task_operator import add_task_root
from .connector import Base, engine

# 需要注意的是必须在这里增加对应的模型，否则对应的数据模型无法加载
logger = LoggerOperation().get_logger("database")


class DatabaseOperator:
    """对于数据库的整体操作，创建数据库，删除数据库"""

    def create_database(self):
        """创建数据库"""
        logger.info("开始创建数据库")
        Base.metadata.create_all(bind=engine)

        # 创建任务根节点
        try:
            logger.info("创建初始任务根节点")
            add_task_root()
        except Exception as e:
            logger.info("任务根节点已经存在")

        logger.info("创建数据库完成")

    def drop_database(self):
        """删除数据库"""
        logger.info("开始创建数据库")
        Base.metadata.drop_all(bind=engine)
        logger.info("创建数据库完成")


def trans_str2uuid(uuid_obj: Union[str | UUID | None]) -> UUID:
    """检测UUID格式，如果是字符串，将转换为UUID对象

    Args:
        uuid_obj (Optional[str  |  UUID]): 待转换的UUID

    Returns:
        UUID: UUID对象
    """
    logger.info("对uuid进行操作:%s", uuid_obj)
    try:
        if isinstance(uuid_obj, str):
            uuid_obj = uuid.UUID(uuid_obj)
    except Exception as e:
        uuid_obj = None

    return uuid_obj


def trans_datetime2str(time: Union[datetime | str]):
    """将datetime格式数据转换为str格式数据

    Args:
        time (datetime): datetime格式数据
    """

    if isinstance(time, str):
        return time
    elif isinstance(time, datetime):
        formatted_date = time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date
