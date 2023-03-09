from __future__ import annotations
import logging
import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from datetime import timedelta
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=4)

def setup_platform(hass: HomeAssistant, config, add_entities: AddEntitiesCallback) -> None:

    hub = hass.data[DOMAIN]["hub"]
    outputs = hub.get_all_entities()

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
        self._state = "on" if switch["value"] == True else "off"
        self.hub = hub

    @property
    def state(self) -> str: 
        return self._state

    @property
    def is_on(self) -> bool:
        return True if self._state == "on" else False

    def turn_on(self):
        self.hub.set_entity(self._uuid, True)

    def turn_off(self):
        self.hub.set_entity(self._uuid, False)

    def update(self):
        newstate = self.hub.get_entity(self._uuid)
        if newstate["value"]:
            self._state = "on"
        else:
            self._state = "off"
