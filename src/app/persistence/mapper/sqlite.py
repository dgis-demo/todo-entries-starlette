from sqlalchemy.orm import sessionmaker

from entities import TodoEntry
from persistence.mapper.errors import (
    CreateMapperError,
    EntityNotFoundMapperError, 
    UpdateMapperError,
)
from persistence.mapper.interfaces import (
    TodoEntryMapperInterface,
    TodoLabelMapperInterface,
)
from persistence.models import TodoEntryModel, TodoLabelModel
from value_objects import TodoLabel


class SqliteTodoEntryMapper(TodoEntryMapperInterface):
    _storage: sessionmaker

    def __init__(self, storage: sessionmaker) -> None:
        self._storage = storage

    async def get(self, identifier: int) -> TodoEntry:
        try:
            with self._storage() as session:
                todo_entry = session.get(
                    TodoEntryModel, 
                    ident=identifier,
                )

                if todo_entry is None:
                    raise AttributeError

                return TodoEntry.from_orm(todo_entry)
        except AttributeError:
            raise EntityNotFoundMapperError(f"Entity `id:{identifier}` was not found.")

    async def create(self, entity: TodoEntry) -> TodoEntry:
        try:
            with self._storage() as session:
                todo_entry = TodoEntryModel(
                    summary=entity.summary,
                    detail=entity.detail,
                    created_at=entity.created_at,
                )
                session.add(todo_entry)
                session.commit()
                return TodoEntry.from_orm(todo_entry)
        except TypeError as error:
            raise CreateMapperError(error)

    async def update(self, identifier: int, fields: dict) -> TodoEntry:
        try:
            with self._storage() as session:
                todo_entry = session.get(
                    TodoEntryModel, 
                    ident=identifier,
                )

                if todo_entry is None:
                    raise AttributeError

                label_id = fields.get("label_id")
                todo_label = session.get(
                    TodoLabelModel,
                    ident=label_id,
                )

                if todo_label is not None:
                    todo_entry.label_id = label_id

                session.commit()
                return TodoEntry.from_orm(todo_entry)
        except (TypeError, AttributeError) as error:
            raise UpdateMapperError(error)


class SqliteTodoLabelMapper(TodoLabelMapperInterface):
    _storage: sessionmaker

    def __init__(self, storage: sessionmaker) -> None:
        self._storage = storage

    async def create(self, value_object: TodoLabel) -> TodoLabel:
        try:
            with self._storage() as session:
                todo_label = TodoLabelModel(
                    name=value_object.name,
                )
                session.add(todo_label)
                session.commit()
                return TodoLabel.from_orm(todo_label)
        except TypeError as error:
            raise CreateMapperError(error)
