"""database model to manage task"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base_model import BaseModel
from .connector import Base


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
