from json import loads
import uuid

from pydantic import BaseModel
import pytest

from apischema.encoder import (
    error_to_json,
    base_model_to_json,
    encode_to_json_response,
    encode_error_to_json_response,
)
from apischema.validator import SchemaError
from entities import AbstractEntity
from value_objects import AbstractValueObject


def test_error_to_json() -> None:
    error = SchemaError(
        type="Validation Error",
        message="Something is wrong",
        validation_schema={"maxlength": 16, "type": "string"},
        path="some.path.in.json",
    )
    json = error_to_json(error=error)
    assert isinstance(json, str)

    data = loads(json)

    assert "type" in data
    assert "message" in data
    assert "validation_schema" in data
    assert "path" in data


@pytest.mark.parametrize(
    "base_model",
    [
        AbstractEntity(id=1),
        AbstractValueObject(id=uuid.uuid4()),
    ]
)
def test_base_model_to_json(base_model: BaseModel) -> None:
    json = base_model_to_json(data=base_model)
    assert isinstance(json, str)

    data = loads(json)

    assert "id" in data


@pytest.mark.parametrize(
    "base_model",
    [
        AbstractEntity(id=42),
        AbstractValueObject(id=uuid.uuid4()),
    ]
)
def test_encode_to_json_response(base_model: BaseModel) -> None:
    data = encode_to_json_response(data=base_model)

    assert isinstance(data, bytes)


def test_encode_error_to_json_response() -> None:
    error = SchemaError(
        type="Error",
        message="Something is wrong",
        validation_schema={"type": "string"},
        path="property",
    )
    data = encode_error_to_json_response(error=error)

    assert isinstance(data, bytes)
