from apischema.validator import (
    validate_todo_entry_creation,
    validate_todo_label,
)


def test_short_summary_in_todo_entry() -> None:
    data = {
        "summary": "Lo",
        "detail": "",
        "created_at": "2022-09-05T18:07:19.280040+00:00",
    }

    error = validate_todo_entry_creation(raw_data=data)
    assert error.path == "summary"
    assert "maxLength" in error.validation_schema
    assert "minLength" in error.validation_schema
    assert "type" in error.validation_schema


def test_short_label_in_todo_label() -> None:
    data = {
        "name": "Lo",
    }

    error = validate_todo_label(raw_data=data)
    assert error.path == "name"
    assert "maxLength" in error.validation_schema
    assert "minLength" in error.validation_schema
    assert "type" in error.validation_schema
