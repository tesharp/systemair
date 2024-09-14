"""Binary sensor platform for Systemair SAVE Connect 2.0."""

from __future__ import annotations
from dataclasses import dataclass

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import SystemairSaveConnectEntity
from .modbus import ModbusParameter, parameter_map

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SystemairSaveConnectDataUpdateCoordinator
    from .data import SystemairSaveConnectConfigEntry


@dataclass(kw_only=True, frozen=True)
class SystemairSaveConnectBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a Systemair binary sensor entity."""

    registry: ModbusParameter


ENTITY_DESCRIPTIONS = (
    SystemairSaveConnectBinarySensorEntityDescription(
        key="heat_exchange_active",
        name="Heat Exchange Active",
        device_class=BinarySensorDeviceClass.RUNNING,
        registry=parameter_map["REG_OUTPUT_Y2_DIGITAL"],
    ),
    SystemairSaveConnectBinarySensorEntityDescription(
        key="heater_active",
        name="Heater Active",
        device_class=BinarySensorDeviceClass.RUNNING,
        registry=parameter_map["REG_OUTPUT_TRIAC"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: SystemairSaveConnectConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        SystemairSaveConnectBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class SystemairSaveConnectBinarySensor(SystemairSaveConnectEntity, BinarySensorEntity):
    """Systemair SAVE Connect 2.0 binary_sensor class."""

    entity_description: SystemairSaveConnectBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: SystemairSaveConnectDataUpdateCoordinator,
        entity_description: SystemairSaveConnectBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.runtime_data.serial_number}-{entity_description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.get_modbus_data(self.entity_description.registry) != 0
