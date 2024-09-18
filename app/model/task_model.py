"""database model to manage task"""


import enum

from sqlalchemy import Column, String, ForeignKey, Integer, Enum

from sqlalchemy.dialects.postgresql import UUID

from .base_model import BaseModel
from .connector import Base


class RelationType(enum.Enum):
    """get relation type

    Args:
        enum (_type_): enum type
    """

    COMPOSE = "组成"
    PREREQUISITES = "前提"


class TaskModel(BaseModel, Base):
    """Task Manager database model

    Args:
        BaseModel (_type_): Base database model
    """

    __tablename__ = "Task"

    name = Column(String(), nullable=False, unique=True, comment="task name")

    parent_task_id = Column(
        UUID(),
        ForeignKey("Task.id", ondelete="CASCADE"),
        default=None,
        comment="parent task id",
    )

    relation_type = Column(Enum(), comment="relations between the task and parent task")

    order = Column(Integer(), default=0, comment="task order start from 0")
