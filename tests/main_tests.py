from proxmoxmanager.main import ProxmoxManager, APIWrapper
import unittest
from unittest.mock import Mock, patch


class TestProxmoxManager(unittest.TestCase):
    proxmoxmanager = ProxmoxManager(host="0.0.0.0", user="root@pam", token_name="name", token_value="secret")

    def test_list_users(self):
        return_value = [{"userid": "user1", "enable": "1"}, {"userid": "user2", "enable": "0"}]
        with patch.object(APIWrapper, "list_users", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_users(), return_value)
            target_method.assert_called_once_with()

    def test_get_user(self):
        return_value = {"userid": "user1", "enabled": "1"}
        with patch.object(APIWrapper, "get_user", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.get_user(userid="user1"), return_value)
            target_method.assert_called_once_with(userid="user1")

    def test_list_resources_without_type(self):
        return_value = [{"vmid": "100", "type": "qemu"}, {"vmid": "101", "type": "lxc"}]
        with patch.object(APIWrapper, "list_resources", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_resources(), return_value)
            target_method.assert_called_once_with()

    def test_list_resources_with_type(self):
        return_value = [{"vmid": "100", "type": "qemu"}]
        with patch.object(APIWrapper, "list_resources", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_resources(resource_type="qemu"), return_value)
            target_method.assert_called_once_with(type="qemu")

    def test_list_vms(self):
        return_value = [{"vmid": "100", "name": "foo"}, {"vmid": "101", "name": "bar"}]
        with patch.object(APIWrapper, "list_vms", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_vms(node="node1"), return_value)
            target_method.assert_called_once_with(node="node1")

    def test_get_vm(self):
        return_value = {"vmid": "100", "name": "foo"}
        with patch.object(APIWrapper, "get_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.get_vm(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_delete_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "delete_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.delete_vm(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_clone_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "clone_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.clone_vm(newid="101", node="node1", vmid="100", full=True, name="bar",
                                                          target="node2"), return_value)
            target_method.assert_called_once_with(newid="101", node="node1", vmid="100", full="1", name="bar",
                                                  target="node2")

    def test_list_containers(self):
        return_value = [{"vmid": "100", "hostname": "foo"}, {"vmid": "101", "hostname": "bar"}]
        with patch.object(APIWrapper, "list_containers", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_containers(node="node1"), return_value)
            target_method.assert_called_once_with(node="node1")

    def test_get_container(self):
        return_value = {"vmid": "100", "hostname": "foo"}
        with patch.object(APIWrapper, "get_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.get_container(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_delete_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "delete_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.delete_container(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_clone_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "clone_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.clone_container(newid="101", node="node1", vmid="100", full=True,
                                                                 hostname="bar", target="node2"), return_value)
            target_method.assert_called_once_with(newid="101", node="node1", vmid="100", full="1", hostname="bar",
                                                  target="node2")

    # TODO: add tests for power management methods


if __name__ == "__main__":
    unittest.main()
