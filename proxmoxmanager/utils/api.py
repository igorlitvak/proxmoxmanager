from proxmoxer import ProxmoxAPI


class APIWrapper:
    """
    Class that wraps proxmoxer library without changing any returns and only simplifying API endpoint calls
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._proxmoxer = ProxmoxAPI(host=host, user=user, token_name=token_name, token_value=token_value,
                                     verify_ssl=False)
        self._host = host

    @property
    def host(self):
        return self._host

    def get_version(self, **kwargs):
        return self._proxmoxer.version.get(**kwargs)

    def list_users(self, **kwargs):
        return self._proxmoxer.access.users.get(**kwargs)

    def get_user(self, userid: str, **kwargs):
        return self._proxmoxer.access.users(userid).get(**kwargs)

    def create_user(self, userid: str, password: str, **kwargs):
        return self._proxmoxer.access.users.post(userid=userid, password=password, **kwargs)

    def delete_user(self, userid: str, **kwargs):
        return self._proxmoxer.access.users(userid).delete(**kwargs)

    def list_roles(self, **kwargs):
        return self._proxmoxer.access.roles.get(**kwargs)

    def list_permissions(self, **kwargs):
        return self._proxmoxer.access.permissions.get(**kwargs)

    def get_access_control_list(self, **kwargs):
        return self._proxmoxer.access.acl.get(**kwargs)

    def update_access_control_list(self, path: str, roles: str, **kwargs):
        return self._proxmoxer.access.acl.put(path=path, roles=roles, **kwargs)

    def list_nodes(self, **kwargs):
        return self._proxmoxer.nodes.get(**kwargs)

    def get_node_status(self, node: str, **kwargs):
        return self._proxmoxer.nodes(node).status.get(**kwargs)

    def list_resources(self, **kwargs):
        return self._proxmoxer.cluster.resources.get(**kwargs)

    def list_vms(self, node, **kwargs):
        return self._proxmoxer.nodes(node).qemu.get(**kwargs)

    def get_vm_status(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).status.current.get(**kwargs)

    def get_vm_config(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).config.get(**kwargs)

    def delete_vm(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).delete(**kwargs)

    def clone_vm(self, newid: str, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).qemu(vmid).clone.post(newid=newid, **kwargs)

    def list_containers(self, node: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc.get(**kwargs)

    def get_container_status(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).status.current.get(**kwargs)

    def get_container_config(self, node: str, vmid: str, **kwargs):
        return self._proxmoxer.nodes(node).lxc(vmid).config.get(**kwargs)

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
