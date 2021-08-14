from ..api import APIWrapper
from .errors import ProxmoxException
from typing import Dict, Any
from random import choice


class ProxmoxNode:
    def __init__(self, api: APIWrapper, node: str):
        self._api = api
        self._node = node

    @property
    def id(self) -> str:
        """
        :return: Unique ID of node (get-only)
        """
        return self._node

    def online(self) -> bool:
        """
        Check if node is currently online
        :return: True/False
        """
        resp = self._api.list_nodes()
        return any(elem["node"] == self._node for elem in resp if elem["status"] == "online")

    def get_status_report(self) -> Dict[str, Any]:
        """
        Get detailed status info about this node
        :return: Node info in JSON-like format
        """
        return self._api.get_node_status(self._node)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._node}>"

    def __str__(self):
        return self._node


class ProxmoxNodeDict:
    def __init__(self, api: APIWrapper):
        self._api = api
        self._nodes: Dict[str, ProxmoxNode] = {}

    def keys(self):
        self._get_nodes()
        return self._nodes.keys()

    def values(self):
        self._get_nodes()
        return self._nodes.values()

    def items(self):
        self._get_nodes()
        return self._nodes.items()

    def choose_at_random(self, online_only: bool = True) -> ProxmoxNode:
        """
        Choose random node from list of availible nodes
        :param online_only: Only choose between nodes that are currently online (optional, default=True)
        :return: ProxmoxNode object
        """
        valid_choices = [node for node in self.values() if node.online or not online_only]
        if not valid_choices:
            raise ProxmoxException(f"No {'online ' if online_only else ''}nodes found")
        return choice(valid_choices)

    def choose_by_most_free_ram(self, absolute: bool = True, online_only: bool = True):
        """
        Choose from list of availible nodes with most free RAM
        :param absolute: Whether to rate free RAM in bytes or % (optional, default=True)
        :param online_only: Only choose between nodes that are currently online (optional, default=True)
        :return: ProxmoxNode object
        """
        valid_choices = [node for node in self.values() if node.online or not online_only]
        if not valid_choices:
            raise ProxmoxException(f"No {'online ' if online_only else ''}nodes found")
        best_rating = 0.0
        best_node = valid_choices[0]
        for node in valid_choices[1:]:
            memory_info = node.get_status_report()["memory"]
            rating = float(memory_info["free"])
            if not absolute:
                rating /= float(memory_info["total"])
            if rating > best_rating:
                best_node = node
        return best_node

    def __len__(self):
        self._get_nodes()
        return len(self._nodes)

    def __getitem__(self, key: str) -> ProxmoxNode:
        self._get_nodes()
        return self._nodes[key]

    def __repr__(self):
        self._get_nodes()
        return f"<{self.__class__.__name__}: {repr(self._nodes)}>"

    def _get_nodes(self):
        resp = self._api.list_nodes()
        nodes = [ProxmoxNode(self._api, elem["node"]) for elem in resp]
        self._nodes: Dict[str, ProxmoxNode] = {node.id: node for node in nodes}
