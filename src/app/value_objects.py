from typing import Optional
import uuid

from pydantic import BaseModel


class AbstractValueObject(BaseModel):
    id: Optional[uuid.UUID]


class TodoLabel(AbstractValueObject):
    name: str
