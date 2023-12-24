from typing import Any

from boobs.bot.nipple.abc import ABCNipple
from boobs.bot.dispatch.dispatcher import ABCDispatcher, DefaultDispatcher


class DefaultNipple(ABCNipple):
    def __init__(self, dispatcher: "ABCDispatcher | None" = None) -> None:
        self.dispatcher = dispatcher or DefaultDispatcher()

    def load_into(self, framework: Any) -> "DefaultNipple":
        self.state_dispenser = framework.state_dispenser
        self.api = framework.api

        framework.dispatcher.load(self.dispatcher)
        return self

    @property
    def on(self) -> DefaultDispatcher:
        return self.dispatcher  # type: ignore
