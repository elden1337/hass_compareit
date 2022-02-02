"""The Compare IT integration."""
from __future__ import annotations
from datetime import timedelta
from Compare_It import CompareIt
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery
#from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN,
    SCAN_INTERVAL, 
    PLATFORMS,
    DOMAIN_DATA
    )

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: ConfigEntry) -> bool:
    """Set up Compare It"""
    
    username = config[DOMAIN].get(CONF_USERNAME)
    password = config[DOMAIN].get(CONF_PASSWORD)
    hass.data[DOMAIN_DATA] = {}

    hub = CompareIt(username, password)

    hass.data[DOMAIN_DATA]["hub"] = hub
    #hass.config_entries.async_setup_platforms(config, PLATFORMS)
    
    # Load platforms
    for domain in PLATFORMS:
        hass.async_create_task(
            discovery.async_load_platform(hass, domain, DOMAIN, {}, config)
        )

    return True

def unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    unload_ok = hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok