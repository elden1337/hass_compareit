from __future__ import annotations
import logging
import json
import voluptuous as vol

from homeassistant.components.switch import (SwitchEntity)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DOMAIN_DATA, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

def setup_platform(
   hass: HomeAssistant, config, add_entities: AddEntitiesCallback, discovery_info=None
) -> None:

    hub = hass.data[DOMAIN]["hub"]
    outputs = json.loads(hub.GetAllEntities())

    others = []

    for switch in outputs["outputs"]:
        if switch["name"].startswith("Styrda") or switch["name"].startswith("Vattenav"):
            others.append(switch)

    add_entities(CompareItSwitch(o, hub) for o in others)

class CompareItSwitch(SwitchEntity):  
    def __init__(self, switch, hub) -> None:
        """Initialize a CompareitSwitch."""

        self._switch = switch
        self._uuid = switch["uuid"]
        self._attr_name = switch["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"
        self._state = "on" if switch["value"] == True else "off"
        self.hub = hub

    @property
    def is_on(self) -> bool | None:
        return True if self._state == "on" else False

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self, **kwargs: Any) -> None:
        self.hub.SetEntity(self._uuid, True)
        self.update()

    def turn_off(self, **kwargs: Any) -> None:
        self.hub.SetEntity(self._uuid, False)
        self.update()

    def update(self) -> None:
        newstate = json.loads(self.hub.GetEntity(self._uuid))
        if newstate["value"] == True:
            self._state = "on"
        elif newstate["value"] == False:
            self._state = "off"
