from proxmoxmanager.utils import APIWrapper, ProxmoxNodeDict, ProxmoxUserDict, ProxmoxVMDict, ProxmoxContainerDict
from typing import List, Dict, Any


class ProxmoxManager:
    """
    Smart Proxmox VE API wrapper
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)

    @property
    def nodes(self):
        """
        Get all nodes
        :return: Dict-like object containing nodes
        """
        return ProxmoxNodeDict(self._api)

    @property
    def users(self) -> ProxmoxUserDict:
        """
        Get all users
        :return: Dict-like object containing users
        """
        return ProxmoxUserDict(self._api)

    @property
    def vms(self) -> ProxmoxVMDict:
        """
        Get all virtual machines
        :return: Dict-like object containing virtual machines
        """
        return ProxmoxVMDict(self._api)

    @property
    def containers(self) -> ProxmoxContainerDict:
        """
        Get all containers
        :return: Dict-like object containing containers
        """
        return ProxmoxContainerDict(self._api)

    def list_roles(self) -> List[Dict[str, Any]]:
        """
        Get list of availible roles
        :return: List of roles' info in JSON-like format
        """
        return self._api.list_roles()

    def list_role_names(self):
        """
        Get list of names of avalible roles (without any other info)
        :return: List of string role names
        """
        return [role["roleid"] for role in self.list_roles()]

    def smallest_free_vmid(self) -> str:
        """
        Get smallest VM/container ID that is not taken
        :return: ID in string format
        """
        # TODO: test it
        vmids = list(self.vms.keys())
        vmids += list(self.containers.keys())
        vmids.sort()
        # TODO: maybe it is better to use some fancy algorithm
        res = 100
        for vmid in vmids:
            if vmid == str(res):
                res += 1
            else:
                return str(res)
        return str(res)
