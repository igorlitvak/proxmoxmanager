from proxmoxer import ProxmoxAPI


class ProxmoxManager:
    """
    Smart Proxmox VE API wrapper
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)

    def list_users(self):
        """
        List all users
        :return: List of users in JSON-like format
        """
        return self._api.list_users()

    def get_user(self, userid: str):
        """
        Get specific user by id
        :param userid
        :return: User in JSON-like format
        """
        return self._api.get_user(userid)

    def create_user(self, userid: str, password: str, **kwargs):
        self._api.create_user(userid=userid, password=password, **kwargs)

    def list_nodes(self):
        return self._api.list_nodes()

    def get_node(self, node: str):
        return self._api.get_node(node=node)

    def list_resources(self, resource_type: str = None):
        kwargs = {}
        if resource_type is not None:
            kwargs["type"] = resource_type
        return self._api.list_resources(**kwargs)

    def list_vms(self, node: str):
        return self._api.list_vms(node=node)

    def get_vm(self, node: str, vmid: str):
        return self._api.get_vm(node=node, vmid=vmid)

    def delete_vm(self, node: str, vmid: str):
        self._api.delete_vm(node=node, vmid=vmid)

    def clone_vm(self, newid: str, node: str, vmid: str, name: str = None, full: bool = True, target: str = None):
        kwargs = {"newid": newid, "node": node, "vmid": vmid, "full": '1' if full else '0'}
        if name is not None:
            kwargs["name"] = name
        if target is not None:
            kwargs["target"] = target
        self._api.clone_vm(**kwargs)

    def list_containers(self, node: str):
        return self._api.list_containers(node=node)

    def get_container(self, node: str, vmid: str):
        return self._api.get_container(node=node, vmid=vmid)

    def delete_container(self, node: str, vmid: str):
        self._api.delete_container(node=node, vmid=vmid)

    def clone_container(self, newid: str, node: str, vmid: str, hostname: str = None, full: bool = True,
                        target: str = None):
        kwargs = {"newid": newid, "node": node, "vmid": vmid, "full": '1' if full else '0'}
        if hostname is not None:
            kwargs["hostname"] = hostname
        if target is not None:
            kwargs["target"] = target
        self._api.clone_container(**kwargs)


class APIWrapper:
    """
    Class that wraps proxmoxer library without changing any returns and only simplifying API endpoint calls
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._proxmoxer = ProxmoxAPI(host=host, user=user, token_name=token_name, token_value=token_value,
                                     verify_ssl=False)

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
        self._proxmoxer.nodes(node).qemu.get(**kwargs)

    def get_vm(self, node: str, vmid: str, **kwargs):
        self._proxmoxer.nodes(node).qemu(vmid).get(**kwargs)

    def delete_vm(self, node: str, vmid: str, **kwargs):
        self._proxmoxer.nodes(node).qemu(vmid).delete(**kwargs)

    def clone_vm(self, newid: str, node: str, vmid: str, **kwargs):
        self._proxmoxer.nodes(node).qemu(vmid).clone.post(newid=newid, **kwargs)

    def list_containers(self, node: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc.get(**kwargs)

    def get_container(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).get(**kwargs)

    def delete_container(self, node: str, vmid: str, **kwargs):
        self._proxmoxer.nodes(node).lxc(vmid).delete(**kwargs)

    def clone_container(self, newid: str, node: str, vmid: str, **kwargs):
        self._proxmoxer.nodes(node).lxc(vmid).clone.post(newid=newid, **kwargs)
