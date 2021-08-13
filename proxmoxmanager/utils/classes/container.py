from ..api import APIWrapper
from .node import ProxmoxNode, ProxmoxNodeDict
from typing import Dict, List, Any


class ProxmoxContainer:
    def __init__(self, api: APIWrapper, vmid: str, node: str):
        self._api = api
        self._vmid = vmid
        self._node = node

    @property
    def id(self) -> str:
        """
        :return: Unique ID of container (get-only)
        """
        return self._vmid

    @property
    def node(self) -> ProxmoxNode:
        """
        :return: Node on which containers is located (get-only)
        """
        return ProxmoxNode(self._api, self._node)

    def get_status_report(self) -> Dict[str, Any]:
        """
        Get detailed status info about this container
        :return: Container info in JSON-like format
        """
        return self._api.get_container_status(node=self._node, vmid=self._vmid)

    def get_config(self) -> Dict[str, Any]:
        """
        Get detailed config
        :return: Container config in JSON-like format
        """
        return self._api.get_container_config(node=self._node, vmid=self._vmid)

    def is_template(self) -> bool:
        """
        Whether this container is a template
        :return: True/False
        """
        return self.get_config()["template"] == 1

    def delete(self) -> str:
        """
        Delete this container
        :return: ID of deleting task
        """
        return self._api.delete_container(node=self._node, vmid=self._vmid)

    def start(self) -> str:
        """
        Start container
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        return self._api.start_container(**kwargs)

    def stop(self) -> str:
        """
        Stop container (unsafely)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        return self._api.stop_container(**kwargs)

    def shutdown(self, timeout: int = None, force_stop: bool = True) -> str:
        """
        Shutdown container (safely)
        :param timeout: Number of seconds to wait (optional)
        :param force_stop: Whether to stop a container if shutdown failed (optional, default=True)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid, "forceStop": '1' if force_stop else '0'}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.shutdown_container(**kwargs)

    def reboot(self, timeout: int = None) -> str:
        """
        Reboot container (safely)
        :param timeout: Number of seconds to wait (optional)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.reboot_container(**kwargs)

    def suspend(self) -> str:
        """
        Suspend container
        WARNING: doesn't appear in Proxmox GUI and probably never works
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        return self._api.suspend_container(**kwargs)

    def resume(self) -> str:
        """
        Resume container
        WARNING: doesn't appear in Proxmox GUI and probably never works
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        return self._api.resume_container(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._vmid}>"

    def __str__(self):
        return self._vmid


class ProxmoxContainerDict:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._containers: Dict[str, ProxmoxContainer] = {cont.id: cont for cont in self._get_containers()}

    def keys(self):
        return self._containers.keys()

    def values(self):
        return self._containers.values()

    def items(self):
        return self._containers.items()

    def __len__(self):
        return len(self._containers)

    def __getitem__(self, key: str) -> ProxmoxContainer:
        return self._containers[key]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._containers)}>"

    def _get_containers(self) -> List[ProxmoxContainer]:
        containers = []
        for node in ProxmoxNodeDict(self._api).keys():
            resp = self._api.list_containers(node)
            containers += [ProxmoxContainer(self._api, cont["vmid"], node) for cont in resp]
        return containers
