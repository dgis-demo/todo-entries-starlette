todo_entry_creation_schema = {
    "type": "object",
    "required": ["summary", "created_at"],
    "properties": {
        "id": {"type": "integer", "minimum": 1, "maximum": 10_000},
        "summary": {"type": "string", "minLength": 3, "maxLength": 26},
        "detail": {"type": "string", "maxLength": 255},
        "created_at": {"type": "string", "format": "date-time"},
    },
}

todo_entry_updating_schema = {
    "type": "object",
    "required": [],
    "properties": {
        "label_id": {"type": "integer", "minimum": 10_001, "maximum": 20_000},
    },
}

todo_label_creation_schema = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "string", "minLength": 3, "maxLength": 26},
    },
}
