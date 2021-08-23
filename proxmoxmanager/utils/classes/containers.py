from ..api import APIWrapper
from .nodes import ProxmoxNode, ProxmoxNodeDict
from .users import ProxmoxUser
from typing import Dict, List, Tuple, Any, Union


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

    def running(self) -> bool:
        """
        Whether container is currently running
        :return: True/False
        """
        config = self.get_status_report()
        return "status" in config.keys() and config["status"] == "running"

    def is_template(self) -> bool:
        """
        Whether this container is a template
        :return: True/False
        """
        config = self.get_config()
        return "template" in config.keys() and config["template"] == 1

    def clone(self, newid: str, newnode: Union[str, ProxmoxNode] = None, name: str = None, full: bool = True) -> str:
        """
        Clone LXC container
        :param newid: ID of new LXC
        :param newnode: New node ID or ProxmoxNode object (optional)
        :param name: Name of new LXC (optional)
        :param full: Whether to make storage unlinked (note that linked might not be supported) (optional, default=True)
        :return: ID of cloning task
        """
        kwargs = {"newid": newid, "node": self._node, "vmid": self._vmid, "full": '1' if full else '0'}
        if newnode is not None:
            if isinstance(newnode, ProxmoxNode):
                newnode = newnode.id
            kwargs["target"] = newnode
        if name is not None:
            kwargs["hostname"] = name
        return self._api.clone_container(**kwargs)

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

    def view_permissions(self) -> List[Tuple[ProxmoxUser, str]]:
        """
        Get a list of users with permissions for this container and their roles
        :return: List of tuples of ProxmoxUser objects and string names of roles
        """
        path = "/vms/" + self._vmid
        resp = self._api.get_access_control_list()
        return [(ProxmoxUser(self._api, el["ugid"].split("@")[0]), el["roleid"]) for el in resp if
                el["path"] and el["type"] == "user" and el["ugid"].split("@")[1] == "pve" and el["path"] == path]

    def add_permission(self, user: Union[str, ProxmoxUser], role: str) -> None:
        """
        Add new permission for this container
        :param user: User ID or ProxmoxUser object
        :param role: String name of the role
        :return: None
        """
        path = "/vms/" + self._vmid
        if isinstance(user, ProxmoxUser):
            user = user.id
        self._api.update_access_control_list(path=path, roles=role, users=user + "@pve", delete="0", propagate="0")

    def remove_permission(self, user: Union[str, ProxmoxUser], role: str) -> None:
        """
        Remove permission for this container
        :param user: User ID or ProxmoxUser object
        :param role: String name of the role
        :return: None
        """
        path = "/vms/" + self._vmid
        if isinstance(user, ProxmoxUser):
            user = user.id
        self._api.update_access_control_list(path=path, roles=role, users=user + "@pve", delete="1", propagate="0")

    def remove_all_permissions(self) -> None:
        """
        Remove all permissions for this container for all users with any role
        :return: None
        """
        for user, permission in self.view_permissions():
            self.remove_permission(user, permission)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._vmid}>"

    def __str__(self):
        return self._vmid

    def __eq__(self, other: 'ProxmoxContainer'):
        return self._vmid == other._vmid and self._node == other._node


class ProxmoxContainerDict:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._containers: Dict[str, ProxmoxContainer] = {}

    def keys(self):
        self._get_containers()
        return self._containers.keys()

    def values(self):
        self._get_containers()
        return self._containers.values()

    def items(self):
        self._get_containers()
        return self._containers.items()

    def remove(self, vmid: str) -> None:
        """
        Remove container by ID
        :param vmid: Container ID
        :return: None
        """
        self._get_containers()
        self._containers[vmid].delete()

    def __len__(self):
        self._get_containers()
        return len(self._containers)

    def __getitem__(self, key: str) -> ProxmoxContainer:
        self._get_containers()
        return self._containers[key]

    def __iter__(self):
        self._get_containers()
        return iter(self._containers)

    def __repr__(self):
        self._get_containers()
        return f"<{self.__class__.__name__}: {repr(self._containers)}>"

    def _get_containers(self):
        containers = []
        for node in ProxmoxNodeDict(self._api).keys():
            resp = self._api.list_containers(node)
            containers += [ProxmoxContainer(self._api, cont["vmid"], node) for cont in resp]
        self._containers = {cont.id: cont for cont in containers}
