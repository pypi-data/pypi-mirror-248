from typing import Dict, Union

from iag_sdk.client_base import ClientBase


class Config(ClientBase):
    """
    Class that contains methods for the IAG Config API routes.
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

    def get(self) -> Dict:
        """
        Fetch config value from IAG server database.
        """
        return self.query("/config")

    def update(self, config_object: Dict) -> Dict:
        """
        Update config to AG server database.
        Tip: Use get_config() to get the format of the config_object.

        :param config_object: Updated config object.
        """
        return self.query("/config", method="put", jsonbody=config_object)
