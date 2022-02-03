from __future__ import annotations
import logging
import json
import voluptuous as vol

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DOMAIN_DATA, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

def setup_platform(
   hass: HomeAssistant, config, add_entities: AddEntitiesCallback, discovery_info=None
) -> None:

    hub = hass.data[DOMAIN_DATA]["hub"]
    outputs = json.loads(hub.GetAllEntities())

    entity = {
    "home_uuid": '',
    "away_uuid": '',
    "init_value": True
    }

    for switch in outputs["outputs"]:
        if switch["name"].startswith("OUT"):
            if switch["name"].endswith("HOME"):
                entity["home_uuid"] = switch["uuid"]
                entity["init_value"] = switch["value"]
            else:
                entity["away_uuid"] = switch["uuid"]     

    entities = []
    entities.append(entity)

    add_entities(CompareItBinarySensor(entity, hub) for entity in entities)

class CompareItBinarySensor(BinarySensorEntity):  
    def __init__(self, switch, hub) -> None:
        """Initialize a Compareit Binary sensor."""

        self._switch = switch
        self._name = "Hemma/Borta"
        self._uuid_home = switch["home_uuid"]
        self._uuid_away = switch["away_uuid"]
        self._state = "on" if switch["init_value"] == True else "off"
        self.hub = hub

    @property
    def unique_id(self):
        return f"compareit_homeaway"

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool | None:
        return True if self._state == "on" else False

    @property
    def device_class(self):
        return "presence"

    def update(self) -> None:
        homestate = json.loads(self.hub.GetEntity(self._uuid_home))
        awaystate = json.loads(self.hub.GetEntity(self._uuid_away))
        if homestate["value"] == True:
            self._state = "on"
        elif awaystate["value"] == True:
            self._state = "off"
