"""Systemair Client."""

from __future__ import annotations

import socket
from typing import TYPE_CHECKING, Any

import aiohttp
import async_timeout

from .const import LOGGER

if TYPE_CHECKING:
    from .modbus import ModbusParameter


class SystemairApiClientError(Exception):
    """Exception to indicate a general API error."""


class SystemairApiClientCommunicationError(
    SystemairApiClientError,
):
    """Exception to indicate a communication error."""


class SystemairApiClient:
    """Systemair API Client."""

    def __init__(
        self,
        address: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Systemair API Client."""
        self._address = address
        self._session = session

    async def async_test_connection(self) -> Any:
        """Test connection to API."""
        return await self._api_wrapper(method="get", url=f"http://{self._address}/mread?{{}}")

    async def async_get_endpoint(self, endpoint: str) -> Any:
        """Get information from the API."""
        return await self._api_wrapper(method="get", url=f"http://{self._address}/{endpoint}")

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
        return await self._api_wrapper(method="get", url=url)

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        retries = 2
        try:
            for attempt in range(retries):
                async with async_timeout.timeout(10):
                    response = await self._session.request(
                        method=method,
                        url=url,
                        headers=headers,
                        json=data,
                    )
                    response_body = await response.text()
                    if "MB DISCONNECTED" in response_body:
                        LOGGER.warning("Received 'MB DISCONNECTED', retrying...")

                        if attempt == retries - 1:
                            raise SystemairApiClientCommunicationError(
                                "MB DISCONNECTED",
                            )

                        continue
                    if "OK" in response_body:
                        return response_body
                    return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise SystemairApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise SystemairApiClientCommunicationError(
                msg,
            ) from exception
        except SystemairApiClientCommunicationError as exception:
            msg = f"Received mb disconnect - {exception}"
            raise SystemairApiClientError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise SystemairApiClientError(
                msg,
            ) from exception
