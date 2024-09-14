"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout

from .const import LOGGER
from .modbus import ModbusParameter


class SystemairSaveConnectApiClientError(Exception):
    """Exception to indicate a general API error."""


class SystemairSaveConnectApiClientCommunicationError(
    SystemairSaveConnectApiClientError,
):
    """Exception to indicate a communication error."""


class SystemairSaveConnectApiClientAuthenticationError(
    SystemairSaveConnectApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise SystemairSaveConnectApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class SystemairSaveConnectApiClient:
    """Sample API Client."""

    def __init__(
        self,
        address: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._address = address
        self._session = session

    async def async_test_connection(self) -> Any:
        """Test connection to API."""
        return await self._api_wrapper(
            method="get", url=f"http://{self._address}/mread?{{}}"
        )

    async def async_get_endpoint(self, endpoint: str) -> Any:
        """Get information from the API."""
        return await self._api_wrapper(
            method="get", url=f"http://{self._address}/{endpoint}"
        )

    async def async_get_data(self, reg: list[ModbusParameter]) -> Any:
        """Read modbus registers."""
        query_params = ",".join(f"%22{item.register - 1}%22:1" for item in reg)
        url = f"http://{self._address}/mread?{{{query_params}}}"
        LOGGER.debug("URL: %s", url)
        return await self._api_wrapper(method="get", url=url)

    async def async_set_data(self, registry: ModbusParameter, value: int) -> Any:
        """Write data to the API."""
        query_params = f"%22{registry.register - 1}%22:{value}"
        url = f"http://{self._address}/mwrite?{{{query_params}}}"
        LOGGER.debug("URL: %s", url)
        # return None
        return await self._api_wrapper(method="get", url=url)

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            for _attempt in range(2):
                async with async_timeout.timeout(10):
                    response = await self._session.request(
                        method=method,
                        url=url,
                        headers=headers,
                        json=data,
                    )
                    _verify_response_or_raise(response)
                    response_body = await response.text()
                    if "MB DISCONNECTED" in response_body:
                        LOGGER.warning("Received 'MB DISCONNECTED', retrying...")
                        continue
                    if "OK" in response_body:
                        return response_body
                    return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise SystemairSaveConnectApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise SystemairSaveConnectApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise SystemairSaveConnectApiClientError(
                msg,
            ) from exception
