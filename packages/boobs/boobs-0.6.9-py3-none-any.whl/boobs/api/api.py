from boobs.api.abc import ABCAPI
from boobs.api.utils import Token
from boobs.api.validators import (
    DEFAULT_REQUEST_VALIDATORS,
    DEFAULT_RESPONSE_VALIDATORS,
)
from boobs.modules import logger
from boobs.net.abc import ABCNetworkClient
from boobs.net.default import DefaultNetworkClient
from boobs.types.methods import APIMethods


class API(ABCAPI, APIMethods):
    def __init__(
        self, token: Token, http_client: ABCNetworkClient | None = None
    ) -> None:
        super().__init__(self)

        self.token = token
        self.network_client = http_client or DefaultNetworkClient()
        self.request_validators = DEFAULT_REQUEST_VALIDATORS
        self.response_validators = DEFAULT_RESPONSE_VALIDATORS

    async def request(self, method: str, params: dict = {}) -> bytes:
        await logger.debug("Calling", method=method, params=params)

        data = await self.validate_request(params)
        response = await self.network_client.request_bytes(
            self.api_url + method, data=data
        )

        await logger.debug("Received", response=response.decode())
        return await self.validate_response(response)
