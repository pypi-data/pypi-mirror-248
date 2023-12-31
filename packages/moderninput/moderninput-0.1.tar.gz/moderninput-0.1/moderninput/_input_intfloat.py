from ._base import InputBase


def is_intfloat(value: str) -> bool:
    try:
        float(value)
        return True

    except ValueError:
        return False


def input_intfloat(
    prompt: str | None,
    minimal: int | None = None,
    maximal: int | None = None,
    base: InputBase | None = None,
) -> float:
    if base is None:
        base = InputBase()

    base.set_checker(
        function=lambda x: is_intfloat(value=x)
        and (minimal if minimal is not None else float("-inf"))
        <= float(x)
        <= (maximal if maximal is not None else float("+inf"))
    )
    return float(base.invoke(prompt=prompt))
