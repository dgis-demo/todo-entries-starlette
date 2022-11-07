from random import randint
import uuid

from entities import TodoEntry
from persistence.mapper.errors import EntityNotFoundMapperError, CreateMapperError
from persistence.mapper.interfaces import (
    TodoEntryMapperInterface,
    TodoLabelMapperInterface,
)
from value_objects import TodoLabel


class MemoryTodoEntryMapper(TodoEntryMapperInterface):
    _storage: dict

    def __init__(self, storage: dict) -> None:
        self._storage = storage

    async def get(self, identifier: int) -> TodoEntry:
        try:
            return self._storage[identifier]
        except KeyError:
            raise EntityNotFoundMapperError(f"Entity `id:{identifier}` was not found.")

    async def create(self, entity: TodoEntry) -> TodoEntry:
        try:
            entity.id = self._generate_unique_id()
            self._storage[entity.id] = entity
            return entity
        except TypeError as error:
            raise CreateMapperError(error)

    def _generate_unique_id(self) -> int:
        identifier = randint(1, 10_000)
        while identifier in self._storage:
            identifier = randint(1, 10_000)

        return identifier


class MemoryTodoLabelMapper(TodoLabelMapperInterface):
    _storage: dict

    def __init__(self, storage: dict) -> None:
        self._storage = storage

    async def create(self, value_object: TodoLabel) -> TodoLabel:
        try:
            value_object.id = uuid.uuid4()
            self._storage[value_object.id] = value_object
            return value_object
        except TypeError as error:
            raise CreateMapperError(error)
