from ._base import InputBase


def input_length(
    prompt: str | None,
    minimal_length: int | None,
    maximal_length: int | None,
    base: InputBase | None = None,
) -> str:
    if base is None:
        base = InputBase()

    base.set_checker(
        function=lambda x: (
            minimal_length if minimal_length is not None else float("-inf")
        )
        <= len(x)
        <= (maximal_length if maximal_length is not None else float("+inf"))
    )
    return base.invoke(prompt=prompt)
