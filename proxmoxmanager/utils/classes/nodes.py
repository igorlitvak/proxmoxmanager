from ..api import APIWrapper
from .errors import ProxmoxException
from typing import Dict, Any, List, Tuple
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
        return any(
            elem["node"] == self._node for elem in resp if "status" in elem.keys() and elem["status"] == "online")

    def get_status_report(self) -> Dict[str, Any]:
        """
        Get detailed status info about this node
        :return: Node info in JSON-like format
        """
        return self._api.get_node_status(node=self._node)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._node}>"

    def __str__(self):
        return self._node

    def __eq__(self, other: 'ProxmoxNode'):
        return self._node == other._node


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

    def get_memory_info(self, nodes: List[ProxmoxNode]) -> List[Tuple[ProxmoxNode, float, float]]:
        result = []

        for node in nodes:
            memory_info = node.get_status_report()["memory"]
            rating_abs = float(memory_info["free"])
            rating = rating_abs / float(memory_info["total"])
            result.append((node, rating_abs, rating))

        return result

    def choose_by_most_free_ram(self, absolute: bool = True, online_only: bool = True) -> ProxmoxNode:
        """
        Choose from list of availible nodes with most free RAM
        :param absolute: Whether to rate free RAM in bytes or % (optional, default=True)
        :param online_only: Only choose between nodes that are currently online (optional, default=True)
        :return: ProxmoxNode object
        """
        valid_choices = [node for node in self.values() if node.online or not online_only]
        if not valid_choices:
            raise ProxmoxException(f"No {'online ' if online_only else ''}nodes found")

        memory_info = self.get_memory_info(valid_choices)

        rating_index = 1 if absolute else 2

        nodes_sorted = sorted(memory_info, key=lambda result: result[rating_index], reverse=True)
        best_node_info = nodes_sorted[0]
        best_node = best_node_info[0]

        return best_node

    def __len__(self):
        self._get_nodes()
        return len(self._nodes)

    def __getitem__(self, key: str) -> ProxmoxNode:
        self._get_nodes()
        return self._nodes[key]

    def __iter__(self):
        self._get_nodes()
        return iter(self._nodes)

    def __repr__(self):
        self._get_nodes()
        return f"<{self.__class__.__name__}: {repr(self._nodes)}>"

    def _get_nodes(self):
        resp = self._api.list_nodes()
        nodes = [ProxmoxNode(self._api, elem["node"]) for elem in resp]
        self._nodes: Dict[str, ProxmoxNode] = {node.id: node for node in nodes}
