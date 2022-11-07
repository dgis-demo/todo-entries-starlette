from entities import TodoEntry
from persistence.errors import (
    EntityNotFoundError, 
    CreateError,
    UpdateError,
)
from persistence.mapper.errors import (
    EntityNotFoundMapperError, 
    CreateMapperError,
    UpdateMapperError,
)
from persistence.mapper.interfaces import (
    TodoEntryMapperInterface,
    TodoLabelMapperInterface,
)
from value_objects import TodoLabel


class TodoEntryRepository:
    _mapper: TodoEntryMapperInterface

    def __init__(self, mapper: TodoEntryMapperInterface) -> None:
        self._mapper = mapper

    async def get(self, identifier: int) -> TodoEntry:
        try:
            return await self._mapper.get(identifier=identifier)
        except EntityNotFoundMapperError as error:
            raise EntityNotFoundError(error)

    async def create(self, entity: TodoEntry) -> TodoEntry:
        try:
            return await self._mapper.create(entity=entity)
        except CreateMapperError as error:
            raise CreateError(error)

    async def update(self, identifier: int, fields: dict) -> TodoEntry:
        try:
            return await self._mapper.update(
                identifier=identifier,
                fields=fields,
            )
        except UpdateMapperError as error:
            raise UpdateError(error)


class TodoLabelRepository:
    _mapper: TodoLabelMapperInterface

    def __init__(self, mapper: TodoLabelMapperInterface) -> None:
        self._mapper = mapper

    async def create(self, value_object: TodoLabel) -> TodoLabel:
        try:
            return await self._mapper.create(value_object=value_object)
        except CreateMapperError as error:
            raise CreateError(error)
