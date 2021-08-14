from proxmoxmanager.utils.classes.nodes import ProxmoxNode, ProxmoxNodeDict
from proxmoxmanager.utils.api import APIWrapper
import unittest
from unittest.mock import patch


class TestProxmoxNode(unittest.TestCase):
    NODE_NAME = "node_name"
    node = ProxmoxNode(api=APIWrapper("example.com:8006", "root@pam", "TOKEN_NAME", "SECRET_VALUE"), node=NODE_NAME)

    def test_id(self):
        self.assertEqual(self.NODE_NAME, self.node.id)

    def test_online_true(self):
        return_value = [{"node": "other_node_name", "status": "online"}, {"node": self.NODE_NAME, "status": "online"}]
        with patch.object(APIWrapper, "list_nodes", return_value=return_value) as target_method:
            self.assertTrue(self.node.online())
            target_method.assert_called_once_with()

    def test_online_false(self):
        return_value = [{"node": "other_node_name", "status": "foo"}, {"node": self.NODE_NAME, "status": "bar"}]
        with patch.object(APIWrapper, "list_nodes", return_value=return_value) as target_method:
            self.assertFalse(self.node.online())
            target_method.assert_called_once_with()

    def test_get_status_report(self):
        return_value = {"memory": {"free": 1000, "used": 24, "total": 1024}, "uptime": 1000}
        with patch.object(APIWrapper, "get_node_status", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.node.get_status_report())
            target_method.assert_called_once_with(node=self.NODE_NAME)

    def test_repr(self):
        self.assertEqual(f"<ProxmoxNode: {self.NODE_NAME}>", repr(self.node))

    def test_str(self):
        self.assertEqual(self.NODE_NAME, str(self.node))


class TestProxmoxNodeList(unittest.TestCase):
    def setUp(self):
        self.RAW_NODE_LIST = [{"node": "node1", "status": "online"}, {"node": "node2", "status": "offline"}]
        self.patcher = patch.object(APIWrapper, "list_nodes", return_value=self.RAW_NODE_LIST)
        self.mock_list_nodes = self.patcher.start()
        self.api = APIWrapper("example.com:8006", "root@pam", "TOKEN_NAME", "SECRET_VALUE")

    def tearDown(self):
        self.patcher.stop()

    def test_get_nodes(self):
        node_dict = ProxmoxNodeDict(api=self.api)
        self.assertEqual({}, node_dict._nodes)
        node_dict._get_nodes()
        self.assertEqual({"node1": ProxmoxNode(self.api, "node1"), "node2": ProxmoxNode(self.api, "node2")},
                         node_dict._nodes)

    # TODO: write more tests


if __name__ == "__main__":
    unittest.main()
