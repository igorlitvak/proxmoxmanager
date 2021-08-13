from .api import APIWrapper
from typing import Dict, List, Tuple, Any
from random import choice
from proxmoxer import ProxmoxAPI


# TODO: check that all typehints are correct

class ProxmoxException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ProxmoxNode:
    def __init__(self, api: APIWrapper, node: str):
        self._api = api
        self._node = node

    @property
    def id(self) -> str:
        return self._node

    def online(self) -> bool:
        # TODO: probably could be done with get_status_report
        resp = self._api.list_nodes()
        return any(elem["node"] == self._node for elem in resp if elem["status"] == "online")

    def get_status_report(self) -> Dict[str, Any]:
        """
        Get detailed status info about this node
        :return: Node info in JSON-like format
        """
        return self._api.get_node_status(self._node)

    def __str__(self):
        return self._node


class ProxmoxNodeList:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._nodes: Dict[str, ProxmoxNode] = {node.id: node for node in self._get_nodes()}

    def keys(self):
        return self._nodes.keys()

    def values(self):
        return self._nodes.values()

    def items(self):
        return self._nodes.items()

    def choose_node_random(self, online_only: bool = True) -> ProxmoxNode:
        valid_choices = [node for node in self.values() if node.online or not online_only]
        if not valid_choices:
            raise ProxmoxException(f"No {'online ' if online_only else ''}nodes found")
        return choice(valid_choices)

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, key: str) -> ProxmoxNode:
        return self._nodes[key]

    def _get_nodes(self) -> List[ProxmoxNode]:
        resp = self._api.list_nodes()
        return [ProxmoxNode(self._api, elem["node"]) for elem in resp]


class ProxmoxUser:
    def __init__(self, api: APIWrapper, userid: str):
        self._api = api
        self._userid = userid

    @property
    def id(self) -> str:
        """
        :return: Unique ID of user (get-only)
        """
        return self._userid

    def get_tokens(self, password: str) -> Tuple[str, str]:
        """
        :param password
        :return: Tuple consisting of the authentication and CSRF tokens
        """
        tmp_api = ProxmoxAPI(host=self._api.host, user=self._userid + "@pve", password=password, verify_ssl=False)
        return tmp_api.get_tokens()

    def __str__(self):
        return self._userid


class ProxmoxUserList:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._users: Dict[str, ProxmoxUser] = {user.id: user for user in self._get_users()}

    def keys(self):
        return self._users.keys()

    def values(self):
        return self._users.values()

    def items(self):
        return self._users.items()

    def __len__(self):
        return len(self._users)

    def __getitem__(self, key: str) -> ProxmoxUser:
        return self._users[key]

    def _get_users(self) -> List[ProxmoxUser]:
        resp = self._api.list_users()
        # Only users in @pve realm will be returned
        userid_list = [elem["userid"].split("@")[0] for elem in resp if elem["userid"].split("@")[1] == "pve"]
        return [ProxmoxUser(self._api, userid) for userid in userid_list]


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
        :return: Node on which VM is located (get-only)
        """
        return ProxmoxNode(self._api, self._node)

    def get_status_report(self) -> Dict[str, Any]:
        """
        Get detailed status info about this VM
        :return: Virtual machine info in JSON-like format
        """
        return self._api.get_vm_status(node=self._node, vmid=self._vmid)

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

    def __str__(self):
        return self._vmid


class ProxmoxVMList:
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

    def _get_vms(self) -> List[ProxmoxVM]:
        vms = []
        for node in ProxmoxNodeList(self._api).keys():
            resp = self._api.list_vms(node)
            vms += [ProxmoxVM(self._api, vm["vmid"], node) for vm in resp]
        return vms


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

    def __str__(self):
        return self._vmid


class ProxmoxContainerList:
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

    def _get_containers(self) -> List[ProxmoxContainer]:
        containers = []
        for node in ProxmoxNodeList(self._api).keys():
            resp = self._api.list_containers(node)
            containers += [ProxmoxContainer(self._api, cont["vmid"], node) for cont in resp]
        return containers
