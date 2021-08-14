from ..api import APIWrapper
from proxmoxer import ProxmoxAPI
from typing import Tuple, Dict, List


class ProxmoxUser:
    def __init__(self, api: APIWrapper, userid: str):
        self._api = api
        self._userid = userid

    @property
    def id(self) -> str:
        """
        :return: Unique ID of user (get-only)
        """
        return self._userid

    def get_tokens(self, password: str) -> Tuple[str, str]:
        """
        Get tokens needed to authenticate user
        :param password
        :return: Tuple consisting of the authentication and CSRF tokens
        """
        tmp_api = ProxmoxAPI(host=self._api.host, user=self._userid + "@pve", password=password, verify_ssl=False)
        return tmp_api.get_tokens()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._userid}>"

    def __str__(self):
        return self._userid


class ProxmoxUserDict:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._users: Dict[str, ProxmoxUser] = {user.id: user for user in self._get_users()}

    def keys(self):
        return self._users.keys()

    def values(self):
        return self._users.values()

    def items(self):
        return self._users.items()

    def __len__(self):
        return len(self._users)

    def __getitem__(self, key: str) -> ProxmoxUser:
        return self._users[key]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {repr(self._users)}>"

    def _get_users(self) -> List[ProxmoxUser]:
        resp = self._api.list_users()
        # Only users in @pve realm will be returned
        userid_list = [elem["userid"][:elem["userid"].rindex("@")] for elem in resp if
                       elem["userid"].split("@")[-1] == "pve"]
        return [ProxmoxUser(self._api, userid) for userid in userid_list]
