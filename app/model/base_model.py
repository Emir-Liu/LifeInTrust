import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID


class BaseModel:
    """
    基础模型
    """

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)

    create_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="创建时间"
    )
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )

    create_by = Column(String, default=None, comment="创建者")
    update_by = Column(String, default=None, comment="更新者")
