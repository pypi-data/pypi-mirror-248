from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class Collection(ClientBase):
    """
    Class that contains methods for the IAG Collections API routes.
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

    def add(self, config_object: Dict) -> Dict:
        """
        Install an Ansible collection from a Galaxy server or from a tarball.

        :param config_object: Parameters for collection name and Galaxy server authentication.
        """
        return self._make_request(
            "/collections/install", method="post", jsonbody=config_object
        )

    def delete_module_schema(self, collection_name: str, module_name: str) -> Dict:
        """
        Remove a schema for a module in the Ansible collection.

        :param collection_name: Name of collection.
        :param module_name: Name of module.
        """
        return self._make_request(
            f"/collections/{collection_name}/modules/{module_name}/schema",
            method="delete",
        )

    def delete_role_schema(self, collection_name: str, role_name: str) -> Dict:
        """
        Remove a schema for a role in the Ansible collection.

        :param collection_name: Name of collection.
        :param role_name: Name of role.
        """
        return self._make_request(
            f"/collections/{collection_name}/roles/{role_name}/schema", method="delete"
        )

    def get(self, collection_name: str) -> Dict:
        """
        Get details for an Ansible collection.

        :param collection_name: Name of collection to retrieve detail for.
        """
        return self._make_request(f"/collections/{collection_name}")

    def get_module(self, collection_name: str, module_name: str) -> Dict:
        """
        Get details for an Ansible collection.

        :param collection_name: Name of collection to retrieve detail for.
        :param module_name: Name of module to retrieve detail for.
        """
        return self._make_request(
            f"/collections/{collection_name}/modules/{module_name}"
        )

    def get_module_history(
        self,
        collection_name: str,
        module_name: str,
        offset: int = 0,
        limit: int = 10,
        order: str = "descending",
    ) -> Dict:
        """
        Get execution log events for an Ansible collection module.
        Tip: Use get_audit_log() and the audit_id returned by this call, to get the details of the execution.

        :param collection_name: Name of collection.
        :param module_name: Name of module within collection.
        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return.
        :param order: Optional. Sort indication. Available values : 'ascending', 'descending' (default).
        """
        return self._make_request(
            f"/collections/{collection_name}/modules/{module_name}/history",
            params={"offset": offset, "limit": limit, "order": order},
        )

    def get_module_schema(self, collection_name: str, module_name: str) -> Dict:
        """
        Get the schema for a module in the Ansible collection.

        :param collection_name: Name of collection.
        :param module_name: Name of module.
        """
        return self._make_request(
            f"/collections/{collection_name}/modules/{module_name}/schema"
        )

    def get_modules(
        self,
        collection_name: str,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
        detail: str = "summary",
    ) -> Dict:
        """
        Get module list for an Ansible collection.

        :param collection_name: Name of collection to retrieve detail for.
        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'equals({"name":"cisco.asa"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        :param detail: Optional. Select detail level between 'full' (a lot of data) or 'summary' (default) for each item.
        """
        return self._make_request(
            f"/collections/{collection_name}/modules",
            params={
                "offset": offset,
                "limit": limit,
                "filter": filter,
                "order": order,
                "detail": detail,
            },
        )

    def get_role(self, collection_name: str, role_name: str) -> Dict:
        """
        Get details for a role in the Ansible collection.

        :param collection_name: Name of collection to retrieve detail for.
        :param role_name: Name of role to retrieve detail for.
        """
        return self._make_request(f"/collections/{collection_name}/roles/{role_name}")

    def get_role_history(
        self,
        collection_name: str,
        role_name: str,
        offset: int = 0,
        limit: int = 10,
        order: str = "descending",
    ) -> Dict:
        """
        Get execution log events for an Ansible collection role.
        Tip: Use get_audit_log() and the audit_id returned by this call, to get the details of the execution.

        :param collection_name: Name of collection.
        :param role_name: Name of role within collection.
        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return.
        :param order: Optional. Sort indication. Available values : 'ascending', 'descending' (default).
        """
        return self._make_request(
            f"/collections/{collection_name}/roles/{role_name}/history",
            params={"offset": offset, "limit": limit, "order": order},
        )

    def get_role_schema(self, collection_name: str, role_name: str) -> Dict:
        """
        Get the schema for a role in the Ansible collection.

        :param collection_name: Name of collection.
        :param role_name: Name of role.
        """
        return self._make_request(
            f"/collections/{collection_name}/roles/{role_name}/schema"
        )

    def get_roles(
        self,
        collection_name: str,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
        detail: str = "summary",
    ) -> Dict:
        """
        Get role list for an Ansible collection.

        :param collection_name: Name of collection to retrieve detail for.
        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'equals({"name":"cisco.asa"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        :param detail: Optional. Select detail level between 'full' (a lot of data) or 'summary' (default) for each item.
        """
        return self._make_request(
            f"/collections/{collection_name}/roles",
            params={
                "offset": offset,
                "limit": limit,
                "filter": filter,
                "order": order,
                "detail": detail,
            },
        )

    def get_all(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
        detail: str = "summary",
    ) -> Dict:
        """
        Get list of installed Ansible collections.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'equals({"name":"cisco.asa"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        :param detail: Optional. Select detail level between 'full' (a lot! of data) or 'summary' (default) for each item.
        """
        return self._make_request(
            "/collections",
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
        Perform Ansible collection discovery and update internal cache.
        """
        return self._make_request("/collections/refresh", method="post")

    def execute_module(
        self, collection_name: str, module_name: str, parameters: Dict
    ) -> Dict:
        """
        Execute a module contained within the Ansible collection.

        :param collection_name: Name of collection.
        :param module_name: Name of module within collection.
        :param parameters: Module Execution Parameters.
        """
        return self._make_request(
            f"/collections/{collection_name}/modules/{module_name}/execute",
            method="post",
            jsonbody=parameters,
        )

    def execute_role(
        self, collection_name: str, role_name: str, parameters: Dict
    ) -> Dict:
        """
        Execute a module contained within the Ansible collection.

        :param collection_name: Name of collection.
        :param role_name: Name of role within collection.
        :param parameters: Role Execution Parameters.
        """
        return self._make_request(
            f"/collections/{collection_name}/roles/{role_name}/execute",
            method="post",
            jsonbody=parameters,
        )

    def update_module_schema(
        self, collection_name: str, module_name: str, config_object: Dict
    ) -> Dict:
        """
        Update/Insert a schema document for module in the Ansible collection.
        Tip: Use get_collection_module_schema() to get an idea of the format of the config_object.

        :param collection_name: Name of collection.
        :param module_name: Name of module.
        :param config_object: Schema to apply to module identified in path.
        """
        return self._make_request(
            f"/collections/{collection_name}/modules/{module_name}/schema",
            method="put",
            jsonbody=config_object,
        )

    def update_role_schema(
        self, collection_name: str, role_name: str, config_object: Dict
    ) -> Dict:
        """
        Update/Insert a schema document for role in the Ansible collection.
        Tip: Use get_collection_role_schema() to get an idea of the format of the config_object.

        :param collection_name: Name of collection.
        :param role_name: Name of role.
        :param config_object: Schema to apply to module identified in path.
        """
        return self._make_request(
            f"/collections/{collection_name}/roles/{role_name}/schema",
            method="put",
            jsonbody=config_object,
        )
