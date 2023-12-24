from abc import ABC, abstractmethod

from boobs.api import ABCAPI
from boobs.bot.dispatch.dispatcher import ABCDispatcher, DefaultDispatcher
from boobs.bot.polling import ABCPoller


class ABCFramework(ABC):
    api: "ABCAPI"
    dispatcher: "ABCDispatcher"
    poller: "ABCPoller"

    @abstractmethod
    def run_forever(self) -> None:
        pass

    @property
    def on(self) -> DefaultDispatcher:
        return self.dispatcher  # type: ignore
