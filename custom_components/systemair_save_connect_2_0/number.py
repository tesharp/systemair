"""The Systemair SAVE Connect 2.0 integration."""

import asyncio.exceptions
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from typing import TYPE_CHECKING

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import SystemairSaveConnectEntity
from .modbus import ModbusParameter, parameter_map
from .data import SystemairSaveConnectConfigEntry
from .coordinator import SystemairSaveConnectDataUpdateCoordinator


@dataclass(kw_only=True, frozen=True)
class SystemairSaveConnectNumberEntityDescription(NumberEntityDescription):
    """Describes a Systemair number entity."""

    registry: ModbusParameter


NUMBERS: tuple[SystemairSaveConnectNumberEntityDescription, ...] = (
    SystemairSaveConnectNumberEntityDescription(
        key="time_delay_holiday",
        name="Holiday: Time delay",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.DURATION,
        native_step=1,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=UnitOfTime.DAYS,
        registry=parameter_map["REG_USERMODE_HOLIDAY_TIME"],
    ),
    SystemairSaveConnectNumberEntityDescription(
        key="time_delay_away",
        name="Away: Time delay",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.DURATION,
        native_step=1,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=UnitOfTime.HOURS,
        registry=parameter_map["REG_USERMODE_AWAY_TIME"],
    ),
    SystemairSaveConnectNumberEntityDescription(
        key="time_delay_fireplace",
        name="Fireplace: Time delay",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.DURATION,
        native_step=1,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        registry=parameter_map["REG_USERMODE_FIREPLACE_TIME"],
    ),
    SystemairSaveConnectNumberEntityDescription(
        key="time_delay_refresh",
        name="Refresh: Time delay",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.DURATION,
        native_step=1,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        registry=parameter_map["REG_USERMODE_REFRESH_TIME"],
    ),
    SystemairSaveConnectNumberEntityDescription(
        key="time_delay_crowded",
        name="Crowded: Time delay",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.DURATION,
        native_step=1,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=UnitOfTime.HOURS,
        registry=parameter_map["REG_USERMODE_CROWDED_TIME"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SystemairSaveConnectConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number from a config entry."""
    async_add_entities(
        SystemairSaveConnectNumber(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in NUMBERS
    )


class SystemairSaveConnectNumber(SystemairSaveConnectEntity, NumberEntity):
    """Representation of a SAVE Connect 2.0 Number."""

    entity_description: SystemairSaveConnectNumberEntityDescription

    def __init__(
        self,
        coordinator: SystemairSaveConnectDataUpdateCoordinator,
        entity_description: SystemairSaveConnectNumberEntityDescription,
    ) -> None:
        """Initialize the number class."""
        super().__init__(coordinator)

        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.runtime_data.serial_number}-{entity_description.key}"
        self.native_min_value = float(entity_description.registry.min or 0)
        self.native_max_value = float(entity_description.registry.max or 100)

    @property
    def native_value(self) -> float:
        """Return the state of the number."""
        return self.coordinator.get_modbus_data(self.entity_description.registry)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        try:
            await self.coordinator.set_modbus_data(
                self.entity_description.registry, value
            )
        except (asyncio.exceptions.TimeoutError, ConnectionError) as exc:
            raise HomeAssistantError from exc
        finally:
            await self.coordinator.async_refresh()
