from typing import Any, Dict, Union

from iag_sdk.client_base import ClientBase


class Ldap(ClientBase):
    """
    Class that contains methods for the IAG LDAP API routes.
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

    def test(self) -> Any:
        """
        test LDAP connection
        """
        return self.query("/ldap/test_bind", method="post")
