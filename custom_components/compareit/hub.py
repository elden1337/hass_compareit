import logging
import json
from Compare_It import CompareIt

_LOGGER = logging.getLogger(__name__)

class Hub:
    def __init__(self, hass, username, password):
        self._hass = hass
        self.api = CompareIt(username, password)

    async def async_get_entity(self, uuid):
        try:
            ret = await self.api.async_get_entity(uuid)
            if ret:
                return ret
        except Exception as e:
            _LOGGER.error(f"Unable to get entity {uuid}. Exception: {e}")

    async def async_set_entity(self, uuid, val) -> None:
        await self.api.async_set_entity(uuid, val)

    async def async_get_all_entities(self):
        try:
            ret = await self.api.async_get_all_entities()
            if ret:
                return ret
        except Exception as e:
            _LOGGER.error(f"Unable to get all entities. Exception: {e}")

