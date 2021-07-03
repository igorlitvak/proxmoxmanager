from proxmoxer import ProxmoxAPI


class ProxmoxManager:

    def __init__(self, host: str, user: str, token_name: str, token_value: str):
        self._api = ProxmoxAPI(host=host, user=user, token_name=token_name, token_value=token_value)
