from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.light import (ATTR_BRIGHTNESS, LightEntity)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from datetime import timedelta

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=4)


async def async_setup_entry(hass: HomeAssistant, config, async_add_entities):
    hub = hass.data[DOMAIN]["hub"]
    outputs = await hub.get_all_entities()

    staticlights = []
    dimmablelights = []

    for light in outputs["outputs"]:
        if light["name"].startswith("Belysning") or light["name"].startswith("Ytter"):
            if light["type"] == 1:
                staticlights.append(light)
            elif light["type"] == 2:
                dimmablelights.append(light)

    async_add_entities(CompareItStaticLight(staticlight, hub) for staticlight in staticlights)
    async_add_entities(CompareItDimmableLight(dimmablelight, hub) for dimmablelight in dimmablelights)

class CompareItStaticLight(LightEntity):
    def __init__(self, light, hub) -> None:
        """Initialize a static CompareitLight."""    
        self._uuid = light["uuid"]
        self._attr_name = light["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"
        self._state = None
        self.hub = hub

    @property
    def is_on(self) -> bool:
        return True if self._state == "on" else False

    def turn_on(self) -> None:
        self.hub.set_entity(self._uuid, True)
        self._state = "on"

    def turn_off(self) -> None:
        self.hub.set_entity(self._uuid, False)
        self._state = "off"

    def update(self) -> None:
        newstate = self.hub.get_entity(self._uuid)
        self._state = "on" if newstate.get("value") else "off"

    @property
    def device_info(self):
        return {
            "identifiers":  1337,
            "name":         "HomeLine",
            "sw_version":   1,
            "model":        2,
            "manufacturer": "Peaq systems",
        }


class CompareItDimmableLight(LightEntity):  
    def __init__(self, light, hub) -> None:
        """Initialize a dimmable CompareitLight."""
        self._light = light
        self._uuid = light["uuid"]
        self._attr_name = light["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"
        self._state = None
        self._brightness = None
        self.hub = hub

    @property
    def brightness(self):
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        return True if self._state == "on" else False

    @property
    def supported_features(self):
        return 1 #brightness

    def turn_on(self, **kwargs: Any) -> None:
        self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self.hub.set_entity(self._uuid, round(self._brightness/2.55))
        self._state = "on"

    def turn_off(self) -> None:
        self.hub.set_entity(self._uuid, 0)
        self._brightness = 0
        self._state = "off"

    def update(self) -> None:
        newstate = self.hub.get_entity(self._uuid)
        if newstate["value"] > 0:
            self._state = "on"
        elif newstate["value"] == 0:
            self._state = "off"
        self._brightness =  round(newstate["value"] * 2.55)

    @property
    def device_info(self):
        return {
            "identifiers":  1337,
            "name":         "HomeLine",
            "sw_version":   1,
            "model":        2,
            "manufacturer": "Peaq systems",
        }