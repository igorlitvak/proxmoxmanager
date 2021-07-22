from proxmoxmanager.main import ProxmoxManager, APIWrapper
import unittest
from unittest.mock import patch


class TestProxmoxManager(unittest.TestCase):
    proxmoxmanager = ProxmoxManager(host="0.0.0.0", user="root@pam", token_name="name", token_value="secret")

    def test_list_users(self):
        return_value = [{"userid": "user1@pve", "enable": "1"}, {"userid": "user2@pam", "enable": "0"}]
        with patch.object(APIWrapper, "list_users", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_users(), return_value)
            target_method.assert_called_once_with()

    def test_get_user(self):
        return_value = {"userid": "user1@pve", "enabled": "1"}
        with patch.object(APIWrapper, "get_user", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.get_user(userid="user1@pve"), return_value)
            target_method.assert_called_once_with(userid="user1@pve")

    def test_get_user_without_realm(self):
        return_value = {"userid": "user1@pve", "enabled": "1"}
        with patch.object(APIWrapper, "get_user", return_value=return_value) as target_method, self.assertLogs(
                self.proxmoxmanager._logger) as logs:
            self.assertEqual(self.proxmoxmanager.get_user(userid="user1"), return_value)
            target_method.assert_called_once_with(userid="user1@pve")
            self.assertEqual(len(logs.records), 1)
            self.assertEqual(logs.records[0].getMessage(),
                             "Username user1 doesn't specify realm - \"@pve\" will be appended to username")

    def test_create_user(self):
        return_value = None
        with patch.object(APIWrapper, "create_user", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.create_user(userid="user1@pve", password="12345"), return_value)
            target_method.assert_called_once_with(userid="user1@pve", password="12345")

    def test_create_user_without_realm(self):
        return_value = None
        with patch.object(APIWrapper, "create_user", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.create_user(userid="user1", password="12345"), return_value)
            target_method.assert_called_once_with(userid="user1@pve", password="12345")

    def test_list_resources_without_type(self):
        return_value = [{"id": "qemu/100", "type": "vm"}, {"id": "node/pve", "type": "node"}]
        with patch.object(APIWrapper, "list_resources", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_resources(), return_value)
            target_method.assert_called_once_with()

    def test_list_resources_with_type(self):
        return_value = [{"id": "qemu/100", "type": "vm"}]
        with patch.object(APIWrapper, "list_resources", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_resources(resource_type="vm"), return_value)
            target_method.assert_called_once_with(type="vm")

    def test_list_vms(self):
        return_value = [{"vmid": "100", "name": "foo"}, {"vmid": "101", "name": "bar"}]
        with patch.object(APIWrapper, "list_vms", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_vms(node="node1"), return_value)
            target_method.assert_called_once_with(node="node1")

    def test_get_vm_status(self):
        return_value = {"vmid": "100", "name": "foo"}
        with patch.object(APIWrapper, "get_vm_status", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.get_vm_status(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_delete_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "delete_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.delete_vm(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_clone_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "clone_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.clone_vm(newid="101", node="node1", vmid="100", name="bar",
                                                          target="node2"), return_value)
            target_method.assert_called_once_with(newid="101", node="node1", vmid="100", full="1", name="bar",
                                                  target="node2")

    def test_list_containers(self):
        return_value = [{"vmid": "100", "hostname": "foo"}, {"vmid": "101", "hostname": "bar"}]
        with patch.object(APIWrapper, "list_containers", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_containers(node="node1"), return_value)
            target_method.assert_called_once_with(node="node1")

    def test_get_container_status(self):
        return_value = {"vmid": "100", "hostname": "foo"}
        with patch.object(APIWrapper, "get_container_status", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.get_container_status(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_delete_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "delete_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.delete_container(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_clone_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "clone_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.clone_container(newid="101", node="node1", vmid="100", hostname="bar",
                                                                 target="node2"), return_value)
            target_method.assert_called_once_with(newid="101", node="node1", vmid="100", full="1", hostname="bar",
                                                  target="node2")

    def test_start_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "start_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.start_vm(node="node1", vmid="100", timeout=10), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100", timeout="10")

    def test_stop_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "stop_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.stop_vm(node="node1", vmid="100", timeout=10), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100", timeout="10")

    def test_shutdown_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "shutdown_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.shutdown_vm(node="node1", vmid="100", timeout=10), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100", timeout="10", forceStop="1")

    def test_reset_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "reset_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.reset_vm(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_reboot_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "reboot_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.reboot_vm(node="node1", vmid="100", timeout=10), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100", timeout="10")

    def test_suspend_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "suspend_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.suspend_vm(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100", todisk="0")

    def test_resume_vm(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "resume_vm", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.resume_vm(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_start_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "start_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.start_container(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_stop_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "stop_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.stop_container(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_shutdown_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "shutdown_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.shutdown_container(node="node1", vmid="100", timeout=10), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100", timeout="10", forceStop="1")

    def test_reboot_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "reboot_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.reboot_container(node="node1", vmid="100", timeout=10), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100", timeout="10")

    def test_suspend_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "suspend_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.suspend_container(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_resume_container(self):
        return_value = "TASKID"
        with patch.object(APIWrapper, "resume_container", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.resume_container(node="node1", vmid="100"), return_value)
            target_method.assert_called_once_with(node="node1", vmid="100")

    def test_list_tasks(self):
        return_value = [{"upid": "TASKID1", "status": "stopped"}, {"upid": "TASKID2", "status": "stopped"}]
        with patch.object(APIWrapper, "list_tasks", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.list_tasks(node="node1"), return_value)
            target_method.assert_called_once_with(node="node1")

    def test_get_task_logs(self):
        return_value = ["foo", "bar"]
        with patch.object(APIWrapper, "get_task_logs", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.get_task_logs(node="node1", upid="100"), return_value)
            target_method.assert_called_once_with(node="node1", upid="100")

    def test_get_task_status(self):
        return_value = {"upid": "TASKID1", "status": "stopped"}
        with patch.object(APIWrapper, "get_task_status", return_value=return_value) as target_method:
            self.assertEqual(self.proxmoxmanager.get_task_status(node="node1", upid="100"), return_value)
            target_method.assert_called_once_with(node="node1", upid="100")


if __name__ == "__main__":
    unittest.main()
