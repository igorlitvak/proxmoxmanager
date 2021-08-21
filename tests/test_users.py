from proxmoxmanager.utils.classes.users import ProxmoxUser, ProxmoxUserDict
from proxmoxmanager.utils.api import APIWrapper
import unittest
from unittest.mock import patch


class TestProxmoxUser(unittest.TestCase):
    USERID = "testuser"
    user = ProxmoxUser(api=APIWrapper("example.com:8006", "root@pam", "TOKEN_NAME", "SECRET_VALUE"), userid=USERID)

    def test_id(self):
        self.assertEqual(self.USERID, self.user.id)

    def test_get_config(self):
        return_value = {"expire": 0, "email": "testuser@foo.bar", "enable": 1}
        with patch.object(APIWrapper, "get_user", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.user.get_config())
            target_method.assert_called_once_with(userid=self.USERID + "@pve")

    def test_get_tokens(self):
        return_value = ("foooo", "baaar")
        with patch.object(APIWrapper, "get_user_tokens", return_value=return_value) as target_method:
            self.assertEqual(return_value, self.user.get_tokens("12345"))
            target_method.assert_called_once_with(userid=self.USERID + "@pve", password="12345")

    def test_change_password(self):
        with patch.object(APIWrapper, "change_user_password") as target_method:
            self.user.change_password("12345", "foobar")
            target_method.assert_called_once_with(userid=self.USERID + "@pve", old_password="12345",
                                                  new_password="foobar")

    def test_change_password_too_short(self):
        self.assertRaises(ValueError, self.user.change_password, old_password="12345", new_password="1234")

    def test_delete(self):
        with patch.object(APIWrapper, "delete_user") as target_method:
            self.user.delete()
            target_method.assert_called_once_with(userid=self.USERID + "@pve")

    def test_repr(self):
        self.assertEqual(f"<ProxmoxUser: {self.USERID}>", repr(self.user))

    def test_str(self):
        self.assertEqual(self.USERID, str(self.user))


# TODO: test ProxmoxUserDict

if __name__ == "__main__":
    unittest.main()
