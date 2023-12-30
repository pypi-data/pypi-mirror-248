from typing import Dict, Optional, Union

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
        base_url: Optional[str] = "/api/v2.0",
        protocol: Optional[str] = "http",
        port: Optional[Union[int, str]] = 8083,
        verify: Optional[bool] = True,
        session = None,
        token: Optional[str] = None
    ) -> None:
        super().__init__(host, username, password, base_url, protocol, port, verify, session, token)

    def get(self) -> Dict:
        """
        Fetch config value from IAG server database.
        """
        return self._make_request("/config")

    def update(self, config_object: Dict) -> Dict:
        """
        Update config to AG server database.
        Tip: Use get_config() to get the format of the config_object.

        :param config_object: Updated config object.
        """
        return self._make_request("/config", method="put", jsonbody=config_object)
