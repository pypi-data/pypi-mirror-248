from ._base import InputBase

from re import fullmatch


def input_email(
    prompt: str | None,
    base: InputBase | None = None,
) -> str:
    if base is None:
        base = InputBase()

    base.set_checker(
        function=lambda x: fullmatch(pattern=r"[^@]+@[^@]+\.[^@]+", string=x)
        is not None
    )
    return base.invoke(prompt=prompt)
