from ..api import APIWrapper
from .node import ProxmoxNode, ProxmoxNodeDict
from typing import Dict, List, Any


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

    def is_template(self) -> bool:
        """
        Whether this VM is a template
        :return: True/False
        """
        return self.get_config()["template"] == 1

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

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._vmid}>"

    def __str__(self):
        return self._vmid


class ProxmoxVMDict:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._vms: Dict[str, ProxmoxVM] = {vm.id: vm for vm in self._get_vms()}

    def keys(self):
        return self._vms.keys()

    def values(self):
        return self._vms.values()

    def items(self):
        return self._vms.items()

    def __len__(self):
        return len(self._vms)

    def __getitem__(self, key: str) -> ProxmoxVM:
        return self._vms[key]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._vms)}>"

    def _get_vms(self) -> List[ProxmoxVM]:
        vms = []
        for node in ProxmoxNodeDict(self._api).keys():
            resp = self._api.list_vms(node)
            vms += [ProxmoxVM(self._api, vm["vmid"], node) for vm in resp]
        return vms
