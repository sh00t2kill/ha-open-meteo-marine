"""Test the Open Meteo Marine config flow."""
import pytest
from unittest.mock import AsyncMock, patch

from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant

from custom_components.openmeteo_marine.config_flow import ConfigFlow
from custom_components.openmeteo_marine.const import DOMAIN


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.openmeteo_marine.config_flow.validate_input",
        return_value={"title": "Open Meteo Marine (40.7128, -74.0060)"},
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_LATITUDE: 40.7128,
                CONF_LONGITUDE: -74.0060,
                "update_interval": 60,
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result2["title"] == "Open Meteo Marine (40.7128, -74.0060)"
    assert result2["data"] == {
        CONF_LATITUDE: 40.7128,
        CONF_LONGITUDE: -74.0060,
        "update_interval": 60,
    }


async def test_form_invalid_latitude(hass: HomeAssistant) -> None:
    """Test we handle invalid latitude."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_LATITUDE: 91.0,  # Invalid latitude
            CONF_LONGITUDE: -74.0060,
            "update_interval": 60,
        },
    )

    assert result2["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result2["errors"] == {"base": "invalid_latitude"}