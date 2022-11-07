from datetime import datetime, timezone

import pytest

from entities import TodoEntry
from persistence.errors import (
    EntityNotFoundError, 
    CreateError,
    UpdateError,
)
from persistence.mapper.memory import (
    MemoryTodoEntryMapper,
    MemoryTodoLabelMapper,
)
from persistence.repository import (
    TodoEntryRepository,
    TodoLabelRepository,
)
from value_objects import TodoLabel

_memory_storage = {
    1: TodoEntry(id=1, summary="Lorem Ipsum", created_at=datetime.now(tz=timezone.utc)),
    10_001: TodoLabel(id=10_001, name="Lorem"),
}


@pytest.mark.asyncio
async def test_get_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=_memory_storage)
    repository = TodoEntryRepository(mapper=mapper)

    entity = await repository.get(identifier=1)
    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_not_found_error() -> None:
    mapper = MemoryTodoEntryMapper(storage=_memory_storage)
    repository = TodoEntryRepository(mapper=mapper)

    with pytest.raises(EntityNotFoundError):
        await repository.get(identifier=42)


@pytest.mark.asyncio
async def test_save_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=_memory_storage)
    repository = TodoEntryRepository(mapper=mapper)

    data = TodoEntry(
        summary="Buy flowers to my wife",
        detail="We have marriage anniversary",
        created_at=datetime.now(tz=timezone.utc),
    )

    entity = await repository.create(entity=data)
    assert isinstance(entity, TodoEntry)
    assert entity.id > 1


@pytest.mark.asyncio
async def test_todo_entry_create_error() -> None:
    mapper = MemoryTodoEntryMapper(storage=None)
    repository = TodoEntryRepository(mapper=mapper)

    data = TodoEntry(
        summary="Lorem Ipsum",
        detail=None,
        created_at=datetime.now(tz=timezone.utc),
    )

    with pytest.raises(CreateError):
        await repository.create(entity=data)


@pytest.mark.asyncio
async def test_save_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=_memory_storage)
    repository = TodoEntryRepository(mapper=mapper)
    identifier = 1
    fields = {"label_id": 10_001}

    entity = await repository.update(
        identifier=identifier,
        fields=fields,
    )
    assert isinstance(entity, TodoEntry)
    assert entity.id == identifier
    assert entity.label.id == 10_001


@pytest.mark.asyncio
async def test_todo_entry_update_error() -> None:
    mapper = MemoryTodoEntryMapper(storage=None)
    repository = TodoEntryRepository(mapper=mapper)
    identifier = 1
    fields = {"label_id": 10_001}

    with pytest.raises(UpdateError):
        await repository.update(
            identifier=identifier,
            fields=fields,
        )


@pytest.mark.asyncio
async def test_save_todo_label() -> None:
    mapper = MemoryTodoLabelMapper(storage=_memory_storage)
    repository = TodoLabelRepository(mapper=mapper)
    name = "Lorem Ipsum"

    data = TodoLabel(
        name=name,
    )

    value_object = await repository.create(value_object=data)
    assert isinstance(value_object, TodoLabel)
    assert value_object.name == name


@pytest.mark.asyncio
async def test_todo_label_create_error() -> None:
    mapper = MemoryTodoLabelMapper(storage=None)
    repository = TodoLabelRepository(mapper=mapper)

    data = TodoLabel(
        name="Lorem Ipsum",
    )

    with pytest.raises(CreateError):
        await repository.create(value_object=data)
