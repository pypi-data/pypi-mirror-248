from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, AsyncIterator

if TYPE_CHECKING:
    from boobs.api.abc import ABCAPI
    from boobs.errors import ABCErrorHandler
    from boobs.types.objects import Update


class ABCPoller(ABC):
    api: "ABCAPI"
    error_handler: "ABCErrorHandler"

    @abstractmethod
    def poll(self) -> AsyncIterator["Update"]:
        """
        Polls server for updates and yields them
        """
