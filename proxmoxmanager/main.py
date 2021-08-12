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
        self._host = host
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)
        # self._logger = logging.getLogger(__name__)
        self._node_list = ProxmoxNodeList(self._api)
        self._user_list = ProxmoxUserList(self._api)
        self._vm_list = ProxmoxVMList(self._api)
        self._container_list = ProxmoxContainerList(self._api)

    @property
    def nodes(self):
        return self._node_list

    @property
    def users(self) -> ProxmoxUserList:
        return self._user_list

    @property
    def vms(self) -> ProxmoxVMList:
        return self._vm_list

    @property
    def containers(self) -> ProxmoxContainerList:
        return self._container_list


class SimpleProxmoxManager:
    """
    Smart Proxmox VE API wrapper
    This version is simplified and only consists of methods
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._host = host
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)
        self._logger = logging.getLogger(__name__)

    def list_users(self) -> list:
        """
        List all users
        :return: List of users in JSON-like format
        """
        # TODO
        return self._api.list_users()

    def get_user(self, userid: str) -> dict:
        """
        Get specific user by id
        :param userid: Username in username@pve or username@pam format
        :return: User info in JSON-like format
        """
        # TODO
        userid = self._append_pve_to_userid(userid)
        return self._api.get_user(userid=userid)

    def create_user(self, userid: str, password: str, **kwargs) -> None:
        """
        Create new user
        :param userid: Username in username@pve format
        :param password: Password at least 5 characters long
        :param kwargs: Other arguments passed to Proxmox API
        :return: None
        """
        # TODO
        if not re.match(r"^\w+@pve$", userid):
            userid = userid + "@pve"
        return self._api.create_user(userid=userid, password=password, **kwargs)

    def list_roles(self) -> list:
        """
        List all availible roles on server
        :return: List of roles in JSON-like format
        """
        # TODO
        return self._api.list_roles()

    def get_permissions_for_user(self, userid: str) -> dict:
        """
        List permissions that given user has
        :param userid: Username in username@pve or username@pam format
        :return: User permissions in JSON-like format
        """
        # TODO
        userid = self._append_pve_to_userid(userid)
        return self._api.list_permissions(userid=userid)

    def give_permission_to_user(self, userid: str, role: str, path: str, propagate: bool = False) -> None:
        """
        Give user permission for given path with given role
        :param userid: Username in username@pve or username@pam format
        :param role: Name of role to be added
        :param path: Path to which permission will be applied, for example /vms/100
        :param propagate: Whether to inherit permissions (optional, default=False)
        :return: None
        """
        # TODO
        userid = self._append_pve_to_userid(userid)
        return self._api.update_access_control_list(path=path, roles=role, users=userid, delete="0",
                                                    propagate='1' if propagate else '0')

    def remove_permission_from_user(self, userid: str, role: str, path: str, propagate: bool = False) -> None:
        """
        Remove user permission from given path with given role
        :param userid: Username in username@pve or username@pam format
        :param role: Name of role to be removed
        :param path: Path to which permission will be applied, for example /vms/100
        :param propagate: Whether to inherit permissions (optional, default=False)
        :return: None
        """
        # TODO
        userid = self._append_pve_to_userid(userid)
        return self._api.update_access_control_list(path=path, roles=role, users=userid, delete="1",
                                                    propagate='1' if propagate else '0')

    def get_user_tokens(self, userid: str, password: str) -> Tuple[str, str]:
        """
        :param userid: Username in username@pve or username@pam format
        :param password
        :return: Tuple consisting of the authentication and CSRF tokens
        """
        userid = self._append_pve_to_userid(userid)
        tmp_api = ProxmoxAPI(host=self._host, user=userid, password=password, verify_ssl=False)
        return tmp_api.get_tokens()

    def list_nodes(self) -> list:
        """
        List all nodes
        :return: List of nodes in JSON-like format
        """
        return self._api.list_nodes()

    def get_node_status(self, node: str) -> dict:
        """
        Get specific node by id
        :param node
        :return: Node info in JSON-like format
        """
        # TODO
        return self._api.get_node_status(node=node)

    def list_resources(self, resource_type: str = None) -> list:
        """
        List all resources
        :param resource_type: node | storage | vm | sdn (optional)
        :return: List of resources in JSON-like format
        """
        # TODO
        kwargs = {}
        if resource_type is not None:
            kwargs["type"] = resource_type
        return self._api.list_resources(**kwargs)

    def list_vms(self, node: str) -> list:
        """
        List all virtual machines on node
        :param node
        :return: List of vitrual machines in JSON-like format
        """
        # TODO
        return self._api.list_vms(node=node)

    def get_vm_status(self, node: str, vmid: str) -> dict:
        """
        Get specific virtual machine by id
        :param node
        :param vmid
        :return: Virtual machine info in JSON-like format
        """
        # TODO
        return self._api.get_vm_status(node=node, vmid=vmid)

    def delete_vm(self, node: str, vmid: str) -> str:
        """
        Delete vitrual machine by id
        :param node
        :param vmid
        :return: ID of deleting task
        """
        # TODO
        return self._api.delete_vm(node=node, vmid=vmid)

    def clone_vm(self, newid: str, node: str, vmid: str, name: str = None, full: bool = True,
                 target: str = None) -> str:
        """
        Clone virtual machine
        :param newid: ID of new VM
        :param node: Old node ID
        :param vmid: ID of old VM
        :param name: Name of new VM (optional)
        :param full: Whether to make storage unlinked (optional, default=True)
        :param target: New node ID (optional)
        :return: ID of cloning task
        """
        # TODO
        kwargs = {"newid": newid, "node": node, "vmid": vmid, "full": '1' if full else '0'}
        if name is not None:
            kwargs["name"] = name
        if target is not None:
            kwargs["target"] = target
        return self._api.clone_vm(**kwargs)

    def list_containers(self, node: str) -> list:
        """
        List all LXC containers on node
        :param node
        :return: List of containers in JSON-like format
        """
        # TODO
        return self._api.list_containers(node=node)

    def get_container_status(self, node: str, vmid: str) -> dict:
        """
        Get specific LXC container by id
        :param node
        :param vmid
        :return: Container info in JSON-like format
        """
        # TODO
        return self._api.get_container_status(node=node, vmid=vmid)

    def delete_container(self, node: str, vmid: str) -> str:
        """
        Delete LXC container by id
        :param node
        :param vmid
        :return: ID of deleting task
        """
        # TODO
        return self._api.delete_container(node=node, vmid=vmid)

    def clone_container(self, newid: str, node: str, vmid: str, hostname: str = None, full: bool = True,
                        target: str = None) -> str:
        """
        Clone LXC container
        :param newid: ID of new LXC
        :param node: Old node ID
        :param vmid: ID of old LXC
        :param hostname: Name of new LXC (optional)
        :param full: Whether to make storage unlinked (optional, default=True)
        :param target: New node ID (optional)
        :return: ID of cloning task
        """
        # TODO
        kwargs = {"newid": newid, "node": node, "vmid": vmid, "full": '1' if full else '0'}
        if hostname is not None:
            kwargs["hostname"] = hostname
        if target is not None:
            kwargs["target"] = target
        return self._api.clone_container(**kwargs)

    def start_vm(self, node: str, vmid: str, timeout: int = None) -> str:
        """
        Start virtual machine
        :param node
        :param vmid
        :param timeout: Number of seconds to wait (optional)
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.start_vm(**kwargs)

    def stop_vm(self, node: str, vmid: str, timeout: int = None) -> str:
        """
        Stop virtual machine (unsafely)
        :param node
        :param vmid
        :param timeout: Number of seconds to wait (optional)
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.stop_vm(**kwargs)

    def shutdown_vm(self, node: str, vmid: str, timeout: int = None, force_stop: bool = True) -> str:
        """
        Shutdown virtual machine (safely)
        :param node
        :param vmid
        :param timeout: Number of seconds to wait (optional)
        :param force_stop: Whether to stop a VM if shutdown failed (optional, default=True)
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid, "forceStop": '1' if force_stop else '0'}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.shutdown_vm(**kwargs)

    def reset_vm(self, node: str, vmid: str) -> str:
        """
        Reset virtual machine (unsafely)
        :param node
        :param vmid
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        return self._api.reset_vm(**kwargs)

    def reboot_vm(self, node: str, vmid: str, timeout: int = None) -> str:
        """
        Reboot virtual machine (safely)
        :param node
        :param vmid
        :param timeout: Number of seconds to wait (optional)
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.reboot_vm(**kwargs)

    def suspend_vm(self, node: str, vmid: str, to_disk: bool = False) -> str:
        """
        Suspend virtual machine
        :param node
        :param vmid
        :param to_disk: Whether to suspend VM to disk (optional, defaul=False)
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid, "todisk": '1' if to_disk else '0'}
        return self._api.suspend_vm(**kwargs)

    def resume_vm(self, node: str, vmid: str) -> str:
        """
        Resume virtual machine
        :param node
        :param vmid
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        return self._api.resume_vm(**kwargs)

    def start_container(self, node: str, vmid: str) -> str:
        """
        Start container
        :param node
        :param vmid
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        return self._api.start_container(**kwargs)

    def stop_container(self, node: str, vmid: str) -> str:
        """
        Stop container (unsafely)
        :param node
        :param vmid
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        return self._api.stop_container(**kwargs)

    def shutdown_container(self, node: str, vmid: str, timeout: int = None, force_stop: bool = True) -> str:
        """
        Shutdown container (safely)
        :param node
        :param vmid
        :param timeout: Number of seconds to wait (optional)
        :param force_stop: Whether to stop a container if shutdown failed (optional, default=True)
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid, "forceStop": '1' if force_stop else '0'}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.shutdown_container(**kwargs)

    def reboot_container(self, node: str, vmid: str, timeout: int = None) -> str:
        """
        Reboot container (safely)
        :param node
        :param vmid
        :param timeout: Number of seconds to wait (optional)
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.reboot_container(**kwargs)

    def suspend_container(self, node: str, vmid: str) -> str:
        """
        Suspend container
        WARNING: doesn't appear in Proxmox GUI and probably never works
        :param node
        :param vmid
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        return self._api.suspend_container(**kwargs)

    def resume_container(self, node: str, vmid: str) -> str:
        """
        Resume container
        WARNING: doesn't appear in Proxmox GUI and probably never works
        :param node
        :param vmid
        :return: ID of task
        """
        # TODO
        kwargs = {"node": node, "vmid": vmid}
        return self._api.resume_container(**kwargs)

    def list_tasks(self, node: str) -> list:
        """
        List all finished tasks
        :param node
        :return: List of tasks in JSON-like format
        """
        # TODO
        return self._api.list_tasks(node=node)

    def get_task_logs(self, node: str, upid: str) -> list:
        """
        Get logs for specific task
        :param node
        :param upid
        :return: List of tasks in JSON-like format
        """
        # TODO
        return self._api.get_task_logs(node=node, upid=upid)

    def get_task_status(self, node: str, upid: str) -> dict:
        """
        Get status of specific task
        :param node
        :param upid
        :return: Task status in JSON-like format
        """
        # TODO
        return self._api.get_task_status(node=node, upid=upid)

    def _append_pve_to_userid(self, userid: str):
        """
        Internal method that appends "@pve" to userid if no realm was specified
        :param userid
        :return: userid with realm
        """
        if not (re.match(r"^\w+@pve$", userid) or re.match(r"^\w+@pam$", userid)):
            self._logger.warning(f"Username {userid} doesn't specify realm - \"@pve\" will be appended to username")
            userid = userid + "@pve"
        return userid
