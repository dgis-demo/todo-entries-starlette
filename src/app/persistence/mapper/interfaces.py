from abc import ABCMeta, abstractmethod

from entities import TodoEntry
from value_objects import TodoLabel


class TodoEntryMapperInterface(metaclass=ABCMeta):
    @abstractmethod
    async def get(self, identifier: int) -> TodoEntry:
        """Return TodoEntry entity from persistence layer"""

    @abstractmethod
    async def create(self, entity: TodoEntry) -> TodoEntry:
        """Creates new TodoEntry in persistence layer"""

    @abstractmethod
    async def update(self, identifier: int, fields: dict) -> TodoEntry:
        """Updates a TodoEntry in persistence layer"""


class TodoLabelMapperInterface(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, value_object: TodoLabel) -> TodoLabel:
        """Creates new TodoLabel in persistence layer"""
