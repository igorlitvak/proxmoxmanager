from .api import APIWrapper


class ProxmoxUser:
    def __init__(self, api: APIWrapper, userid: str, password: str):
        self._api = api
        self._userid = userid
        self._password = password


class ProxmoxUserList:
    def __init__(self, api: APIWrapper):
        self._api = api


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
