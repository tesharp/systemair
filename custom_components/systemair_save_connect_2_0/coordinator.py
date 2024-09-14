"""DataUpdateCoordinator for Systemair SAVE Connect 2.0."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    SystemairSaveConnectApiClientAuthenticationError,
    SystemairSaveConnectApiClientError,
)

from .const import DOMAIN, LOGGER
from .modbus import IntegerType

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import SystemairSaveConnectConfigEntry
    from .modbus import ModbusParameter


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class SystemairSaveConnectDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: SystemairSaveConnectConfigEntry
    modbus_parameters: list[ModbusParameter]

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=20),
        )
        self.modbus_parameters = []

    def register_modbus_parameters(self, modbus_parameter: ModbusParameter) -> None:
        """Register a list of Modbus parameters to be updated."""
        if modbus_parameter not in self.modbus_parameters:
            self.modbus_parameters.append(modbus_parameter)

    def get_modbus_data(self, register: ModbusParameter) -> Any:
        """Get the data for a Modbus register."""
        self.register_modbus_parameters(register)
        value = self.data.get(str(register.register - 1))
        if value is None:
            return 0
        if register.boolean:
            return value != 0
        value = int(value)
        if register.sig == IntegerType.INT and value > (1 << 15):
            value = -(65536 - value)
        return value / (register.scaleFactor or 1)

    async def set_modbus_data(self, register: ModbusParameter, value: Any) -> None:
        """Set the data for a Modbus register."""
        if register.boolean:
            if not isinstance(value, bool):
                raise ValueError("Value must be a boolean")
            value = 1 if value else 0
            return await self.config_entry.runtime_data.client.async_set_data(
                register, value
            )

        value = int(value)
        value = value * (register.scaleFactor or 1)
        if register.min is not None and value < register.min:
            value = register.min
        if register.max is not None and value > register.max:
            value = register.max

        return await self.config_entry.runtime_data.client.async_set_data(
            register, value
        )

    async def _async_setup(self) -> None:
        """Set up the coordinator."""
        menu = await self.config_entry.runtime_data.client.async_get_endpoint("menu")
        unit_version = await self.config_entry.runtime_data.client.async_get_endpoint(
            "unit_version"
        )
        self.config_entry.runtime_data.mac_address = menu["mac"]
        self.config_entry.runtime_data.serial_number = unit_version[
            "System Serial Number"
        ]
        self.config_entry.runtime_data.mb_hw_version = unit_version["MB HW version"]
        self.config_entry.runtime_data.mb_model = unit_version["MB Model"]
        self.config_entry.runtime_data.mb_sw_version = unit_version["MB SW version"]
        self.config_entry.runtime_data.iam_sw_version = unit_version["IAM SW version"]

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data(
                self.modbus_parameters
            )
        except SystemairSaveConnectApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except SystemairSaveConnectApiClientError as exception:
            raise UpdateFailed(exception) from exception
