from ..api import APIWrapper
from typing import Tuple, Dict, Any


class ProxmoxUser:
    def __init__(self, api: APIWrapper, userid: str):
        self._api = api
        self._userid = userid
        self._fulluserid = userid + "@pve"

    @property
    def id(self) -> str:
        """
        :return: Unique ID of user (get-only)
        """
        return self._userid

    def get_config(self) -> Dict[str, Any]:
        """
        Get detailed config
        :return: User config in JSON-like format
        """
        return self._api.get_user(userid=self._fulluserid)

    def get_tokens(self, password: str) -> Tuple[str, str]:
        """
        Get tokens needed to authenticate user
        :param password
        :return: Tuple consisting of the authentication and CSRF tokens
        """
        return self._api.get_user_tokens(userid=self._fulluserid, password=password)

    def change_password(self, old_password: str, new_password: str) -> None:
        """
        Change this user's password
        :param old_password: Current password (can't be retrieved via API)
        :param new_password: New password at least 5 characters long
        :return: None
        """
        if len(new_password) < 5:
            raise ValueError(f"Password has to be at least 5 characters long")
        self._api.change_user_password(userid=self._fulluserid, old_password=old_password, new_password=new_password)

    def delete(self) -> None:
        """
        Delete this user
        :return: None
        """
        self._api.delete_user(userid=self._fulluserid)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._userid}>"

    def __str__(self):
        return self._userid

    def __eq__(self, other: 'ProxmoxUser'):
        return self._userid == other._userid


class ProxmoxUserDict:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._users: Dict[str, ProxmoxUser] = {}

    def keys(self):
        self._get_users()
        return self._users.keys()

    def values(self):
        self._get_users()
        return self._users.values()

    def items(self):
        self._get_users()
        return self._users.items()

    def create(self, user: str, password: str, **kwargs) -> ProxmoxUser:
        """
        Create new user
        :param user: Unique user ID
        :param password: Password at least 5 characters long
        :param kwargs: Other arguments passed to Proxmox API (comment, firstname, lastname, email...)
        :return: ProxmoxUser object for newly created user
        """
        self._get_users()
        if user in self._users.keys():
            raise ValueError(f"User {user} already exists")
        if len(password) < 5:
            raise ValueError(f"Password has to be at least 5 characters long")
        self._api.create_user(userid=user + "@pve", password=password, **kwargs)
        return ProxmoxUser(self._api, user)

    def remove(self, user: str) -> None:
        """
        Remove user by ID
        :param user: User ID
        :return: None
        """
        self._get_users()
        self._users[user].delete()

    def __len__(self):
        self._get_users()
        return len(self._users)

    def __getitem__(self, key: str) -> ProxmoxUser:
        self._get_users()
        return self._users[key]

    def __repr__(self):
        self._get_users()
        return f"<{self.__class__.__name__}: {repr(self._users)}>"

    def _get_users(self):
        resp = self._api.list_users()
        # Only users in @pve realm will be returned
        userid_list = [el["userid"][:el["userid"].rindex("@")] for el in resp if el["userid"].split("@")[-1] == "pve"]
        users = [ProxmoxUser(self._api, userid) for userid in userid_list]
        self._users: Dict[str, ProxmoxUser] = {user.id: user for user in users}
