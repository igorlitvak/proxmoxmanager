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

    # TODO: write more tests


# TODO: test ProxmoxContainerDict


if __name__ == "__main__":
    unittest.main()
