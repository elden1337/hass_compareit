import logging

class Hub:
    def __init__(self):
        self._compare_it = None

    def get_entity(self, uuid):
        self._compare_it.GetEntity(self._uuid)

    def set_entity(self, uuid, val):
        self._compare_it.SetEntity(uuid, val)