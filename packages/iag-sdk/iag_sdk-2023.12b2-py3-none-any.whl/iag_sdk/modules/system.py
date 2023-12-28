from typing import Dict, Union

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
        headers: Dict,
        base_url: str = "/api/v2.0",
        protocol: str = "http",
        port: Union[int, str] = 8083,
        verify: bool = True,
    ) -> None:
        super().__init__(host, username, password, headers, base_url, protocol, port, verify)

    def get_audit_log(self, audit_id: str) -> Dict:
        """
        Get execution history payload.

        :param audit_id: Audit id of execution.
        """
        return self.query(f"/exec_history/{audit_id}")

    def get_audit_logs(
        self, offset: int = 0, limit: int = 50, order: str = "descending"
    ) -> Dict:
        """
        Retrieve execution audit logs persisted in the database.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param order: Optional. Sort indication. Available values : 'ascending', 'descending' (default).
        """
        return self.query(
            "/audit", params={"offset": offset, "limit": limit, "order": order}
        )

    def get_health(self) -> Dict:
        """
        Determine if AG server is up and running.
        """
        return self.query("/poll")

    def get_openapi_spec(self) -> Dict:
        """
        Get the current OpenAPI spec from the running instance of IAG
        """
        return self.query("/openapi_spec")

    def get_status(self) -> Dict:
        """
        Get the AG server status (version, ansible version, etc).
        """
        return self.query(f"/status")
