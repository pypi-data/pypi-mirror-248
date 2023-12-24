import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from boobs.api import ABCAPI
    from boobs.bot.dispatch.view.abc import ABCView
    from boobs.bot.states.dispenser.abc import ABCStateDispenser
    from boobs.errors import ABCErrorHandler
    from boobs.types.objects import Update


class ABCRouter(ABC):
    views: dict[str, "ABCView"]
    state_dispenser: "ABCStateDispenser"
    error_handler: "ABCErrorHandler"

    @abstractmethod
    async def route(self, update: "Update", api: "ABCAPI") -> typing.Any:
        """
        Routes updates to their corresponding views
        """
