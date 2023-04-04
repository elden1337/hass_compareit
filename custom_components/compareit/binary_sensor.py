from __future__ import annotations
import logging
import voluptuous as vol

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from datetime import timedelta
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=20)

BINARYSENSOR_TYPE = {
  "Hemma/Borta": "presence",
  "Vattenläckagedetektor": "moisture",
  "Brandlarm": "smoke",
  "Inbrottslarm": "safety"
}

async def async_setup_entry(hass: HomeAssistant, config, async_add_entities):
    hub = hass.data[DOMAIN]["hub"]
    result = await hub.async_get_all_entities()
    
    homeaway = {
    "home_uuid": '',
    "away_uuid": '',
    "init_value": True
    }
    
    entities = []

    for switch in result["inputs"]:
        if switch["name"].endswith("HOME"):
            homeaway["home_uuid"] = switch["uuid"]
            homeaway["init_value"] = switch["value"]
        elif switch["name"].endswith("AWAY"):
            homeaway["away_uuid"] = switch["uuid"] 
        elif switch["name"] == "Brandlarm" or switch["name"] == "Inbrottslarm" or switch["name"] == "Vattenläckagedetektor":
            entities.append(switch)           

    homeaways = []
    homeaways.append(homeaway)

    async_add_entities(CompareItHomeAwayBinarySensor(entity, hub) for entity in homeaways)
    async_add_entities(CompareItBinarySensor(entity, hub) for entity in entities)


class CompareItBinarySensor(BinarySensorEntity):  
    def __init__(self, switch, hub) -> None:
        """Initialize a Compareit Binary sensor."""
        _LOGGER.info(f"setting up {switch['name']} sensor.")
        self._switch = switch
        self._uuid = switch["uuid"]
        self._attr_name = switch["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid}"
        self._state = "on" if switch["value"] == True else "off"
        self.hub = hub

    @property
    def name(self) -> str:
        return self._attr_name

    @property
    def is_on(self) -> bool:
        return True if self._state == "on" else False

    @property
    def device_class(self):
        return BINARYSENSOR_TYPE[self.name]

    async def async_update(self) -> None:
        newstate = await self.hub.async_get_entity(self._uuid)
        if newstate["value"]:
            self._state = "on"
        elif newstate["value"]:
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


class CompareItHomeAwayBinarySensor(BinarySensorEntity):  
    def __init__(self, switch, hub) -> None:
        """Initialize a Compareit Binary sensor with dual uuids."""
        _LOGGER.info("setting up Home away sensor.")
        self._switch = switch
        self._attr_name = "Hemma/Borta"
        self._uuid_home = switch["home_uuid"]
        self._uuid_away = switch["away_uuid"]
        self._attr_unique_id = f"{DOMAIN}_{self._uuid_home}-{self._uuid_away}"
        self._state = "on" if switch["init_value"] == True else "off"
        self.hub = hub

    @property
    def name(self) -> str:
        return self._attr_name

    @property
    def is_on(self) -> bool:
        return True if self._state == "on" else False

    @property
    def device_class(self):
        return BINARYSENSOR_TYPE[self._attr_name]

    async def async_update(self) -> None:
        homestate = await self.hub.async_get_entity(self._uuid_home)
        awaystate = await self.hub.async_get_entity(self._uuid_away)
        if homestate["value"]:
            self._state = "on"
        elif awaystate["value"]:
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
