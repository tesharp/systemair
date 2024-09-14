"""Constants for Systemair SAVE Connect 2.0."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "systemair_save_connect_2_0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

MAX_TEMP = 30
MIN_TEMP = 12

PRESET_MODE_MANUAL = "manual"
PRESET_MODE_CROWDED = "crowded"
PRESET_MODE_REFRESH = "refresh"
PRESET_MODE_FIREPLACE = "fireplace"
PRESET_MODE_AWAY = "away"
PRESET_MODE_HOLIDAY = "holiday"
