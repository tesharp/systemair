"""Sensor platform for Systemair0."""

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
    UnitOfTemperature,
)

from .entity import SystemairEntity
from .modbus import ModbusParameter, parameter_map

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SystemairDataUpdateCoordinator
    from .data import SystemairConfigEntry


@dataclass(kw_only=True, frozen=True)
class SystemairSensorEntityDescription(SensorEntityDescription):
    """Describes a Systemair sensor entity."""

    registry: ModbusParameter


ENTITY_DESCRIPTIONS = (
    SystemairSensorEntityDescription(
        key="outside_air_temperature",
        translation_key="outside_air_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        registry=parameter_map["REG_SENSOR_OAT"],
    ),
    SystemairSensorEntityDescription(
        key="extract_air_temperature",
        translation_key="extract_air_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        registry=parameter_map["REG_SENSOR_PDM_EAT_VALUE"],
    ),
    SystemairSensorEntityDescription(
        key="overheat_temperature",
        translation_key="overheat_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        registry=parameter_map["REG_SENSOR_OHT"],
    ),
    SystemairSensorEntityDescription(
        key="meter_saf_rpm",
        translation_key="meter_saf_rpm",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        registry=parameter_map["REG_SENSOR_RPM_SAF"],
    ),
    SystemairSensorEntityDescription(
        key="meter_saf_reg_speed",
        translation_key="meter_saf_reg_speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        registry=parameter_map["REG_OUTPUT_SAF"],
    ),
    SystemairSensorEntityDescription(
        key="meter_eaf_rpm",
        translation_key="meter_eaf_rpm",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        registry=parameter_map["REG_SENSOR_RPM_EAF"],
    ),
    SystemairSensorEntityDescription(
        key="meter_eaf_reg_speed",
        translation_key="meter_eaf_reg_speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        registry=parameter_map["REG_OUTPUT_EAF"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: SystemairConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        SystemairSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class SystemairSensor(SystemairEntity, SensorEntity):
    """Systemair Sensor class."""

    _attr_has_entity_name = True

    entity_description: SystemairSensorEntityDescription

    def __init__(
        self,
        coordinator: SystemairDataUpdateCoordinator,
        entity_description: SystemairSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{entity_description.key}"

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.get_modbus_data(self.entity_description.registry)
