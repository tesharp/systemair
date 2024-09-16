"""Switch platform for Systemair."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .entity import SystemairEntity
from .modbus import ModbusParameter, parameter_map

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SystemairDataUpdateCoordinator
    from .data import SystemairConfigEntry


@dataclass(kw_only=True, frozen=True)
class SystemairSwitchEntityDescription(SwitchEntityDescription):
    """Describes a Systemair sensor entity."""

    registry: ModbusParameter


ENTITY_DESCRIPTIONS = (
    SystemairSwitchEntityDescription(
        key="eco_mode",
        name="ECO Mode",
        icon="mdi:leaf",
        registry=parameter_map["REG_ECO_MODE_ON_OFF"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: SystemairConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        SystemairSwitch(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class SystemairSwitch(SystemairEntity, SwitchEntity):
    """Systemair switch class."""

    entity_description: SystemairSwitchEntityDescription

    def __init__(
        self,
        coordinator: SystemairDataUpdateCoordinator,
        entity_description: SystemairSwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.runtime_data.serial_number}-{entity_description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.coordinator.get_modbus_data(self.entity_description.registry) != 0

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        await self.coordinator.set_modbus_data(self.entity_description.registry, value=True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        await self.coordinator.set_modbus_data(self.entity_description.registry, value=False)
        await self.coordinator.async_request_refresh()
