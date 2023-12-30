from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class System(ClientBase):
    """
    Class that contains methods for the IAG System API routes.
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

    def get_audit_log(self, audit_id: str) -> Dict:
        """
        Get execution history payload.

        :param audit_id: Audit id of execution.
        """
        return self._make_request(f"/exec_history/{audit_id}")

    def get_audit_logs(
        self, offset: int = 0, limit: int = 50, order: str = "descending"
    ) -> Dict:
        """
        Retrieve execution audit logs persisted in the database.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param order: Optional. Sort indication. Available values : 'ascending', 'descending' (default).
        """
        return self._make_request(
            "/audit", params={"offset": offset, "limit": limit, "order": order}
        )

    def get_health(self) -> Dict:
        """
        Determine if AG server is up and running.
        """
        return self._make_request("/poll")

    def get_openapi_spec(self) -> Dict:
        """
        Get the current OpenAPI spec from the running instance of IAG
        """
        return self._make_request("/openapi_spec")

    def get_status(self) -> Dict:
        """
        Get the AG server status (version, ansible version, etc).
        """
        return self._make_request(f"/status")
