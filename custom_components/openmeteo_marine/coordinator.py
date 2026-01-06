"""DataUpdateCoordinator for Open Meteo Marine."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

import httpx
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, API_BASE_URL, ATTRIBUTION

_LOGGER = logging.getLogger(__name__)


class OpenMeteoMarineDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Open Meteo Marine API."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: dict[str, Any],
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.latitude = config[CONF_LATITUDE]
        self.longitude = config[CONF_LONGITUDE]
        self._client = httpx.AsyncClient(timeout=30.0)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            return await self._fetch_marine_data()
        except Exception as exception:
            raise UpdateFailed(f"Error communicating with API: {exception}") from exception

    async def _fetch_marine_data(self) -> dict[str, Any]:
        """Fetch marine data from Open Meteo API."""
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": [
                "wave_height",
                "wave_direction", 
                "wave_period",
                "sea_surface_temperature",
                "ocean_current_velocity",
                "ocean_current_direction"
            ],
            "timezone": "auto",
        }

        try:
            response = await self._client.get(API_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "current" not in data:
                raise UpdateFailed("Invalid API response: missing current data")

            current_data = data["current"]
            
            # Parse the data into a more usable format
            parsed_data = {}
            
            if "wave_height" in current_data:
                parsed_data["wave_height"] = current_data["wave_height"]
            
            if "wave_direction" in current_data:
                parsed_data["wave_direction"] = current_data["wave_direction"]
                
            if "wave_period" in current_data:
                parsed_data["wave_period"] = current_data["wave_period"]
                
            if "sea_surface_temperature" in current_data:
                parsed_data["sea_surface_temperature"] = current_data["sea_surface_temperature"]
                
            if "ocean_current_velocity" in current_data:
                parsed_data["current_velocity"] = current_data["ocean_current_velocity"]
                
            if "ocean_current_direction" in current_data:
                parsed_data["current_direction"] = current_data["ocean_current_direction"]

            parsed_data["last_updated"] = datetime.now()
            parsed_data["attribution"] = ATTRIBUTION
            
            _LOGGER.debug("Successfully fetched marine data: %s", parsed_data)
            return parsed_data

        except httpx.RequestError as err:
            raise UpdateFailed(f"Error requesting data: {err}") from err
        except httpx.HTTPStatusError as err:
            raise UpdateFailed(f"HTTP error occurred: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def async_shutdown(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()