def clean_text(value):
    if not isinstance(value, str):
        return None

    value = value.strip()

    if not value:
        return None

    return value

def parse_bool(value, default=False):
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    return None

def parse_rating(value):
    if isinstance(value, bool):
        return None

    if isinstance(value, float):
        return None

    try:
        value = int(value)
    except (TypeError, ValueError):
        return None

    if value < 1 or value > 5:
        return None

    return value