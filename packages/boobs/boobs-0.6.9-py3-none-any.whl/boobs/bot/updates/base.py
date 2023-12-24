from boobs.api import ABCAPI, API
from boobs.bot.states import StateRepr


class BaseUpdate:
    unprep_ctx_api: ABCAPI | None = None
    state_repr: StateRepr | None = None

    @property
    def ctx_api(self) -> API:
        return self.unprep_ctx_api  # type: ignore
