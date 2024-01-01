from ._typecheck import type_check
from ._utils import return_self

from typing import Callable
from typing import Any


class InputBase:
    def __init__(self) -> None:
        self.__checker = None
        self.__invalid = None
        self.__valid = None
        self.__interrupt = None
        self.__do_ireturn = None
        self.__ireturn = None

    @return_self
    def set_checker(self, function: Callable) -> "InputBase":
        self.__checker = type_check(
            value=function, name="function", types=Callable | None
        )

    @return_self
    def set_invalid_handler(self, function: Callable | None) -> "InputBase":
        self.__invalid = type_check(
            value=function, name="function", types=Callable | None
        )

    @return_self
    def set_valid_handler(self, function: Callable | None) -> "InputBase":
        self.__valid = type_check(
            value=function, name="function", types=Callable | None
        )

    @return_self
    def set_interrupt_handler(
        self,
        function: Callable | None,
        do_ireturn: bool | None = None,
        ireturn: Any | None = None,
    ) -> "InputBase":
        self.__interrupt = type_check(
            value=function, name="function", types=Callable | None
        )
        self.__do_ireturn = type_check(
            value=do_ireturn, name="do_ireturn", types=bool | None
        )
        self.__ireturn = type_check(value=ireturn, name="ireturn", types=Any | None)

        if (do_ireturn is None or do_ireturn is False) and ireturn is not None:
            raise ValueError("do_ireturn must be True for set ireturn")

    def invoke(self, prompt: str | None) -> str:
        type_check(value=prompt, name="prompt", types=str | None)

        while True:
            try:
                value = input(prompt)

            except KeyboardInterrupt:
                if self.__interrupt is not None:
                    self.__interrupt()

                if self.__do_ireturn is True:
                    return self.__ireturn

            if self.__checker is not None and self.__checker(value) is False:
                if self.__invalid is not None:
                    self.__invalid(value)

                continue

            if self.__valid is not None:
                self.__valid(value)

            break

        return value
