from proxmoxer import ProxmoxAPI


class ProxmoxManager:
    """
    Smart Proxmox VE API wrapper
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)
        self._api.get_version()  # Ping  # TODO: catch and reraise if exception occurs

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
        return self._api.get_user(userid)

    def create_user(self, userid: str, password: str, **kwargs) -> None:
        """
        Create new user
        :param userid
        :param password
        :param kwargs: Other arguments passed to Proxmox API
        :return: None
        """
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
        return self._api.get_node(node=node)

    def list_resources(self, resource_type: str = None) -> list:
        """
        List all resources
        :param resource_type: node | storage | pool | qemu | lxc | openvz | sdn (optional)
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

    def get_vm(self, node: str, vmid: str) -> dict:
        """
        Get specific virtual machine by id
        :param node
        :param vmid
        :return: Virtual machine info in JSON-like format
        """
        return self._api.get_vm(node=node, vmid=vmid)

    def delete_vm(self, node: str, vmid: str) -> None:
        """
        Delete vitrual machine by id
        :param node
        :param vmid
        :return: None
        """
        return self._api.delete_vm(node=node, vmid=vmid)

    def clone_vm(self, newid: str, node: str, vmid: str, name: str = None, full: bool = True,
                 target: str = None) -> None:
        """
        Clone virtual machine
        :param newid: ID of new VM
        :param node: Old node ID
        :param vmid: ID of old VM
        :param name: Name of new VM (optional)
        :param full: Whether to make storage unlinked (optional, default=True)
        :param target: New node ID (optional)
        :return: None
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

    def get_container(self, node: str, vmid: str) -> dict:
        """
        Get specific LXC container by id
        :param node
        :param vmid
        :return: Container info in JSON-like format
        """
        return self._api.get_container(node=node, vmid=vmid)

    def delete_container(self, node: str, vmid: str) -> None:
        """
        Delete LXC container by id
        :param node
        :param vmid
        :return: None
        """
        return self._api.delete_container(node=node, vmid=vmid)

    def clone_container(self, newid: str, node: str, vmid: str, hostname: str = None, full: bool = True,
                        target: str = None) -> None:
        """
        Clone LXC container
        :param newid: ID of new LXC
        :param node: Old node ID
        :param vmid: ID of old LXC
        :param hostname: Name of new LXC (optional)
        :param full: Whether to make storage unlinked (optional, default=True)
        :param target: New node ID (optional)
        :return: None
        """
        kwargs = {"newid": newid, "node": node, "vmid": vmid, "full": '1' if full else '0'}
        if hostname is not None:
            kwargs["hostname"] = hostname
        if target is not None:
            kwargs["target"] = target
        return self._api.clone_container(**kwargs)


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

    def get_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).get(**kwargs)

    def delete_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).delete(**kwargs)

    def clone_vm(self, newid: str, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).clone.post(newid=newid, **kwargs)

    def list_containers(self, node: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc.get(**kwargs)

    def get_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).get(**kwargs)

    def delete_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).delete(**kwargs)

    def clone_container(self, newid: str, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).clone.post(newid=newid, **kwargs)
