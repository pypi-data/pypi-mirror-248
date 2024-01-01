from ._base import InputBase


def input_choice(
    prompt: str | None,
    choices: list,
    base: InputBase | None = None,
) -> str:
    if base is None:
        base = InputBase()

    base.set_checker(function=lambda x: x in choices)
    return base.invoke(prompt=prompt)
