from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class Module(ClientBase):
    """
    Class that contains methods for the IAG Modules API routes.
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

    def delete_schema(self, name: str) -> Dict:
        """
        Remove an Ansible module schema.

        :param name: Name of module
        """
        return self._make_request(f"/modules/{name}/schema", method="delete")

    def execute(self, name: str, parameters: Dict) -> Dict:
        """
        Execute an Ansible module.
        Tip: Use get_module_schema() to get the format of the parameters object.

        :param name: Name of module to be executed.
        :param parameters: Module Execution Parameters
        """
        return self._make_request(
            f"/modules/{name}/execute", method="post", jsonbody=parameters
        )

    def get(self, name: str) -> Dict:
        """
        Get information for an Ansible module.

        :param name: Name of module to retrieve.
        """
        return self._make_request(f"/modules/{name}")

    def get_history(
        self, name: str, offset: int = 0, limit: int = 10, order: str = "descending"
    ) -> Dict:
        """
        Get execution log events for an Ansible module.
        Tip: Use get_audit_log() and the audit_id returned by this call, to get the details of the execution.

        :param name: Name of module.
        :param offset: Optional.The number of items to skip before starting to collect the result set.
        :param limit: Optional.The number of items to return (default 10).
        :param order: Optional. Sort indication. Available values : 'ascending', 'descending' (default).
        """
        return self._make_request(
            f"/modules/{name}/history",
            params={"offset": offset, "limit": limit, "order": order},
        )

    def get_schema(self, name: str) -> Dict:
        """
        Get the schema for an Ansible module.

        :param name: Name of module to retrieve.
        """
        return self._make_request(f"/modules/{name}/schema")

    def get_all(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
        detail: str = "summary",
    ) -> Dict:
        """
        Get a list of Ansible modules.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'equals({"name":"cisco.asa"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        :param detail: Optional. Select detail level between 'full' (a lot of data) or 'summary' (default) for each item.
        """
        return self._make_request(
            f"/modules",
            params={
                "offset": offset,
                "limit": limit,
                "filter": filter,
                "order": order,
                "detail": detail,
            },
        )

    def update_schema(self, name: str, config_object: Dict) -> Dict:
        """
        Update/Insert an Ansible module schema document.

        :param name: Name of module.
        :param config_object: Dictionary containing the updated module schema definition.
        """
        return self._make_request(
            f"/modules/{name}/schema", method="put", jsonbody=config_object
        )

    def refresh(self) -> Dict:
        """
        Perform Ansible module discovery and update internal cache.
        """
        return self._make_request("/modules/refresh", method="post")
