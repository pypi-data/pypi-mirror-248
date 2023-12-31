from ._base import InputBase

from os.path import isdir


def input_dir(
    prompt: str | None,
    base: InputBase | None = None,
) -> str:
    if base is None:
        base = InputBase()

    base.set_checker(function=lambda x: isdir(s=x))
    return base.invoke(prompt=prompt)
