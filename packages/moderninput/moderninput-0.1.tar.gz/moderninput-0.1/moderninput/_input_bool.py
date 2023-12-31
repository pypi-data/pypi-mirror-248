from ._base import InputBase
from ._utils import bool_parse


def input_bool(
    prompt: str | None,
    base: InputBase | None = None,
) -> bool:
    if base is None:
        base = InputBase()

    base.set_checker(
        function=lambda x: x.lower().strip()
        in ("1", "true", "y", "yes", "+", "0", "false", "n", "no", "-")
    )

    return bool_parse(value=base.invoke(prompt=prompt))
