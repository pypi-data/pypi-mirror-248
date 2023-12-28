from typing import Dict, Union

from iag_sdk.client_base import ClientBase


class Script(ClientBase):
    """
    Class that contains methods for the IAG Scripts API routes.
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

    def delete_schema(self, name: str) -> Dict:
        """
        Remove a script schema.

        :param name: Name of script.
        """
        return self.query(f"/scripts/{name}/schema", method="delete")

    def execute(self, name: str, parameters: Dict) -> Dict:
        """
        Execute a script.
        Tip: Use get_script_schema() to get the format of the parameters object.

        :param name: Name of script to be executed.
        :param parameters: Script Execution Parameters.
        """
        return self.query(
            f"/scripts/{name}/execute", method="post", jsonbody=parameters
        )

    def get(self, name: str) -> Dict:
        """
        Get script information.

        :param name: Name of script to retrieve.
        """
        return self.query(f"/scripts/{name}")

    def get_history(
        self, name: str, offset: int = 0, limit: int = 10, order: str = "descending"
    ) -> Dict:
        """
        Get execution log events for a script.
        Tip: Use get_audit_log() and the audit_id returned by this call, to get the details of the execution.

        :param name: Name of script to retrieve.
        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return.
        :param order: Optional. Sort indication. Available values : ascending, descending (default).
        """
        return self.query(
            f"/scripts/{name}/history",
            params={"offset": offset, "limit": limit, "order": order},
        )

    def get_schema(self, name: str) -> Dict:
        """
        Get the schema for a script.

        :param name: Name of script to retrieve.
        """
        return self.query(f"/scripts/{name}/schema")

    def get_all(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
        detail: str = "summary",
    ) -> Dict:
        """
        Get a list of scripts.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'equals({"name":"sample"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : ascending (default), descending.
        :param detail: Optional. Select detail level between 'full' (a lot of data) or 'summary' for each item.
        """
        return self.query(
            "/scripts",
            params={
                "offset": offset,
                "limit": limit,
                "filter": filter,
                "order": order,
                "detail": detail,
            },
        )

    def refresh(self) -> Dict:
        """
        Perform script discovery and update internal cache.
        """
        return self.query("/scripts/refresh", method="post")

    def update_schema(self, name: str, config_object: Dict) -> Dict:
        """
        Update/Insert a script schema document.
        Tip: Use get_script_schema() to get an idea of the format of the config_object.

        :param name: Name of script.
        :param config_object: Dictionary containing the updated script schema definition.
        """
        return self.query(
            f"/scripts/{name}/schema", method="put", jsonbody=config_object
        )
