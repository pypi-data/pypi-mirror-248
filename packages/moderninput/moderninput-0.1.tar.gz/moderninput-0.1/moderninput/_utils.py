from typing import Callable


def return_self(method: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        method(self, *args, **kwargs)
        return self

    return wrapper


def bool_parse(value: str) -> bool:
    if value in ("1", "true", "y", "yes", "+"):
        return True
    
    elif value in ("0", "false", "n", "no", "-"):
        return False
