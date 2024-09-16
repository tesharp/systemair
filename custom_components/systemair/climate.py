"""Systemair integration."""

import asyncio.exceptions
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
)
from homeassistant.components.climate.const import (
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, PRECISION_WHOLE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from httpx import DecodingError

from .const import (
    MAX_TEMP,
    MIN_TEMP,
    PRESET_MODE_AWAY,
    PRESET_MODE_CROWDED,
    PRESET_MODE_FIREPLACE,
    PRESET_MODE_HOLIDAY,
    PRESET_MODE_MANUAL,
    PRESET_MODE_REFRESH,
)
from .coordinator import SystemairDataUpdateCoordinator
from .entity import SystemairEntity
from .modbus import parameter_map

PRESET_MODE_TO_VALUE_MAP = {
    PRESET_MODE_MANUAL: 2,
    PRESET_MODE_CROWDED: 3,
    PRESET_MODE_REFRESH: 4,
    PRESET_MODE_FIREPLACE: 5,
    PRESET_MODE_AWAY: 6,
    PRESET_MODE_HOLIDAY: 7,
}

VALUE_TO_PRESET_MODE_MAP = {value: key for key, value in PRESET_MODE_TO_VALUE_MAP.items()}

FAN_MODE_TO_VALUE_MAP = {
    FAN_LOW: 2,
    FAN_MEDIUM: 3,
    FAN_HIGH: 4,
}

VALUE_TO_FAN_MODE_MAP = {value: key for key, value in FAN_MODE_TO_VALUE_MAP.items()}


async def async_setup_entry(
    _hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Systemair unit."""
    async_add_entities([SystemairClimateEntity(config_entry.runtime_data.coordinator)])


class SystemairClimateEntity(SystemairEntity, ClimateEntity):
    """Systemair air handling unit."""

    _attr_name = None

    from typing import ClassVar

    _attr_hvac_modes: ClassVar[list[HVACMode]] = [
        HVACMode.FAN_ONLY,
    ]

    _attr_preset_modes: ClassVar[list[str]] = [
        PRESET_MODE_MANUAL,
        PRESET_MODE_CROWDED,
        PRESET_MODE_REFRESH,
        PRESET_MODE_FIREPLACE,
        PRESET_MODE_AWAY,
        PRESET_MODE_HOLIDAY,
    ]

    _attr_fan_modes: ClassVar[list[str]] = [
        FAN_LOW,
        FAN_MEDIUM,
        FAN_HIGH,
    ]

    _attr_supported_features = (
        ClimateEntityFeature.PRESET_MODE | ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE
    )

    _attr_target_temperature_step = PRECISION_WHOLE
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_max_temp = MAX_TEMP
    _attr_min_temp = MIN_TEMP
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(self, coordinator: SystemairDataUpdateCoordinator) -> None:
        """Initialize the Systemair unit."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self.translation_key = "saveconnect"

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return current HVAC action."""
        return HVACAction.FAN

    #     if self.device.electric_heater:
    #         return HVACAction.HEATING
    #     return HVACAction.FAN

    @property
    def current_humidity(self) -> float | None:
        """Return the current humidity."""
        return self.coordinator.get_modbus_data(parameter_map["REG_SENSOR_RHS_PDM"])

    @property
    def current_temperature(self) -> float:
        """Return the current temperature."""
        return self.coordinator.get_modbus_data(parameter_map["REG_SENSOR_SAT"])

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""
        return self.coordinator.get_modbus_data(parameter_map["REG_TC_SP"])

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return

        try:
            await self.coordinator.set_modbus_data(parameter_map["REG_TC_SP"], temperature)
        except (asyncio.exceptions.TimeoutError, ConnectionError, DecodingError) as exc:
            raise HomeAssistantError from exc
        finally:
            await self.coordinator.async_refresh()

    @property
    def preset_mode(self) -> str:
        """
        Return the current preset mode, e.g., manual, crowded, refresh, fireplace, away or holiday.

        Requires ClimateEntityFeature.PRESET_MODE.
        """
        mode = self.coordinator.get_modbus_data(parameter_map["REG_USERMODE_HMI_CHANGE_REQUEST"])
        return VALUE_TO_PRESET_MODE_MAP.get(mode, PRESET_MODE_MANUAL)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        ventilation_mode = PRESET_MODE_TO_VALUE_MAP[preset_mode]

        try:
            await self.coordinator.set_modbus_data(parameter_map["REG_USERMODE_HMI_CHANGE_REQUEST"], ventilation_mode)
        except (asyncio.exceptions.TimeoutError, ConnectionError, DecodingError) as exc:
            raise HomeAssistantError from exc
        finally:
            await self.coordinator.async_refresh()

    @property
    def hvac_mode(self) -> HVACMode:
        """Return hvac operation ie. heat, cool mode."""
        return HVACMode.FAN_ONLY
        # if self.device.ventilation_mode == VENTILATION_MODE_STOP:
        #     return HVACMode.OFF

        # return HVACMode.FAN_ONLY

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        return
        # try:
        #     if hvac_mode == HVACMode.OFF:
        #         await self.device.set_ventilation_mode(VENTILATION_MODE_STOP)
        #     else:
        #         await self.device.set_ventilation_mode(VENTILATION_MODE_HOME)
        # except (asyncio.exceptions.TimeoutError, ConnectionError, DecodingError) as exc:
        #     raise HomeAssistantError from exc
        # finally:
        #     await self.coordinator.async_refresh()

    @property
    def fan_mode(self) -> str:
        """Return the current fan mode."""
        mode = self.coordinator.get_modbus_data(parameter_map["REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF"])
        return VALUE_TO_FAN_MODE_MAP.get(mode, FAN_LOW)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        mode = FAN_MODE_TO_VALUE_MAP[fan_mode]
        try:
            await self.coordinator.set_modbus_data(parameter_map["REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF"], mode)
        except (asyncio.exceptions.TimeoutError, ConnectionError) as exc:
            raise HomeAssistantError from exc
        finally:
            await self.coordinator.async_refresh()
