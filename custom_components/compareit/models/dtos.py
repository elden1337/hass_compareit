from dataclasses import dataclass

@dataclass
class DTO_base:
    uuid: str
    name: str


@dataclass
class outputDTO(DTO_base):
    type: int
    value: any
    online: bool
    systemtype: int
    nodename: str
    nodeid: str
    index: int
    target: any
    devicetype: any


@dataclass
class inputDTO(outputDTO):
    forcetoggle: bool
    priority: int
    turnon: bool


@dataclass
class scenarioDTO(DTO_base):
    dimmerspeed: int
    private: int
    order: int
    attached: list  # uuid is key, target (bool) is value
    priority: int
    active: bool


@dataclass
class groupDTO(DTO_base):
    order: int
    color: int
    private: int
    category: str
    objects: list  # uuid-list