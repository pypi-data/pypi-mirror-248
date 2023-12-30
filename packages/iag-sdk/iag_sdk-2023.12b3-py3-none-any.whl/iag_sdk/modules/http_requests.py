from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class HttpRequest(ClientBase):
    """
    Class that contains methods for the IAG HTTP Requests API routes.
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

    def execute(self, parameters: Dict) -> Dict:
        """
        Send an HTTP/1.1 request to an inventory device.

        :param parameters: Parameters required to send your request. See the Requests library for all other supported parameters: https://docs.python-requests.org/en/latest/api/
        """
        return self._make_request(
            "/http_requests/request/execute", method="post", jsonbody=parameters
        )

    def get_history(
        self, offset: int = 0, limit: int = 10, order: str = "descending"
    ) -> Dict:
        """
        Get execution log events for an HTTP request.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 10).
        :param order: Optional. Sort indication. Available values : 'ascending', 'descending' (default).
        """
        return self._make_request(
            "/http_requests/request/history",
            params={"offset": offset, "limit": limit, "order": order},
        )

    def get_schema(self) -> Dict:
        """
        Get the json schema for http_requests' request endpoint.
        """
        return self._make_request("/http_requests/request/schema")
