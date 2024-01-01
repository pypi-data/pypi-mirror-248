from ._base import InputBase


def is_ipv4(value: str) -> bool:
    parts = value.split(".")

    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False

        if not (0 <= int(part) <= 255):
            return False

    return True


def input_ipv4(
    prompt: str | None,
    base: InputBase | None = None,
) -> int:
    if base is None:
        base = InputBase()

    base.set_checker(function=lambda x: is_ipv4(value=x))
    return base.invoke(prompt=prompt)
