from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class Secret(ClientBase):
    """
    Class that contains methods for the IAG Secrets API routes.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        base_url: Optional[str] = "/api/v2.0",
        protocol: Optional[str] = "http",
        port: Optional[Union[int, str]] = 8083,
        verify: Optional[bool] = True,
        session = None,
        token: Optional[str] = None
    ) -> None:
        super().__init__(host, username, password, base_url, protocol, port, verify, session, token)

    def add(self, path: str, config_object: Dict) -> Dict:
        """
        Add a new Hashicorp Vault secret.

        :param path: Name of secret path.
        :param config_object: Secret definition {"path": path, "secret_data": {}}
        """
        return self._make_request(
            "/secrets", method="post", params={"path": path}, jsonbody=config_object
        )

    def delete(self, path: str) -> Dict:
        """
        Delete a Hashicorp Vault secret.

        :param path: Name of secret path.
        """
        return self._make_request("/secrets", method="delete", params={"path": path})

    def get(self, path: str) -> Dict:
        """
        Get a list of Hashicorp Vault secrets.

        :param path: Name of secret path.
        """
        return self._make_request("/secrets", params={"path": path})

    def update(self, path: str, config_object: Dict) -> Dict:
        """
        Updata a Hashicorpy Vault secret.

        :param path: Name of secret path.
        :param config_object: Secret data key/value pairs
        """
        return self._make_request(
            "/secrets", method="put", params={"path": path}, jsonbody=config_object
        )
