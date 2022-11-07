from typing import Optional

from pydantic import BaseModel


class AbstractValueObject(BaseModel):
    id: Optional[int]


class TodoLabel(AbstractValueObject):
    name: str
