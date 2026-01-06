"""The Open Meteo Marine integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, CONF_UPDATE_INTERVAL
from .coordinator import OpenMeteoMarineDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

# YAML Configuration Schema
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_LATITUDE): cv.latitude,
                vol.Required(CONF_LONGITUDE): cv.longitude,
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(
                    vol.Coerce(int), vol.Range(min=15, max=1440)
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Open Meteo Marine from YAML configuration."""
    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]
    
    _LOGGER.info("Setting up Open Meteo Marine integration from YAML")
    
    coordinator = OpenMeteoMarineDataUpdateCoordinator(
        hass,
        {
            CONF_LATITUDE: conf[CONF_LATITUDE],
            CONF_LONGITUDE: conf[CONF_LONGITUDE],
            CONF_UPDATE_INTERVAL: conf[CONF_UPDATE_INTERVAL],
        },
        update_interval=timedelta(minutes=conf[CONF_UPDATE_INTERVAL])
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["yaml_config"] = coordinator

    # Load sensor platform
    await async_load_platform(hass, Platform.SENSOR, DOMAIN, {}, config)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Open Meteo Marine from a config entry."""
    _LOGGER.info("Setting up Open Meteo Marine integration from UI")
    
    coordinator = OpenMeteoMarineDataUpdateCoordinator(
        hass,
        entry.data,
        update_interval=timedelta(minutes=entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL))
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok