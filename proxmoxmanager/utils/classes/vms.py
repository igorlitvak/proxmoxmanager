from ..api import APIWrapper
from .nodes import ProxmoxNode, ProxmoxNodeDict
from .users import ProxmoxUser
from typing import Dict, List, Tuple, Any, Union


class ProxmoxVM:
    def __init__(self, api: APIWrapper, vmid: str, node: str):
        self._api = api
        self._vmid = vmid
        self._node = node

    @property
    def id(self) -> str:
        """
        :return: Unique ID of VM (get-only)
        """
        return self._vmid

    @property
    def node(self) -> ProxmoxNode:
        """
        Node on which VM is located (get-only)
        :return: ProxmoxNode object
        """
        return ProxmoxNode(self._api, self._node)

    def get_status_report(self) -> Dict[str, Any]:
        """
        Get detailed status info about this VM
        :return: Virtual machine info in JSON-like format
        """
        return self._api.get_vm_status(node=self._node, vmid=self._vmid)

    def get_config(self) -> Dict[str, Any]:
        """
        Get detailed config
        :return: VM config in JSON-like format
        """
        return self._api.get_vm_config(node=self._node, vmid=self._vmid)

    def running(self) -> bool:
        """
        Whether VM is currently running
        :return: True/False
        """
        config = self.get_status_report()
        return "status" in config.keys() and config["status"] == "running"

    def is_template(self) -> bool:
        """
        Whether this VM is a template
        :return: True/False
        """
        config = self.get_config()
        return "template" in config.keys() and config["template"] == 1

    def clone(self, newid: Union[str, int], newnode: Union[str, ProxmoxNode] = None, name: str = None,
              full: bool = True) -> str:
        """
        Clone virtual machine
        :param newid: ID of new VM (integer number 100-999999999)
        :param newnode: New node ID or ProxmoxNode object (optional)
        :param name: Name of new VM (optional)
        :param full: Whether to make storage unlinked (note that linked might not be supported) (optional, default=True)
        :return: ID of cloning task
        """
        try:
            newid = int(newid)
        except ValueError:
            raise ValueError("ID of VM should be an integer between 100 and 999999999")
        if newid < 100 or newid > 999_999_999:
            raise ValueError("ID of VM should be an integer between 100 and 999999999")
        newid = str(newid)
        kwargs = {"newid": newid, "node": self._node, "vmid": self._vmid, "full": '1' if full else '0'}
        if newnode is not None:
            if isinstance(newnode, ProxmoxNode):
                newnode = newnode.id
            kwargs["target"] = newnode
        if name is not None:
            kwargs["name"] = name
        return self._api.clone_vm(**kwargs)

    def delete(self) -> str:
        """
        Delete this VM
        :return: ID of deleting task
        """
        return self._api.delete_vm(node=self._node, vmid=self._vmid)

    def start(self, timeout: int = None) -> str:
        """
        Start virtual machine
        :param timeout: Number of seconds to wait (optional)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.start_vm(**kwargs)

    def stop(self, timeout: int = None) -> str:
        """
        Stop virtual machine (unsafely)
        :param timeout: Number of seconds to wait (optional)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.stop_vm(**kwargs)

    def shutdown(self, timeout: int = None, force_stop: bool = True) -> str:
        """
        Shutdown virtual machine (safely)
        :param timeout: Number of seconds to wait (optional)
        :param force_stop: Whether to stop a VM if shutdown failed (optional, default=True)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid, "forceStop": '1' if force_stop else '0'}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.shutdown_vm(**kwargs)

    def reset(self) -> str:
        """
        Reset virtual machine (unsafely)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        return self._api.reset_vm(**kwargs)

    def reboot(self, timeout: int = None) -> str:
        """
        Reboot virtual machine (safely)
        :param timeout: Number of seconds to wait (optional)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.reboot_vm(**kwargs)

    def suspend(self, to_disk: bool = False) -> str:
        """
        Suspend virtual machine
        :param to_disk: Whether to suspend VM to disk (optional, defaul=False)
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid, "todisk": '1' if to_disk else '0'}
        return self._api.suspend_vm(**kwargs)

    def resume(self) -> str:
        """
        Resume virtual machine
        :return: ID of task
        """
        kwargs = {"node": self._node, "vmid": self._vmid}
        return self._api.resume_vm(**kwargs)

    def view_permissions(self) -> List[Tuple[ProxmoxUser, str]]:
        """
        Get a list of users with permissions for this VM and their roles
        :return: List of tuples of ProxmoxUser objects and string names of roles
        """
        path = "/vms/" + self._vmid
        resp = self._api.get_access_control_list()
        return [(ProxmoxUser(self._api, el["ugid"].split("@")[0]), el["roleid"]) for el in resp if
                el["path"] and el["type"] == "user" and el["ugid"].split("@")[1] == "pve" and el["path"] == path]

    def add_permission(self, user: Union[str, ProxmoxUser], role: str) -> None:
        """
        Add new permission for this VM
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
        Remove permission for this VM
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
        Remove all permissions for this VM for all users with any role
        :return: None
        """
        for user, permission in self.view_permissions():
            self.remove_permission(user, permission)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._vmid}>"

    def __str__(self):
        return self._vmid

    def __eq__(self, other: 'ProxmoxVM'):
        return self._vmid == other._vmid and self._node == other._node


class ProxmoxVMDict:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._vms: Dict[str, ProxmoxVM] = {}

    def keys(self):
        self._get_vms()
        return self._vms.keys()

    def values(self):
        self._get_vms()
        return self._vms.values()

    def items(self):
        self._get_vms()
        return self._vms.items()

    def remove(self, vmid: Union[str, int]) -> None:
        """
        Remove VM by ID
        :param vmid: VM ID
        :return: None
        """
        vmid = str(vmid)
        self._get_vms()
        self._vms[vmid].delete()

    def __len__(self):
        self._get_vms()
        return len(self._vms)

    def __getitem__(self, key: Union[str, int]) -> ProxmoxVM:
        key = str(key)
        self._get_vms()
        return self._vms[key]

    def __iter__(self):
        self._get_vms()
        return iter(self._vms)

    def __repr__(self):
        self._get_vms()
        return f"<{self.__class__.__name__}: {repr(self._vms)}>"

    def _get_vms(self):
        vms = []
        for node in ProxmoxNodeDict(self._api).keys():
            resp = self._api.list_vms(node)
            vms += [ProxmoxVM(self._api, str(vm["vmid"]), node) for vm in resp]
        self._vms = {vm.id: vm for vm in vms}
