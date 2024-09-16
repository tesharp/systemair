"""Adds config flow for Systemair."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    SystemairApiClient,
    SystemairApiClientCommunicationError,
    SystemairApiClientError,
)
from .const import DOMAIN, LOGGER


class SystemairFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Systemair."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                mac_address = await self._test_connection(
                    address=user_input[CONF_IP_ADDRESS],
                )
            except SystemairApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except SystemairApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(mac_address)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_IP_ADDRESS],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_IP_ADDRESS, description="IP / dns address of web interface"
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        )
                    )
                },
            ),
            errors=_errors,
        )

    async def _test_connection(self, address: str) -> str:
        """Validate credentials."""
        client = SystemairApiClient(
            address=address,
            session=async_create_clientsession(self.hass),
        )
        menu = await client.async_get_endpoint("menu")
        return menu["mac"]
