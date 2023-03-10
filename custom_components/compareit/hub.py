import logging
import json
from Compare_It import CompareIt

_LOGGER = logging.getLogger(__name__)

class Hub:
    def __init__(self, hass, username, password):
        self._hass = hass
        self._compare_it = CompareIt(username, password)
        # self._all_entities = None
        # await self.get_all_entities_async()

    # @property
    # def entities(self) -> dict:
    #     return self._all_entities
    #
    # @entities.setter
    # def entities(self, val) -> None:
    #     self._all_entities = val

    def get_entity(self, uuid):
        ret = self._compare_it.GetEntity(uuid)
        if ret:
            return json.loads(ret)
        _LOGGER.error(f"Unable to get entity {uuid}.")

    def set_entity(self, uuid, val) -> None:
        self._compare_it.SetEntity(uuid, val)

    async def get_all_entities_async(self):
        ret = await self._hass.async_add_executor_job(self._compare_it.GetAllEntities)
        if ret:
            return json.loads(ret)
        _LOGGER.error("Unable to get all entities_async.")
        
    def get_all_entities(self):
        ret = self._compare_it.GetAllEntities()
        if ret:
            return json.loads(ret)
        _LOGGER.error("Unable to get all entities.")
