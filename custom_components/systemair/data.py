"""Custom types for Systemair."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import SystemairApiClient
    from .coordinator import SystemairDataUpdateCoordinator


type SystemairConfigEntry = ConfigEntry[SystemairData]


@dataclass
class SystemairData:
    """Data for the Systemair."""

    client: SystemairApiClient
    coordinator: SystemairDataUpdateCoordinator
    integration: Integration

    iam_sw_version: str | None = None
    mb_hw_version: str | None = None
    mb_model: str | None = None
    mb_sw_version: str | None = None
    serial_number: str | None = None
    mac_address: str | None = None
