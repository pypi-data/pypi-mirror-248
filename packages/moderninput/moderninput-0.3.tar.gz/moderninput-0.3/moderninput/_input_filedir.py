from ._base import InputBase

from os.path import isdir
from os.path import isfile


def input_filedir(
    prompt: str | None,
    base: InputBase | None = None,
) -> str:
    if base is None:
        base = InputBase()

    base.set_checker(function=lambda x: isdir(s=x) or isfile(path=x))
    return base.invoke(prompt=prompt)
