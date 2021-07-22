from proxmoxer import ProxmoxAPI


class ProxmoxManager:
    """
    Smart Proxmox VE API wrapper
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)

    def list_users(self) -> list:
        """
        List all users
        :return: List of users in JSON-like format
        """
        return self._api.list_users()

    def get_user(self, userid: str) -> dict:
        """
        Get specific user by id
        :param userid
        :return: User info in JSON-like format
        """
        # TODO: append @pve to username if it doesn't have realm
        return self._api.get_user(userid=userid)

    def create_user(self, userid: str, password: str, **kwargs) -> None:
        """
        Create new user
        :param userid
        :param password
        :param kwargs: Other arguments passed to Proxmox API
        :return: None
        """
        # TODO: check that username looks like username@pve
        # TODO: ckeck that password is 5+ characters long
        return self._api.create_user(userid=userid, password=password, **kwargs)

    def list_nodes(self) -> list:
        """
        List all nodes
        :return: List of nodes in JSON-like format
        """
        return self._api.list_nodes()

    def get_node(self, node: str) -> dict:
        """
        Get specific node by id
        :param node
        :return: Node info in JSON-like format
        """
        # FIXME: change API endpoint or delete method
        return self._api.get_node(node=node)

    def list_resources(self, resource_type: str = None) -> list:
        """
        List all resources
        :param resource_type: node | storage | vm | sdn (optional)
        :return: List of resources in JSON-like format
        """
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
        return self._api.list_vms(node=node)

    def get_vm_status(self, node: str, vmid: str) -> dict:
        """
        Get specific virtual machine by id
        :param node
        :param vmid
        :return: Virtual machine info in JSON-like format
        """
        return self._api.get_vm_status(node=node, vmid=vmid)

    def delete_vm(self, node: str, vmid: str) -> str:
        """
        Delete vitrual machine by id
        :param node
        :param vmid
        :return: ID of deleting task
        """
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
        return self._api.list_containers(node=node)

    def get_container_status(self, node: str, vmid: str) -> dict:
        """
        Get specific LXC container by id
        :param node
        :param vmid
        :return: Container info in JSON-like format
        """
        return self._api.get_container_status(node=node, vmid=vmid)

    def delete_container(self, node: str, vmid: str) -> str:
        """
        Delete LXC container by id
        :param node
        :param vmid
        :return: ID of deleting task
        """
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
        kwargs = {"node": node, "vmid": vmid, "todisk": '1' if to_disk else '0'}
        return self._api.suspend_vm(**kwargs)

    def resume_vm(self, node: str, vmid: str) -> str:
        """
        Resume virtual machine
        :param node
        :param vmid
        :return: ID of task
        """
        kwargs = {"node": node, "vmid": vmid}
        return self._api.resume_vm(**kwargs)

    def start_container(self, node: str, vmid: str) -> str:
        """
        Start container
        :param node
        :param vmid
        :return: ID of task
        """
        kwargs = {"node": node, "vmid": vmid}
        return self._api.start_container(**kwargs)

    def stop_container(self, node: str, vmid: str) -> str:
        """
        Stop container (unsafely)
        :param node
        :param vmid
        :return: ID of task
        """
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
        kwargs = {"node": node, "vmid": vmid}
        if timeout is not None:
            kwargs["timeout"] = str(timeout)
        return self._api.reboot_container(**kwargs)

    def suspend_container(self, node: str, vmid: str) -> str:
        """
        Suspend container
        :param node
        :param vmid
        :return: ID of task
        """
        # TODO: doesn't seem to work
        kwargs = {"node": node, "vmid": vmid}
        return self._api.suspend_container(**kwargs)

    def resume_container(self, node: str, vmid: str) -> str:
        """
        Resume container
        :param node
        :param vmid
        :return: ID of task
        """
        kwargs = {"node": node, "vmid": vmid}
        return self._api.resume_container(**kwargs)

    def list_tasks(self, node: str) -> list:
        """
        List all finished tasks
        :param node
        :return: List of tasks in JSON-like format
        """
        return self._api.list_tasks(node=node)

    def get_task_logs(self, node: str, upid: str) -> list:
        """
        Get logs for specific task
        :param node
        :param upid
        :return: List of tasks in JSON-like format
        """
        return self._api.get_task_logs(node=node, upid=upid)

    def get_task_status(self, node: str, upid: str) -> dict:
        """
        Get status of specific task
        :param node
        :param upid
        :return: Task status in JSOB-like format
        """
        return self._api.get_task_status(node=node, upid=upid)


class APIWrapper:
    """
    Class that wraps proxmoxer library without changing any returns and only simplifying API endpoint calls
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._proxmoxer = ProxmoxAPI(host=host, user=user, token_name=token_name, token_value=token_value,
                                     verify_ssl=False)

    def get_version(self):
        return self._proxmoxer.version.get()

    def list_users(self, **kwargs):
        return self._proxmoxer.access.users.get(**kwargs)

    def get_user(self, userid: str, **kwargs):
        return self._proxmoxer.access.users(userid).get(**kwargs)

    def create_user(self, userid: str, password: str, **kwargs):
        return self._proxmoxer.access.users.post(userid=userid, password=password, **kwargs)

    def list_nodes(self):
        return self._proxmoxer.nodes.get()

    def get_node(self, node: str, **kwargs):
        return self._proxmoxer.nodes(node).get(**kwargs)

    def list_resources(self, **kwargs):
        return self._proxmoxer.cluster.resources.get(**kwargs)

    def list_vms(self, node, **kwargs):
        return self._proxmoxer.nodes(node).qemu.get(**kwargs)

    def get_vm_status(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.current.get(**kwargs)

    def delete_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).delete(**kwargs)

    def clone_vm(self, newid: str, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).clone.post(newid=newid, **kwargs)

    def list_containers(self, node: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc.get(**kwargs)

    def get_container_status(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).status.current.get(**kwargs)

    def delete_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).delete(**kwargs)

    def clone_container(self, newid: str, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).clone.post(newid=newid, **kwargs)

    def start_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.start.post(**kwargs)

    def stop_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.stop.post(**kwargs)

    def shutdown_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.shutdown.post(**kwargs)

    def reset_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.reset.post(**kwargs)

    def reboot_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.reboot.post(**kwargs)

    def suspend_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.suspend.post(**kwargs)

    def resume_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.resume.post(**kwargs)

    def start_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).status.start.post(**kwargs)

    def stop_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).status.stop.post(**kwargs)

    def shutdown_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).status.shutdown.post(**kwargs)

    def reboot_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).status.reboot.post(**kwargs)

    def suspend_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).status.suspend.post(**kwargs)

    def resume_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).status.resume.post(**kwargs)

    def list_tasks(self, node: str, **kwargs):
        return self._proxmoxer.nodes(node).tasks.get(**kwargs)

    def get_task_logs(self, node: str, upid: str, **kwargs):
        return self._proxmoxer.nodes(node).tasks(upid).log.get(**kwargs)

    def get_task_status(self, node: str, upid: str, **kwargs):
        return self._proxmoxer.nodes(node).tasks(upid).status.get(**kwargs)
