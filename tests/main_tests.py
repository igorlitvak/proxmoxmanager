from proxmoxmanager import ProxmoxManager
import unittest


class FooAPIWrapper:
    """
    Placeholder for APIWrapper class that does not require to connect to anything
    """

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_users():
        return [{"userid": "1", "username": "user1"}, {"userid": "2", "username": "user2"}]

    @staticmethod
    def get_user(userid: str):
        users = [{"userid": "1", "username": "user1"}, {"userid": "2", "username": "user2"}]
        return list(filter(lambda u: u["userid"] == userid, users))[0]


class FooProxmoxManager(ProxmoxManager):
    """
    PromoxmoxManager class that is modified to user PlaceholderAPIWrapper
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        # Override parent class initialization
        self._api = FooAPIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)


class TestProxmoxManager(unittest.TestCase):
    """
    Unittest for ProxmoxManagerClass
    """

    def test_get_users(self):
        p = FooProxmoxManager("foo", "bar", "bat", "baz")
        self.assertEqual(p.get_users(), FooAPIWrapper.get_users(), "Method is supposed to return raw data")

    def test_get_user(self):
        p = FooProxmoxManager("foo", "bar", "bat", "baz")
        self.assertEqual(p.get_user("1"), FooAPIWrapper.get_user("1"), "Method is supposed to return raw data")
        self.assertEqual(p.get_user("2"), FooAPIWrapper.get_user("2"), "Method is supposed to return raw data")
        self.assertIsNone(p.get_user("3"), "Method should return None for nonexistent users")


if __name__ == '__main__':
    unittest.main()
