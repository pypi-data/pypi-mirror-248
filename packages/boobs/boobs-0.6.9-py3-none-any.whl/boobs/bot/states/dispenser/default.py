from boobs.bot.states.dispenser import ABCStateDispenser
from boobs.bot.states.types import BaseStateGroup, StateRepr
from boobs.tools.storage import ABCStorage, MemoryStorage


class DefaultStateDispenser(ABCStateDispenser):
    def __init__(self, storage: ABCStorage | None = None) -> None:
        self.storage = storage or MemoryStorage()

    async def get(self, chat_id: int) -> StateRepr | None:
        return await self.storage.get(f"fsm_state:{chat_id}", default=None)

    async def set(self, chat_id: int, state: BaseStateGroup, **payload) -> None:
        return await self.storage.put(
            f"fsm_state:{chat_id}",
            StateRepr(chat_id=chat_id, state=state, payload=payload),
        )

    async def finish(self, chat_id: int) -> None:
        return await self.storage.delete(f"fsm_state:{chat_id}")
