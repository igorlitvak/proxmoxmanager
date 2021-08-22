from proxmoxmanager.utils import APIWrapper, ProxmoxNodeDict, ProxmoxUserDict, ProxmoxVMDict, ProxmoxContainerDict


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
