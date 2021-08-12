from .api import APIWrapper
from typing import Dict, List, Tuple
from random import choice
from proxmoxer import ProxmoxAPI


class ProxmoxException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ProxmoxNode:
    def __init__(self, api: APIWrapper, node: str):
        self._api = api
        self._node = node

    @property
    def id(self) -> str:
        return self._node

    @property
    def online(self) -> bool:
        # TODO
        return True

    def __str__(self):
        return self.id


class ProxmoxNodeList:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._nodes: Dict[str, ProxmoxNode] = {node.id: node for node in self._get_nodes()}

    def keys(self):
        return self._nodes.keys()

    def values(self):
        return self._nodes.values()

    def items(self):
        return self._nodes.items()

    def choose_node_random(self, online_only: bool = True) -> ProxmoxNode:
        valid_choices = [node for node in self.values() if node.online or not online_only]
        if not valid_choices:
            raise ProxmoxException(f"No {'online ' if online_only else ''}nodes found")
        return choice(valid_choices)

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, key: str) -> ProxmoxNode:
        return self._nodes[key]

    def _get_nodes(self) -> List[ProxmoxNode]:
        resp = self._api.list_nodes()
        return [ProxmoxNode(self._api, elem["node"]) for elem in resp]


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

    def get_user_tokens(self, password: str) -> Tuple[str, str]:
        """
        :param password
        :return: Tuple consisting of the authentication and CSRF tokens
        """
        tmp_api = ProxmoxAPI(host=self._api.host, user=self._userid, password=password, verify_ssl=False)
        return tmp_api.get_tokens()

    def __str__(self):
        return self.id


class ProxmoxUserList:
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

    def _get_users(self) -> List[ProxmoxUser]:
        resp = self._api.list_users()
        # Only users in @pve realm will be returned
        userid_list = [elem["userid"].split("@")[0] for elem in resp if elem["userid"].split("@")[1] == "pve"]
        return [ProxmoxUser(self._api, userid) for userid in userid_list]


class ProxmoxVM:
    def __init__(self, api: APIWrapper, vmid: str, node: str):
        self._api = api
        self._vmid = vmid
        self._node = node


class ProxmoxVMList:
    def __init__(self, api: APIWrapper):
        self._api = api


class ProxmoxContainer:
    def __init__(self, api: APIWrapper, vmid: str, node: str):
        self._api = api
        self._vmid = vmid
        self._node = node


class ProxmoxContainerList:
    def __init__(self, api: APIWrapper):
        self._api = api
