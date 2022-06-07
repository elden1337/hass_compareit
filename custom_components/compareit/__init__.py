"""The Compare IT integration."""
from __future__ import annotations
from datetime import timedelta

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery

from .const import (
    DOMAIN,
    PLATFORMS,
    )
from .hub import Hub


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry) -> bool:
    """Set up Compare It"""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config.entry_id] = config.data

    hub = Hub(config.data["username"], config.data["password"])

    hass.data[DOMAIN]["hub"] = hub

    async def servicehandler_set_smarthome_mode(call): # pylint:disable=unused-argument
        await hub.call_set_smarthome_mode()

    async def servicehandler_activate_scenario(call): # pylint:disable=unused-argument
        await hub.call_activate_scenario()

    hass.services.async_register(DOMAIN, "set_smarthome_mode", servicehandler_set_smarthome_mode)
    hass.services.async_register(DOMAIN, "activate_scenario", servicehandler_activate_scenario)

    for domain in PLATFORMS:
        hass.async_create_task(
            discovery.async_load_platform(hass, domain, DOMAIN, {}, config)
        )

    return True

def unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok