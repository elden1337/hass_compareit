import logging
from Compare_It import CompareIt
import json

from custom_components.compareit.models.dtos import outputDTO, inputDTO, scenarioDTO, groupDTO

_LOGGER = logging.getLogger(__name__)


class Hub:
    def __init__(self, username, password):
        self.outputs = {}
        self.inputs = {}
        self.scenarios = {}
        self.groups = {}
        self.hub_id = None
        self._api = CompareIt(username, password)
        self.set_lists()

    def get_optional(self, allkeys: dict, name: str, defaultval: any):
        if name in allkeys.keys():
            return allkeys[name]
        else:
            return defaultval

    def set_lists(self):
        all = json.loads(self._api.GetAllEntities())

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
            _target = self.get_optional(i, "target", "")
            _forcetoggle = self.get_optional(i, "forcetoggle", False)
            _priority = self.get_optional(i, "priority", -1)
            _turnon = self.get_optional(i, "turnon", False)

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

    def get_entities(self):
        result = self._api.GetAllEntities()

    async def call_set_smarthome_mode(self):
        pass

    async def call_activate_scenario(self):
        pass