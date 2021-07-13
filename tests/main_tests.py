from proxmoxmanager.main import ProxmoxManager, APIWrapper
import unittest
from unittest.mock import Mock, patch


class TestProxmoxManager(unittest.TestCase):
    proxmoxmanager = ProxmoxManager(host="0.0.0.0", user="root@pam", token_name="name", token_value="secret")

    def test_list_users(self):
        with patch.object(APIWrapper, "list_users", return_value=["user1", "user2"]):
            self.assertEqual(self.proxmoxmanager.list_users(), ["user1", "user2"])


if __name__ == "__main__":
    unittest.main()