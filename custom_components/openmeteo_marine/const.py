"""Constants for the Open Meteo Marine integration."""

from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE

DOMAIN = "openmeteo_marine"
ATTRIBUTION = "Data provided by Open-Meteo Marine API"

# Configuration
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_UPDATE_INTERVAL = 60  # minutes

# API endpoints
API_BASE_URL = "https://marine-api.open-meteo.com/v1/marine"

# Sensor types
SENSOR_TYPES = {
    "wave_height": {
        "name": "Wave Height",
        "native_unit_of_measurement": "m",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:wave",
        "api_param": "wave_height",
    },
    "wave_direction": {
        "name": "Wave Direction",
        "native_unit_of_measurement": "°",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:compass",
        "api_param": "wave_direction",
    },
    "wave_period": {
        "name": "Wave Period",
        "native_unit_of_measurement": "s",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
        "api_param": "wave_period",
    },
    "sea_surface_temperature": {
        "name": "Sea Surface Temperature",
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
        "api_param": "sea_surface_temperature",
    },
    "current_velocity": {
        "name": "Current Velocity",
        "native_unit_of_measurement": "m/s",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:waves",
        "api_param": "ocean_current_velocity",
    },
    "current_direction": {
        "name": "Current Direction",
        "native_unit_of_measurement": "°",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:compass-outline",
        "api_param": "ocean_current_direction",
    },
}