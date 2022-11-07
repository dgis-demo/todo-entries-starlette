todo_entry_creation_schema = {
    "type": "object",
    "required": ["summary", "created_at"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "summary": {"type": "string", "minLength": 3, "maxLength": 26},
        "detail": {"type": "string", "maxLength": 255},
        "created_at": {"type": "string", "format": "date-time"},
    },
}

todo_label_creation_schema = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "string", "minLength": 3, "maxLength": 26},
    },
}
