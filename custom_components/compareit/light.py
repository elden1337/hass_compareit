from __future__ import annotations
import logging
import json
from typing import Any

from homeassistant.components.light import (ATTR_BRIGHTNESS, LightEntity)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from datetime import timedelta

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)

async def setup_platform(
   hass: HomeAssistant, config, add_entities: AddEntitiesCallback, discovery_info=None
) -> None:

    hub = hass.data[DOMAIN]["hub"]
    outputs = json.loads(await hub.GetAllEntities())

    staticlights = []
    dimmablelights = []

    for light in outputs["outputs"]:
        if light["name"].startswith("Belysning") or light["name"].startswith("Ytter"):
            if light["type"] == 1:
                staticlights.append(light)
            elif light["type"] == 2:
                dimmablelights.append(light)

    add_entities(CompareItStaticLight(staticlight, hub) for staticlight in staticlights)
    add_entities(CompareItDimmableLight(dimmablelight, hub) for dimmablelight in dimmablelights)

class CompareItStaticLight(LightEntity):
    def __init__(self, light, hub) -> None:
        """Initialize a static CompareitLight."""    
        self._uuid = light["uuid"]
        self._attr_name = light["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"

        self._state = "on" if light["value"] == True else "off"
        self.hub = hub

    @property
    def is_on(self) -> bool | None:
        return True if self._state == "on" else False

    def turn_on(self) -> None:
        self.hub.SetEntity(self._uuid, True)
        self.update()

    def turn_off(self) -> None:
        self.hub.SetEntity(self._uuid, False)
        self.update()

    def update(self) -> None:
        try:
            newstate = json.loads(self.hub.GetEntity(self._uuid))
            if newstate["value"] == True:
                self._state = "on"
            elif newstate["value"] == False:
                self._state = "off"
        except:
            _LOGGER.warning(f"Unable to update {self._attr_name}")

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._hub.hub_id)}}

class CompareItDimmableLight(LightEntity):  
    def __init__(self, light, hub) -> None:
        """Initialize a dimmable CompareitLight."""
        self._light = light
        self._uuid = light["uuid"]
        self._attr_name = light["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"

        self._state = "on" if light["value"] > 0 else "off"
        self._brightness = round(light["value"] * 2.55) if light["value"] > 0 else 0
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
        self.hub.SetEntity(self._uuid, round(self._brightness/2.55))
        self.update()

    def turn_off(self) -> None:
        self.hub.SetEntity(self._uuid, 0)
        self._brightness = 0
        self.update()

    def update(self) -> None:
        try:
            newstate = json.loads(self.hub.GetEntity(self._uuid))
            if newstate["value"] > 0:
                self._state = "on"
            elif newstate["value"] == 0:
                self._state = "off"

            self._brightness =  round(newstate["value"] * 2.55)
        except:
            _LOGGER.warning(f"Unable to update {self._attr_name}")

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._hub.hub_id)}}