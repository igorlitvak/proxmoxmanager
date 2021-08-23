from proxmoxmanager.main import ProxmoxManager
from proxmoxmanager.utils.api import APIWrapper
import unittest
from unittest.mock import patch


class TestProxmoxManager(unittest.TestCase):
    proxmox_manager = ProxmoxManager("example.com:8006", "root@pam", "TOKEN_NAME", "SECRET_VALUE")

    def test_nodes(self):
        nodes = self.proxmox_manager.nodes
        self.assertTrue(nodes._api is self.proxmox_manager._api)
        self.assertEqual({}, nodes._nodes)

    def test_users(self):
        users = self.proxmox_manager.users
        self.assertTrue(users._api is self.proxmox_manager._api)
        self.assertEqual({}, users._users)

    def test_vms(self):
        vms = self.proxmox_manager.vms
        self.assertTrue(vms._api is self.proxmox_manager._api)
        self.assertEqual({}, vms._vms)

    def test_containers(self):
        containers = self.proxmox_manager.containers
        self.assertTrue(containers._api is self.proxmox_manager._api)
        self.assertEqual({}, containers._containers)

    def test_list_roles(self):
        return_value = [{"roleid": "Role1", "special": 1, "privs": "priv1, priv2"},
                        {"roleid": "Role2", "special": 1, "privs": "priv2, priv3"}]
        with patch.object(APIWrapper, "list_roles", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.proxmox_manager.list_roles())
            target_method.assert_called_once_with()

    def test_list_role_names(self):
        return_value = [{"roleid": "Role1", "special": 1, "privs": "priv1, priv2"},
                        {"roleid": "Role2", "special": 1, "privs": "priv2, priv3"}]
        with patch.object(APIWrapper, "list_roles", return_value=return_value) as target_method:
            self.assertEqual(["Role1", "Role2"], self.proxmox_manager.list_role_names())
            target_method.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
