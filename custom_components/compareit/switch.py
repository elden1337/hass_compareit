from __future__ import annotations
import logging
import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from datetime import timedelta
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=6)

async def async_setup_entry(hass: HomeAssistant, config, async_add_entities):

    hub = hass.data[DOMAIN]["hub"]
    result = await hub.async_get_all_entities()

    others = []

    for switch in result["outputs"]:
        if switch["name"].startswith("Styrda") or switch["name"].startswith("Vattenav"):
            others.append(switch)
    _LOGGER.info("compareit setting up switches")
    async_add_entities(CompareItSwitch(o, hub) for o in others)

class CompareItSwitch(SwitchEntity):  
    def __init__(self, switch, hub) -> None:
        """Initialize a CompareitSwitch."""

        self._uuid = switch["uuid"]
        self._attr_name = switch["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"
        self._state = None
        self._state = "on" if switch["value"] == True else "off"
        self.hub = hub

    @property
    def state(self) -> str: 
        return self._state

    @property
    def is_on(self) -> bool:
        return True if self._state == "on" else False

    async def async_turn_on(self):
        await self.hub.async_set_entity(self._uuid, True)

    async def async_turn_off(self):
        await self.hub.async_set_entity(self._uuid, False)

    async def async_update(self):
        newstate = await self.hub.async_get_entity(self._uuid)
        if newstate["value"]:
            self._state = "on"
        else:
            self._state = "off"

    @property
    def device_info(self):
        return {
            "identifiers":  {(DOMAIN, 1337)},
            "name":         "HomeLine",
            "sw_version":   1,
            "model":        2,
            "manufacturer": "Peaq systems",
        }
