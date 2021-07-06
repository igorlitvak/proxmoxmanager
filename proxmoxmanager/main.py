from proxmoxer import ProxmoxAPI
from .utils import return_default_on_exception


class ProxmoxManager:
    """
    Smart Proxmox VE API wrapper
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._api = APIWrapper(host=host, user=user, token_name=token_name, token_value=token_value)

    def get_users(self):
        """
        List all users
        :return: List of users in JSON-like format
        """
        return self._api.get_users()

    @return_default_on_exception(default_value=None)  # TODO: decorator may be unneeded
    def get_user(self, userid: str):
        """
        Get specific user by id
        :param userid
        :return: User in JSON-like format
        """
        return self._api.get_user(userid)


class APIWrapper:
    """
    Class that wraps proxmoxer library without changing any returns and only simplifying API endpoint calls
    """

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._proxmoxer = ProxmoxAPI(host=host, user=user, token_name=token_name, token_value=token_value)

    def get_users(self):
        return self._proxmoxer.access.users.get()

    def get_user(self, userid: str):
        return self._proxmoxer.access.users[userid].get()
