from proxmoxmanager.utils.classes.vms import ProxmoxVM, ProxmoxVMDict
from proxmoxmanager.utils.api import APIWrapper
import unittest
from unittest.mock import patch


class TestProxmoxVM(unittest.TestCase):
    VMID = "100"
    NODE_NAME = "node_name"
    vm = ProxmoxVM(api=APIWrapper("example.com:8006", "root@pam", "TOKEN_NAME", "SECRET_VALUE"), vmid=VMID,
                   node=NODE_NAME)

    def test_id(self):
        self.assertEqual(self.VMID, self.vm.id)

    def test_node(self):
        self.assertEqual(self.NODE_NAME, self.vm.node.id)

    def test_get_status_report(self):
        return_value = {"status": "running", "maxdisk": 1000000, "maxmem": 100000}
        with patch.object(APIWrapper, "get_vm_status", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.vm.get_status_report())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_get_config(self):
        return_value = {"name": "foo", "cores": 4, "memory": 1024}
        with patch.object(APIWrapper, "get_vm_config", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.vm.get_config())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_is_template_true(self):
        return_value = {"name": "foo", "cores": 4, "memory": 1024, "template": 1}
        with patch.object(APIWrapper, "get_vm_config", return_value=return_value) as target_method:
            self.assertTrue(self.vm.is_template())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_is_template_false(self):
        return_value = {"name": "foo", "cores": 4, "memory": 1024}
        with patch.object(APIWrapper, "get_vm_config", return_value=return_value) as target_method:
            self.assertFalse(self.vm.is_template())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_view_permissions(self):
        return_value = [{"ugid": "foo@pve", "roleid": "Role1", "path": "/vms/100", "type": "user"},
                        {"ugid": "bar@pve", "roleid": "Role2", "path": "/vms/100", "type": "user"}]
        with patch.object(APIWrapper, "get_access_control_list", return_value=return_value) as target_method:
            perm = self.vm.view_permissions()
            self.assertEqual(2, len(perm))
            self.assertEqual("foo", perm[0][0].id)
            self.assertEqual("Role1", perm[0][1])
            self.assertEqual("bar", perm[1][0].id)
            self.assertEqual("Role2", perm[1][1])
            target_method.assert_called_once_with()

    def test_view_permissions_other_data(self):
        return_value = [{"ugid": "foo@pve", "roleid": "Role", "path": "/vms/101", "type": "user"},
                        {"ugid": "root@pam", "roleid": "Role", "path": "/vms/100", "type": "user"},
                        {"ugid": "token1", "roleid": "Role", "path": "/vms/100", "type": "token"},
                        {"ugid": "foo@pve", "roleid": "Role", "path": "/vms", "type": "user"},
                        {"ugid": "foo@pve", "roleid": "Role", "path": "/nodes/100", "type": "user"}]
        with patch.object(APIWrapper, "get_access_control_list", return_value=return_value) as target_method:
            self.assertEqual([], self.vm.view_permissions())
            target_method.assert_called_once_with()

    def test_add_permission(self):
        with patch.object(APIWrapper, "update_access_control_list") as target_method:
            self.vm.add_permission(user="foo", role="Role")
            target_method.assert_called_once_with(path="/vms/" + self.VMID, roles="Role", users="foo@pve", delete="0",
                                                  propagate="0")

    def test_remove_permission(self):
        with patch.object(APIWrapper, "update_access_control_list") as target_method:
            self.vm.remove_permission(user="foo", role="Role")
            target_method.assert_called_once_with(path="/vms/" + self.VMID, roles="Role", users="foo@pve", delete="1",
                                                  propagate="0")

    def test_remove_all_permissions(self):
        return_value = [{"ugid": "foo@pve", "roleid": "Role1", "path": "/vms/100", "type": "user"},
                        {"ugid": "bar@pve", "roleid": "Role2", "path": "/vms/100", "type": "user"}]
        with patch.object(APIWrapper, "get_access_control_list", return_value=return_value) as target_method1, \
                patch.object(ProxmoxVM, "remove_permission") as target_method2:
            self.assertEqual(None, self.vm.remove_all_permissions())
            target_method1.assert_called_once_with()
            self.assertEqual(2, target_method2.call_count)

    # TODO: write more tests


# TODO: test ProxmoxVMDict


if __name__ == "__main__":
    unittest.main()
