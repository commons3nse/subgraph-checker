from sqlalchemy import (
    Column,
    func,
)

from sqlalchemy.types import (
    Integer,
    DateTime,
    String,
    Boolean
)

from subgraph_bot.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    current_subgraph = Column(String, nullable=True)
    working = Column(Boolean, default=False, nullable=False)

    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __init__(self, id):
        self.id = id