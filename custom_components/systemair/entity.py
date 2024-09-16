"""Systemair entity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .coordinator import SystemairDataUpdateCoordinator


class SystemairEntity(CoordinatorEntity[SystemairDataUpdateCoordinator]):
    """SystemairEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: SystemairDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            manufacturer="Systemair",
            model=coordinator.config_entry.runtime_data.mb_model,
            hw_version=coordinator.config_entry.runtime_data.mb_hw_version,
            sw_version=coordinator.config_entry.runtime_data.mb_sw_version,
            serial_number=coordinator.config_entry.runtime_data.serial_number,
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
        )
