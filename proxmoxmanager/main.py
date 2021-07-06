from proxmoxer import ProxmoxAPI
from .utils import return_default_on_exception


class ProxmoxManager:

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)

    def get_users(self):
        return self._api.get_users()


class APIWrapper:

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._proxmoxer = ProxmoxAPI(host=host, user=user, token_name=token_name, token_value=token_value)

    def get_users(self):
        return self._proxmoxer.access.users.get()
