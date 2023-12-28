from typing import Dict, Union

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
        headers: Dict,
        base_url: str = "/api/v2.0",
        protocol: str = "http",
        port: Union[int, str] = 8083,
        verify: bool = True,
    ) -> None:
        super().__init__(host, username, password, headers, base_url, protocol, port, verify)

    def add(self, path: str, config_object: Dict) -> Dict:
        """
        Add a new Hashicorp Vault secret.

        :param path: Name of secret path.
        :param config_object: Secret definition {"path": path, "secret_data": {}}
        """
        return self.query(
            "/secrets", method="post", params={"path": path}, jsonbody=config_object
        )

    def delete(self, path: str) -> Dict:
        """
        Delete a Hashicorp Vault secret.

        :param path: Name of secret path.
        """
        return self.query("/secrets", method="delete", params={"path": path})

    def get(self, path: str) -> Dict:
        """
        Get a list of Hashicorp Vault secrets.

        :param path: Name of secret path.
        """
        return self.query("/secrets", params={"path": path})

    def update(self, path: str, config_object: Dict) -> Dict:
        """
        Updata a Hashicorpy Vault secret.

        :param path: Name of secret path.
        :param config_object: Secret data key/value pairs
        """
        return self.query(
            "/secrets", method="put", params={"path": path}, jsonbody=config_object
        )
