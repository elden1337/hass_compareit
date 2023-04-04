import logging
import json
from Compare_It import CompareIt

_LOGGER = logging.getLogger(__name__)

class Hub:
    def __init__(self, hass, username, password):
        self._hass = hass
        self.api = CompareIt(username, password)

    # @property
    # def entities(self) -> dict:
    #     return self._all_entities
    #
    # @entities.setter
    # def entities(self, val) -> None:
    #     self._all_entities = val

    async def async_get_entity(self, uuid):
        ret = await self.api.async_get_entity(uuid)
        if ret:
            return json.loads(ret)
        _LOGGER.error(f"Unable to get entity {uuid}.")

    async def async_set_entity(self, uuid, val) -> None:
        await self.api.async_set_entity(uuid, val)

    async def async_get_all_entities(self):
        ret = await self.api.async_get_all_entities()
        if ret:
            return json.loads(ret)
        _LOGGER.error("Unable to get all entities_async.")

