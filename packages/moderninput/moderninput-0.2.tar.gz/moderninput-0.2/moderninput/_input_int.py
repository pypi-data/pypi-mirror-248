from ._base import InputBase


def is_int(value: str) -> bool:
    try:
        int(value)
        return True

    except ValueError:
        return False


def input_int(
    prompt: str | None,
    minimal: int | None = None,
    maximal: int | None = None,
    base: InputBase | None = None,
) -> int:
    if base is None:
        base = InputBase()

    base.set_checker(
        function=lambda x: is_int(value=x)
        and (minimal if minimal is not None else float("-inf"))
        <= int(x)
        <= (maximal if maximal is not None else float("+inf"))
    )
    return int(base.invoke(prompt=prompt))
