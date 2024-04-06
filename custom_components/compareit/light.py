from __future__ import annotations
import logging
from typing import Any
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.light import (ATTR_BRIGHTNESS, LightEntity)
from homeassistant.core import HomeAssistant
from datetime import timedelta

from .const import *

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=4)


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry, async_add_entities):
    hub = hass.data[DOMAIN]["hub"]
    result = await hub.async_get_all_entities()

    staticlights = []
    dimmablelights = []
    for light in result.get("outputs", []):
        if light.get(NAME, "").startswith("Belysning") or light.get(NAME,"").startswith("Ytter"):
            typestr = light.get(TYPESTR, 0)
            if typestr == 1:
                staticlights.append(light)
            elif typestr == 2:
                dimmablelights.append(light)

    async_add_entities(CompareItStaticLight(staticlight, hub) for staticlight in staticlights)
    async_add_entities(CompareItDimmableLight(dimmablelight, hub) for dimmablelight in dimmablelights)

class CompareItStaticLight(LightEntity):
    def __init__(self, light, hub) -> None:
        """Initialize a static CompareitLight."""    
        self._uuid = light[UUID]
        self._attr_name = light[NAME]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"
        self._state = None
        self.hub = hub

    @property
    def is_on(self) -> bool:
        return True if self._state == ON else False

    async def async_turn_on(self) -> None:
        await self.hub.async_set_entity(self._uuid, True)
        await self.async_update()

    async def async_turn_off(self) -> None:
        await self.hub.async_set_entity(self._uuid, False)
        await self.async_update()

    async def async_update(self) -> None:
        newstate = await self.hub.async_get_entity(self._uuid)
        self._state = ON if newstate.get(VALUE) else OFF

    @property
    def device_info(self):
        return {
            "identifiers":  {(DOMAIN, 1337)},
            NAME:         "HomeLine",
            "sw_version":   1,
            "model":        2,
            "manufacturer": "Peaq systems",
        }


class CompareItDimmableLight(LightEntity):  
    def __init__(self, light, hub) -> None:
        """Initialize a dimmable CompareitLight."""
        self._light = light
        self._uuid = light[UUID]
        self._attr_name = light[NAME]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"
        self._state = None
        self._brightness = None
        self.hub = hub

    @property
    def brightness(self):
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        return True if self._state == ON else False

    @property
    def supported_features(self):
        return 1 #brightness

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        await self.hub.async_set_entity(self._uuid, round(self._brightness/2.55))
        await self.async_update()

    async def async_turn_off(self) -> None:
        await self.hub.async_set_entity(self._uuid, 0)
        await self.async_update()

    async def async_update(self) -> None:
        newstate = await self.hub.async_get_entity(self._uuid)
        try:
            value = newstate.get(VALUE, -1)
            if value == -1:
                _LOGGER.error(f"Error in async update dimmable light. state: {newstate}")
                return
            if value > 0:
                self._state = ON
            elif value == 0:
                self._state = OFF

            self._brightness =  round(value * 2.55)
        except Exception as e:
            _LOGGER.error(f"Error in async update dimmable light: {e}. state: {newstate}")

    @property
    def device_info(self):
        return {
            "identifiers":  {(DOMAIN, 1337)},
            NAME:         "HomeLine",
            "sw_version":   1,
            "model":        2,
            "manufacturer": "Peaq systems",
        }
