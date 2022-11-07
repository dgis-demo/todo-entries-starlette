from typing import Optional

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from pydantic.dataclasses import dataclass

from apischema.schema import (
    todo_entry_creation_schema,
    todo_label_creation_schema,
)


@dataclass
class SchemaError:
    type: str
    message: str
    validation_schema: dict
    path: str


def _validation_error_to_structure(error: ValidationError) -> SchemaError:
    return SchemaError(
        message=error.message,
        validation_schema=error.schema,
        type="Validation error",
        path=".".join(error.absolute_path),
    )


def _validate(raw_data: dict, schema: dict) -> Optional[SchemaError]:
    try:
        validate(instance=raw_data, schema=schema)
    except ValidationError as err:
        return _validation_error_to_structure(error=err)


def validate_todo_entry(raw_data: dict) -> Optional[SchemaError]:
    return _validate(raw_data=raw_data, schema=todo_entry_creation_schema)


def validate_todo_label(raw_data: dict) -> Optional[SchemaError]:
    return _validate(raw_data=raw_data, schema=todo_label_creation_schema)
