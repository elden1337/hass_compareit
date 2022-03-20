from __future__ import annotations
import logging
import json
import voluptuous as vol

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DOMAIN_DATA, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

BINARYSENSOR_TYPE = {
  "Hemma/Borta": "presence",
  "Vattenläckagedetektor": "moisture",
  "Brandlarm": "smoke",
  "Inbrottslarm": "safety"
}

def setup_platform(
   hass: HomeAssistant, config, add_entities: AddEntitiesCallback, discovery_info=None
) -> None:

    hub = hass.data[DOMAIN]["hub"]
    result = json.loads(hub.GetAllEntities())
    
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

    add_entities(CompareItHomeAwayBinarySensor(entity, hub) for entity in homeaways)
    add_entities(CompareItBinarySensor(entity, hub) for entity in entities)


class CompareItBinarySensor(BinarySensorEntity):  
    def __init__(self, switch, hub) -> None:
        """Initialize a Compareit Binary sensor."""

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
    def is_on(self) -> bool | None:
        return True if self._state == "on" else False

    @property
    def device_class(self):
        return BINARYSENSOR_TYPE[self.name]

    def update(self) -> None:
        newstate = json.loads(self.hub.GetEntity(self._uuid))
        if newstate["value"] == True:
            self._state = "on"
        elif newstate["value"] == False:
            self._state = "off"


class CompareItHomeAwayBinarySensor(BinarySensorEntity):  
    def __init__(self, switch, hub) -> None:
        """Initialize a Compareit Binary sensor with dual uuids."""

        self._switch = switch
        self._attr_name = "Hemma/Borta"
        self._uuid_home = switch["home_uuid"]
        self._uuid_away = switch["away_uuid"]
        self._state = "on" if switch["init_value"] == True else "off"
        self.hub = hub

    @property
    def unique_id(self):
        return f"compareit_homeaway"

    @property
    def name(self) -> str:
        return self._attr_name

    @property
    def is_on(self) -> bool | None:
        return True if self._state == "on" else False

    @property
    def device_class(self):
        return BINARYSENSOR_TYPE[self._attr_name]

    def update(self) -> None:
        homestate = json.loads(self.hub.GetEntity(self._uuid_home))
        awaystate = json.loads(self.hub.GetEntity(self._uuid_away))
        if homestate["value"] == True:
            self._state = "on"
        elif awaystate["value"] == True:
            self._state = "off"
