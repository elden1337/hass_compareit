import logging
from Compare_It import CompareIt
import json
from homeassistant.core import HomeAssistant

from custom_components.compareit.models.dtos import outputDTO, inputDTO, scenarioDTO, groupDTO

_LOGGER = logging.getLogger(__name__)


class Hub:
    def __init__(self, username: str, password: str, hass: HomeAssistant):
        self._hass = hass
        self.outputs = {}
        self.inputs = {}
        self.scenarios = {}
        self.groups = {}
        self.hub_id = None
        self._api = CompareIt(username, password)
        self.set_lists()

    def _get_optional(self, allkeys: dict, name: str, defaultval: any):
        if name in allkeys.keys():
            return allkeys[name]
        else:
            return defaultval


    async def GetEntity(self, uuid):
        return self._hass.async_add_executor_job(self._api.GetEntity(uuid))

    async def SetEntity(self, uuid, value):
        return self._hass.async_add_executor_job(self._api.SetEntity(uuid, value))

    async def GetAllEntities(self):
        return self._hass.async_add_executor_job(self._api.GetAllEntities())

    async def set_lists(self):
        all = await self._hass.async_add_executor_job(self._api.GetAllEntities())
        all_json = json.loads(all)

        for o in all["outputs"]:
            self.outputs[o["uuid"]] = outputDTO(
                type=o["type"],
                name=o["name"],
                value=o["value"],
                target=o["target"],
                online=o["online"],
                systemtype=o["systemtype"],
                devicetype=o["devicetype"],
                index=o["index"],
                nodeid=o["nodeid"],
                uuid=o["uuid"],
                nodename=o["nodename"]
            )

        for i in all["inputs"]:
            _target = self._get_optional(i, "target", "")
            _forcetoggle = self._get_optional(i, "forcetoggle", False)
            _priority = self._get_optional(i, "priority", -1)
            _turnon = self._get_optional(i, "turnon", False)

            self.inputs[i["uuid"]] = inputDTO(
                type=i["type"],
                name=i["name"],
                value=i["value"],
                target=_target,
                online=i["online"],
                systemtype=i["systemtype"],
                devicetype=i["devicetype"],
                index=i["index"],
                nodeid=i["nodeid"],
                uuid=i["uuid"],
                nodename=i["nodename"],
                forcetoggle=_forcetoggle,
                priority=_priority,
                turnon=_turnon
            )

        for s in all["scenarios"]:
            self.scenarios[s["uuid"]] = scenarioDTO(
                uuid=s["uuid"],
                name=s["name"],
                dimmerspeed=s["dimmerspeed"],
                private=s["private"],
                order=s["order"],
                attached=s["attached"],
                priority=s["priority"],
                active=s["active"]
            )

        for g in all["groups"]:
            self.groups[g["uuid"]] = groupDTO(
                uuid=g["uuid"],
                name=g["name"],
                order=g["order"],
                color=g["color"],
                private=g["private"],
                category=g["category"],
                objects=[o for o in g["objects"]]
            )

    _states_dict = {}

    async def get_entities(self):
        result = await self._hass.async_add_executor_job(self._api.GetAllEntities())

    async def call_set_smarthome_mode(self):
        pass

    async def call_activate_scenario(self):
        pass