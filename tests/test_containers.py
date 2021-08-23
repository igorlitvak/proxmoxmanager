from proxmoxmanager.utils.classes.containers import ProxmoxContainer, ProxmoxContainerDict
from proxmoxmanager.utils.api import APIWrapper
import unittest
from unittest.mock import patch


class TestProxmoxContainer(unittest.TestCase):
    VMID = "100"
    NODE_NAME = "node_name"
    container = ProxmoxContainer(api=APIWrapper("example.com:8006", "root@pam", "TOKEN_NAME", "SECRET_VALUE"),
                                 vmid=VMID, node=NODE_NAME)

    def test_id(self):
        self.assertEqual(self.VMID, self.container.id)

    def test_node(self):
        self.assertEqual(self.NODE_NAME, self.container.node.id)

    def test_get_status_report(self):
        return_value = {"status": "running", "maxdisk": 1000000, "maxmem": 100000}
        with patch.object(APIWrapper, "get_container_status", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.container.get_status_report())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_get_config(self):
        return_value = {"hostname": "foo", "cores": 4, "memory": 1024}
        with patch.object(APIWrapper, "get_container_config", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.container.get_config())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_running_true(self):
        return_value = {"status": "running", "maxdisk": 1000000, "maxmem": 100000}
        with patch.object(APIWrapper, "get_container_status", return_value=return_value) as target_method:
            self.assertTrue(self.container.running())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_running_false(self):
        return_value = {"status": "stopped", "maxdisk": 1000000, "maxmem": 100000}
        with patch.object(APIWrapper, "get_container_status", return_value=return_value) as target_method:
            self.assertFalse(self.container.running())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_is_template_true(self):
        return_value = {"hostname": "foo", "cores": 4, "memory": 1024, "template": 1}
        with patch.object(APIWrapper, "get_container_config", return_value=return_value) as target_method:
            self.assertTrue(self.container.is_template())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_is_template_false(self):
        return_value = {"hostname": "foo", "cores": 4, "memory": 1024}
        with patch.object(APIWrapper, "get_container_config", return_value=return_value) as target_method:
            self.assertFalse(self.container.is_template())
            target_method.assert_called_once_with(vmid=self.VMID, node=self.NODE_NAME)

    def test_clone(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "clone_container", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.container.clone(newid="101", newnode="other_node_name", name="foo"))
            target_method.assert_called_once_with(newid="101", node=self.NODE_NAME, vmid=self.VMID, full="1",
                                                  hostname="foo", target="other_node_name")

    def test_clone_id_not_int(self):
        self.assertRaises(ValueError, self.container.clone, newid="foo")

    def test_clone_id_too_small(self):
        self.assertRaises(ValueError, self.container.clone, newid=99)
        self.assertRaises(ValueError, self.container.clone, newid="99")

    def test_clone_id_too_big(self):
        self.assertRaises(ValueError, self.container.clone, newid=1_000_000_000)
        self.assertRaises(ValueError, self.container.clone, newid="1000000000")

    def test_delete(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "delete_container", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.container.delete())
            target_method.assert_called_once_with(node=self.NODE_NAME, vmid=self.VMID)

    def test_start(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "start_container", return_value=return_value) as target_method:
            self.assertEqual(self.container.start(), return_value)
            target_method.assert_called_once_with(node=self.NODE_NAME, vmid=self.VMID)

    def test_stop(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "stop_container", return_value=return_value) as target_method:
            self.assertEqual(self.container.stop(), return_value)
            target_method.assert_called_once_with(node=self.NODE_NAME, vmid=self.VMID)

    def test_shutdown(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "shutdown_container", return_value=return_value) as target_method:
            self.assertEqual(self.container.shutdown(timeout=10), return_value)
            target_method.assert_called_once_with(node=self.NODE_NAME, vmid=self.VMID, timeout="10", forceStop="1")

    def test_reboot(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "reboot_container", return_value=return_value) as target_method:
            self.assertEqual(self.container.reboot(timeout=10), return_value)
            target_method.assert_called_once_with(node=self.NODE_NAME, vmid=self.VMID, timeout="10")

    def test_suspend(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "suspend_container", return_value=return_value) as target_method:
            self.assertEqual(self.container.suspend(), return_value)
            target_method.assert_called_once_with(node=self.NODE_NAME, vmid=self.VMID)

    def test_resume(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "resume_container", return_value=return_value) as target_method:
            self.assertEqual(self.container.resume(), return_value)
            target_method.assert_called_once_with(node=self.NODE_NAME, vmid=self.VMID)

    def test_view_permissions(self):
        return_value = [{"ugid": "foo@pve", "roleid": "Role1", "path": "/vms/100", "type": "user"},
                        {"ugid": "bar@pve", "roleid": "Role2", "path": "/vms/100", "type": "user"}]
        with patch.object(APIWrapper, "get_access_control_list", return_value=return_value) as target_method:
            perm = self.container.view_permissions()
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
            self.assertEqual([], self.container.view_permissions())
            target_method.assert_called_once_with()

    def test_add_permission(self):
        with patch.object(APIWrapper, "update_access_control_list") as target_method:
            self.container.add_permission(user="foo", role="Role")
            target_method.assert_called_once_with(path="/vms/" + self.VMID, roles="Role", users="foo@pve", delete="0",
                                                  propagate="0")

    def test_remove_permission(self):
        with patch.object(APIWrapper, "update_access_control_list") as target_method:
            self.container.remove_permission(user="foo", role="Role")
            target_method.assert_called_once_with(path="/vms/" + self.VMID, roles="Role", users="foo@pve", delete="1",
                                                  propagate="0")

    def test_remove_all_permissions(self):
        return_value = [{"ugid": "foo@pve", "roleid": "Role1", "path": "/vms/100", "type": "user"},
                        {"ugid": "bar@pve", "roleid": "Role2", "path": "/vms/100", "type": "user"}]
        with patch.object(APIWrapper, "get_access_control_list", return_value=return_value) as target_method1, \
                patch.object(ProxmoxContainer, "remove_permission") as target_method2:
            self.assertEqual(None, self.container.remove_all_permissions())
            target_method1.assert_called_once_with()
            self.assertEqual(2, target_method2.call_count)


# TODO: test ProxmoxContainerDict


if __name__ == "__main__":
    unittest.main()
