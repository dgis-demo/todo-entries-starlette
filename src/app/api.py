from datetime import datetime, timezone
from http import HTTPStatus

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from apischema.encoder import encode_to_json_response, encode_error_to_json_response
from apischema.validator import (
    validate_todo_entry,
    validate_todo_label,
)
from entities import TodoEntry
from persistence.mapper.memory import (
    MemoryTodoEntryMapper,
    MemoryTodoLabelMapper,
)
from persistence.repository import (
    TodoEntryRepository,
    TodoLabelRepository,
)
from value_objects import TodoLabel

from usecases import (
    get_todo_entry, 
    create_todo_entry, 
    create_todo_label,
    UseCaseError, 
    NotFoundError,
)

_MAPPER_IN_MEMORY_STORAGE = {
    1: TodoEntry(id=1, summary="Lorem Ipsum", created_at=datetime.now(tz=timezone.utc))
}


async def get_todo(request: Request) -> Response:
    """
    summary: Finds TodoEntry by id
    parameters:
        - name: id
          in: path
          description: TodoEntry id
          required: true
          schema:
            type: integer
            format: int64
    responses:
        "200":
            description: Object was found.
            examples:
                {"id": 1, "summary": "Lorem Ipsum", "detail": null, "created_at": "2022-09-27T17:29:06.183775+00:00"}
        "404":
            description: Object was not found
    """
    try:
        identifier = request.path_params["id"]  # TODO: add validation

        mapper = MemoryTodoEntryMapper(storage=_MAPPER_IN_MEMORY_STORAGE)
        repository = TodoEntryRepository(mapper=mapper)

        entity = await get_todo_entry(identifier=identifier, repository=repository)
        content = encode_to_json_response(data=entity)

    except NotFoundError:
        return Response(
            content=None,
            status_code=HTTPStatus.NOT_FOUND,
            media_type="application/json",
        )

    return Response(content=content, media_type="application/json")


async def create_new_todo_entry(request: Request) -> Response:
    """
    summary: Creates new TodoEntry
    responses:
        "201":
            description: TodoEntry was created.
            examples:
                {"summary": "Lorem Ipsum", "detail": null, "created_at": "2022-09-05T18:07:19.280040+00:00"}
        "422":
            description: Validation error.
        "500":
            description: Something went wrong, try again later.
    """
    data = await request.json()
    errors = validate_todo_entry(raw_data=data)
    if errors:
        return Response(
            content=encode_error_to_json_response(error=errors),
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            media_type="application/json",
        )

    mapper = MemoryTodoEntryMapper(storage=_MAPPER_IN_MEMORY_STORAGE)
    repository = TodoEntryRepository(mapper=mapper)

    try:
        entity = TodoEntry(**data)
        entity = await create_todo_entry(entity=entity, repository=repository)
        content = encode_to_json_response(data=entity)
    except UseCaseError:
        return Response(
            content=None,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            media_type="application/json",
        )

    return Response(
        content=content, status_code=HTTPStatus.CREATED, media_type="application/json"
    )


async def create_new_todo_label(request: Request) -> Response:
    """
    summary: Creates new TodoLabel
    responses:
        "201":
            description: TodoLabel was created.
            examples:
                {"todo_id": 1, "label": "Lorem ipsum"}
        "422":
            description: Validation error.
        "500":
            description: Something went wrong, try again later.
    """
    data = await request.json()
    errors = validate_todo_label(raw_data=data)
    if errors:
        return Response(
            content=encode_error_to_json_response(error=errors),
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            media_type="application/json",
        )

    mapper = MemoryTodoLabelMapper(storage=_MAPPER_IN_MEMORY_STORAGE)
    repository = TodoLabelRepository(mapper=mapper)

    try:
        value_object = TodoLabel(**data)
        value_object = await create_todo_label(
            value_object=value_object, 
            repository=repository,
        )
        content = encode_to_json_response(data=value_object)
    except UseCaseError:
        return Response(
            content=None,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            media_type="application/json",
        )

    return Response(
        content=content, status_code=HTTPStatus.CREATED, media_type="application/json"
    )

app = Starlette(
    debug=True,
    routes=[
        Route("/todo/", create_new_todo_entry, methods=["POST"]),
        Route("/todo/{id:int}/", get_todo, methods=["GET"]),
        Route("/label/", create_new_todo_label, methods=["POST"]),
    ],
)
