from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from boobs.bot.abc import ABCFramework

if TYPE_CHECKING:
    from boobs.api import ABCAPI
    from boobs.bot.dispatch.dispatcher import ABCDispatcher
    from boobs.bot.states import ABCStateDispenser


class ABCNipple(ABCFramework):
    api: "ABCAPI"
    dispatcher: "ABCDispatcher"
    state_dispenser: "ABCStateDispenser"

    @abstractmethod
    def load_into(self, framework: Any) -> "ABCNipple":
        pass

    def run_forever(self) -> None:
        raise NotImplementedError("Running polling from nipples is not implemented")
