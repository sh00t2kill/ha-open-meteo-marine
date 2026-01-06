"""Platform for sensor integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES, ATTRIBUTION
from .coordinator import OpenMeteoMarineDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for sensor_type, config in SENSOR_TYPES.items():
        entities.append(OpenMeteoMarineSensor(coordinator, sensor_type, config))

    async_add_entities(entities)


async def async_setup_platform(
    hass: HomeAssistant, config, async_add_entities: AddEntitiesCallback, discovery_info=None
) -> None:
    """Set up the sensor platform from YAML configuration."""
    if discovery_info is None:
        return

    coordinator = hass.data[DOMAIN]["yaml_config"]

    entities = []
    for sensor_type, sensor_config in SENSOR_TYPES.items():
        entities.append(OpenMeteoMarineSensor(coordinator, sensor_type, sensor_config))

    async_add_entities(entities)


class OpenMeteoMarineSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Open Meteo Marine Sensor."""

    def __init__(
        self,
        coordinator: OpenMeteoMarineDataUpdateCoordinator,
        sensor_type: str,
        config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._sensor_type = sensor_type
        self._config = config
        self._attr_name = f"Open Meteo Marine {config['name']}"
        self._attr_unique_id = f"{coordinator.latitude}_{coordinator.longitude}_{sensor_type}"
        self._attr_native_unit_of_measurement = config["native_unit_of_measurement"]
        self._attr_device_class = config.get("device_class")
        self._attr_state_class = config.get("state_class")
        self._attr_icon = config["icon"]
        self._attr_attribution = ATTRIBUTION

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this Open Meteo Marine instance."""
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.latitude}_{self.coordinator.longitude}")},
            "name": f"Open Meteo Marine ({self.coordinator.latitude}, {self.coordinator.longitude})",
            "manufacturer": "Open Meteo",
            "model": "Marine Weather API",
            "sw_version": "1.0",
        }

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        if not self.coordinator.data:
            return None
        
        value = self.coordinator.data.get(self._sensor_type)
        
        if value is None:
            _LOGGER.debug("No data available for sensor %s", self._sensor_type)
            return None
            
        try:
            return float(value)
        except (ValueError, TypeError):
            _LOGGER.warning("Invalid value for sensor %s: %s", self._sensor_type, value)
            return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.native_value is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs = {}
        
        if self.coordinator.data:
            attrs["latitude"] = self.coordinator.latitude
            attrs["longitude"] = self.coordinator.longitude
            
            if "last_updated" in self.coordinator.data:
                attrs["last_updated"] = self.coordinator.data["last_updated"].isoformat()
        
        return attrs