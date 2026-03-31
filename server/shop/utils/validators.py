def clean_text(value):
    if not isinstance(value, str):
        return None

    value = value.strip()

    if not value:
        return None

    return value