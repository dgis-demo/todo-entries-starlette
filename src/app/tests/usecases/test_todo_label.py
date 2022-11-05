import pytest

from entities import TodoLabel
from persistence.mapper.memory import MemoryTodoLabelMapper
from persistence.repository import TodoLabelRepository
from usecases import (
    create_todo_label, 
    UseCaseError,
)


@pytest.mark.asyncio
async def test_create_todo_entry() -> None:
    mapper = MemoryTodoLabelMapper(storage={})
    repository = TodoLabelRepository(mapper=mapper)

    data = TodoLabel(name="Lorem Ipsum")
    value_object = await create_todo_label(value_object=data, repository=repository)

    assert isinstance(value_object, TodoLabel)


@pytest.mark.asyncio
async def test_todo_entry_creation_error() -> None:
    mapper = MemoryTodoLabelMapper(storage=None)
    repository = TodoLabelRepository(mapper=mapper)

    data = TodoLabel(name="Lorem Ipsum")
    with pytest.raises(UseCaseError):
        await create_todo_label(value_object=data, repository=repository)
