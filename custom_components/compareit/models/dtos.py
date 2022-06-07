from dataclasses import dataclass

@dataclass
class DTO_base:
    uuid: str
    type: int
    name: str
    value: any
    online: bool
    systemtype: int
    nodename: str
    nodeid: str
    index: int
    target: any
    devicetype: any


@dataclass
class outputDTO(DTO_base):
    pass


@dataclass
class inputDTO(DTO_base):
    forcetoggle: bool
    priority: int
    turnon: bool


@dataclass
class scenarioDTO:
    uuid: str
    name: str
    dimmerspeed: int
    private: int
    order: int
    attached: list  # uuid is key, target (bool) is value
    priority: int
    active: bool


@dataclass
class groupDTO:
    uuid: str
    name: str
    order: int
    color: int
    private: int
    category: str
    objects: list  # uuid-list