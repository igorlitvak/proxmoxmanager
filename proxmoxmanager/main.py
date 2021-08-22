from proxmoxer import ProxmoxAPI
import re
import logging
from typing import Tuple

from proxmoxmanager.utils import *


class ProxmoxManager:
    """
    Smart Proxmox VE API wrapper
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)

    @property
    def nodes(self):
        return ProxmoxNodeDict(self._api)

    @property
    def users(self) -> ProxmoxUserDict:
        return ProxmoxUserDict(self._api)

    @property
    def vms(self) -> ProxmoxVMDict:
        return ProxmoxVMDict(self._api)

    @property
    def containers(self) -> ProxmoxContainerDict:
        return ProxmoxContainerDict(self._api)
