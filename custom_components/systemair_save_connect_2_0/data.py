"""Custom types for Systemair SAVE Connect 2.0."""

from __future__ import annotations

from curses import noecho
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import SystemairSaveConnectApiClient
    from .coordinator import SystemairSaveConnectDataUpdateCoordinator


type SystemairSaveConnectConfigEntry = ConfigEntry[SystemairSaveConnectData]


@dataclass
class SystemairSaveConnectData:
    """Data for the Systemair SAVE Connect 2.0."""

    client: SystemairSaveConnectApiClient
    coordinator: SystemairSaveConnectDataUpdateCoordinator
    integration: Integration

    iam_sw_version: str | None = None
    mb_hw_version: str | None = None
    mb_model: str | None = None
    mb_sw_version: str | None = None
    serial_number: str | None = None
    mac_address: str | None = None
