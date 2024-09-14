"""Sensor platform for Systemair SAVE Connect 2.0."""

from __future__ import annotations
from dataclasses import dataclass

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass

from homeassistant.const import (
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)

from .modbus import ModbusParameter, parameter_map
from .entity import SystemairSaveConnectEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SystemairSaveConnectDataUpdateCoordinator
    from .data import SystemairSaveConnectConfigEntry


@dataclass(kw_only=True, frozen=True)
class SystemairSaveConnectSensorEntityDescription(SensorEntityDescription):
    """Describes a Systemair sensor entity."""

    registry: ModbusParameter


ENTITY_DESCRIPTIONS = (
    SystemairSaveConnectSensorEntityDescription(
        key="outside_air_temperature",
        name="Outside air temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        registry=parameter_map["REG_SENSOR_OAT"],
    ),
    SystemairSaveConnectSensorEntityDescription(
        key="extract_air_temperature",
        name="Extract air temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        registry=parameter_map["REG_SENSOR_PDM_EAT_VALUE"],
    ),
    SystemairSaveConnectSensorEntityDescription(
        key="overheat_temperature",
        name="Overheat temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        registry=parameter_map["REG_SENSOR_OHT"],
    ),
    SystemairSaveConnectSensorEntityDescription(
        key="meter_saf_rpm",
        name="Supply air fan rpm",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        registry=parameter_map["REG_SENSOR_RPM_SAF"],
    ),
    SystemairSaveConnectSensorEntityDescription(
        key="meter_saf_reg_speed",
        name="Supply air fan speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        registry=parameter_map["REG_OUTPUT_SAF"],
    ),
    SystemairSaveConnectSensorEntityDescription(
        key="meter_eaf_rpm",
        name="Extract air fan rpm",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        registry=parameter_map["REG_SENSOR_RPM_EAF"],
    ),
    SystemairSaveConnectSensorEntityDescription(
        key="meter_eaf_reg_speed",
        name="Extract air fan speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        registry=parameter_map["REG_OUTPUT_EAF"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: SystemairSaveConnectConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        SystemairSaveConnectSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class SystemairSaveConnectSensor(SystemairSaveConnectEntity, SensorEntity):
    """Systemair SAVE Connect 2.0 Sensor class."""

    entity_description: SystemairSaveConnectSensorEntityDescription

    def __init__(
        self,
        coordinator: SystemairSaveConnectDataUpdateCoordinator,
        entity_description: SystemairSaveConnectSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.runtime_data.serial_number}-{entity_description.key}"

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.get_modbus_data(self.entity_description.registry)
