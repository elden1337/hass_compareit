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

SCAN_INTERVAL = timedelta(seconds=5)

def setup_platform(hass: HomeAssistant, config, add_entities: AddEntitiesCallback) -> None:

    hub = hass.data[DOMAIN]["hub"]
    outputs = json.loads(hub.GetAllEntities())

    others = []

    for switch in outputs["outputs"]:
        if switch["name"].startswith("Styrda") or switch["name"].startswith("Vattenav"):
            others.append(switch)
    _LOGGER.info("compareit setting up switches")
    add_entities(CompareItSwitch(o, hub) for o in others)

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
        return self._state == "on"

    def turn_on(self):
        self.hub.SetEntity(self._uuid, True)

    def turn_off(self):
        self.hub.SetEntity(self._uuid, False)

    def update(self):
        try:
            newstate = json.loads(self.hub.GetEntity(self._uuid))
            if newstate["value"] == True:
                self.state = "on"
            elif newstate["value"] == False:
                self.state = "off"
        except:
            _LOGGER.warning(f"Unable to update {self._attr_name}")

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._hub.hub_id)}}
