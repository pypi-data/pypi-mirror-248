import logging

from binsync.api import BSArtifactLifter

l = logging.getLogger(name=__name__)


class GhidraArtifactLifter(BSArtifactLifter):
    lift_map = {}

    def __init__(self, controller):
        super(GhidraArtifactLifter, self).__init__(controller)

    def lift_addr(self, addr: int) -> int:
        #return self.controller.rebase_addr(addr)
        return addr

    def lift_type(self, type_str: str) -> str:
        return type_str

    def lift_stack_offset(self, offset: int, func_addr: int) -> int:
        return offset

    def lower_addr(self, addr: int) -> int:
        #return self.controller.rebase_addr(addr, up=True)
        return addr

    def lower_type(self, type_str: str) -> str:
        return type_str

    def lower_stack_offset(self, offset: int, func_addr: int) -> int:
        return offset
