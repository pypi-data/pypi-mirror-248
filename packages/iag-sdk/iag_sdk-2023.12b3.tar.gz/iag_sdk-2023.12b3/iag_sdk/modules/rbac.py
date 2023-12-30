from typing import Dict, List, Optional, Union

from iag_sdk.client_base import ClientBase


class Rbac(ClientBase):
    """
    Class that contains methods for the IAG RBAC API routes.
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

    def add_group(
        self,
        group_name: str,
        roles: List[str],
        users: List[str] = None,
        description: str = None,
    ) -> Dict:
        """
        Add a new RBAC group

        :param group_name: RBAC group name.
        :param roles: List of roles to assign to group.
        :param users: Optional. List of users to assign to group.
        :param description: Optional. Group description.
        """
        parameters = {
            "description": description,
            "name": group_name,
            "roles": roles,
            "users": users,
        }
        return self._make_request("/rbac/groups", method="post", jsonbody=parameters)

    def add_group_roles(self, group_name: str, roles: List[str]) -> Dict:
        """
        Add new roles to the RBAC group.

        :param group_name: RBAC group name.
        :param roles: List of roles to assign to group.
        """
        return self._make_request(
            f"/rbac/groups/{group_name}/roles", method="post", jsonbody={"roles": roles}
        )

    def add_group_users(self, group_name: str, users: List[str]) -> Dict:
        """
        Add new users to the RBAC group.

        :param group_name: RBAC group name.
        :param users: List of users to assign to group.
        """
        return self._make_request(
            f"/rbac/groups/{group_name}/users", method="post", jsonbody={"users": users}
        )

    def delete_group(self, group_name: str) -> Dict:
        """
        Delete an RBAC group.

        :param group_name: RBAC group name.
        """
        return self._make_request(f"/rbac/groups/{group_name}", method="delete")

    def delete_group_role(self, group_name: str, role_name: str) -> Dict:
        """
        Delete a role from the RBAC group.

        :param group_name: RBAC group name.
        :param role_name: Name of role.
        """
        return self._make_request(
            f"/rbac/groups/{group_name}/roles/{role_name}", method="delete"
        )

    def delete_group_user(self, group_name: str, username: str) -> Dict:
        """
        Delete a user from the RBAC group.

        :param group_name: RBAC group name.
        :param username: Name of user.
        """
        return self._make_request(
            f"/rbac/groups/{group_name}/roles/{username}", method="delete"
        )

    def get_group(self, group_name: str) -> Dict:
        """
        Get information for an RBAC group.

        :param group_name: RBAC group name.
        """
        return self._make_request(f"/rbac/groups/{group_name}")

    def get_group_roles(self, group_name: str) -> Dict:
        """
        Get roles for an RBAC group.

        :param group_name: RBAC group name.
        """
        return self._make_request(f"/rbac/groups/{group_name}/roles")

    def get_group_users(self, group_name: str) -> Dict:
        """
        Get users for an RBAC group.

        :param group_name: RBAC group name.
        """
        return self._make_request(f"/rbac/groups/{group_name}/users")

    def get_groups(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
    ) -> Dict:
        """
        Get a list of RBAC groups.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'contains({"name":"admin"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        """
        return self._make_request(
            f"/rbac/groups",
            params={"offset": offset, "limit": limit, "filter": filter, "order": order},
        )

    def get_role(self, role_name: str) -> Dict:
        """
        Get information for an RBAC role.

        :param role_name: Name of RBAC role.
        """
        return self._make_request(f"/rbac/roles/{role_name}")

    def get_roles(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
    ) -> Dict:
        """
        Get a list of RBAC roles.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'contains({"name":"admin"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        """
        return self._make_request(
            f"/rbac/roles",
            params={"offset": offset, "limit": limit, "filter": filter, "order": order},
        )

    def get_user_groups(
        self,
        username: str,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
    ) -> Dict:
        """
        Get RBAC group information for a user.

        :param username: Name of user.
        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'contains({"name":"admin"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        """
        return self._make_request(
            f"/rbac/users/{username}/groups",
            params={"offset": offset, "limit": limit, "filter": filter, "order": order},
        )

    def get_user_roles(
        self,
        username: str,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
    ) -> Dict:
        """
        Get RBAC role information for a user.

        :param username: Name of user.
        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'contains({"name":"admin"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        """
        return self._make_request(
            f"/rbac/users/{username}/roles",
            params={"offset": offset, "limit": limit, "filter": filter, "order": order},
        )

    def update_group(
        self,
        group_name: str,
        roles: List[str] = None,
        users: List[str] = None,
        description: str = None,
    ) -> Dict:
        """
        Update an RBAC group

        :param group_name: RBAC group name.
        :param roles: Optional. List of roles to assign to group.
        :param users: Optional. List of users to assign to group.
        :param description: Optional. Group description.
        """
        parameters = {"description": description, "roles": roles, "users": users}
        return self._make_request(
            f"/rbac/groups/{group_name}", method="put", jsonbody=parameters
        )
