from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from value_objects import TodoLabel


class AbstractEntity(BaseModel):
    id: Optional[int]


class TodoEntry(AbstractEntity):
    summary: str
    detail: Optional[str]
    created_at: datetime
    label: Optional[TodoLabel]
