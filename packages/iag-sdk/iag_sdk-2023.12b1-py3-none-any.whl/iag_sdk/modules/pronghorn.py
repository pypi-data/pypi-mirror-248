from typing import Dict, Union

from iag_sdk.client_base import ClientBase


class Pronghorn(ClientBase):
    """
    Class that contains methods for the IAG Pronghorn API routes.
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
        Get pronghorn.json for the IAG server.
        """
        return self.query("/pronghorn")
