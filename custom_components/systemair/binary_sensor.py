"""Binary sensor platform for Systemair."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import SystemairEntity
from .modbus import ModbusParameter, parameter_map

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SystemairDataUpdateCoordinator
    from .data import SystemairConfigEntry


@dataclass(kw_only=True, frozen=True)
class SystemairBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a Systemair binary sensor entity."""

    registry: ModbusParameter


ENTITY_DESCRIPTIONS = (
    SystemairBinarySensorEntityDescription(
        key="heat_exchange_active",
        translation_key="heat_exchange_active",
        device_class=BinarySensorDeviceClass.RUNNING,
        registry=parameter_map["REG_OUTPUT_Y2_DIGITAL"],
    ),
    SystemairBinarySensorEntityDescription(
        key="heater_active",
        translation_key="heater_active",
        device_class=BinarySensorDeviceClass.RUNNING,
        registry=parameter_map["REG_OUTPUT_TRIAC"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: SystemairConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        SystemairBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class SystemairBinarySensor(SystemairEntity, BinarySensorEntity):
    """Systemair binary_sensor class."""

    _attr_has_entity_name = True

    entity_description: SystemairBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: SystemairDataUpdateCoordinator,
        entity_description: SystemairBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{entity_description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.get_modbus_data(self.entity_description.registry) != 0
