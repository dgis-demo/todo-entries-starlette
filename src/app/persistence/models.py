from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class TodoEntryModel(Base):
    __tablename__ = "todo_entries"

    id = Column(Integer, primary_key=True)
    summary = Column(String(length=26), nullable=False)
    detail = Column(String(length=255))
    created_at = Column(DateTime, default=datetime.utcnow)
    label_id = Column(Integer, ForeignKey(
        "todo_labels.id", 
        ondelete="CASCADE",
    ))

    def __repr__(self) -> str:
        return f"""{self.__name__}(
            id={self.id},
            summary={self.summary},
            detail={self.detail},
            created_at={self.created_at},
            label={self.label.name},
        )
        """


class TodoLabelModel(Base):
    __tablename__ = "todo_labels"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=26), nullable=False)
    todo_entries = relationship(
        "TodoEntryModel", 
        backref="label",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"""{self.__name__}(
            id={self.id},
            name={self.name},
        )
        """
