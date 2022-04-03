from __future__ import annotations
import logging
import json
import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from datetime import timedelta
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=20)

async def async_setup_entry(hass: HomeAssistant, config, async_add_entities: AddEntitiesCallback) -> None:

    hub = hass.data[DOMAIN]["hub"]
    outputs = await json.loads(hub.GetAllEntities())

    others = []

    for switch in outputs["outputs"]:
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
        self.state = "on" if switch["value"] == True else "off"
        self.hub = hub

    @property
    def state(self) -> str: 
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def is_on(self) -> bool:
        return True if self._state == "on" else False

    async def async_turn_on(self):
        await self.hub.SetEntity(self._uuid, True)
        self.async_write_ha_state()

    async def async_turn_off(self):
        await self.hub.SetEntity(self._uuid, False)
        self.async_write_ha_state()

    async def async_update(self):
        newstate = await json.loads(self.hub.GetEntity(self._uuid))
        if newstate["value"] == True:
            self.state = "on"
        elif newstate["value"] == False:
            self.state = "off"
