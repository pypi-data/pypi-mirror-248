from typing import Dict, List, Optional, Union

from iag_sdk.client_base import ClientBase


class Group(ClientBase):
    """
    Class that contains methods for the IAG Groups API routes.
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

    def add(
        self,
        group_name: str,
        devices: List[str],
        childGroups: List[str] = None,
        variables: Dict = None,
    ) -> Dict:
        """
        Add a new Ansible device group.

        :param group_name: Name of device group.
        :param devices: List of devices that are part of this group.
        :param childGroups: Optional. Children of this device group.
        :param variables: Optional. Group variables.
        """
        group = {"name": group_name, "devices": devices}
        if childGroups:
            group["childGroups"] = childGroups
        if variables:
            group["variables"] = variables
        return self._make_request("/groups", method="post", jsonbody=group)

    def add_children(self, group_name: str, child_group_list: List[str]) -> Dict:
        """
        Add new child groups to an Ansible device group.

        :param group_name: Name of group.
        :param child_group_list: Child Group List.
        """
        return self._make_request(
            f"/groups/{group_name}/children", method="post", jsonbody=child_group_list
        )

    def add_devices(self, group_name: str, device_list: List[str]) -> Dict:
        """
        Add new devices to an Ansible device group.

        :param group_name: Name of group.
        :param device_list: Device List.
        """
        return self._make_request(
            f"/groups/{group_name}/devices", method="post", jsonbody=device_list
        )

    def delete(self, name: str) -> Dict:
        """
        Delete an Ansible device group.

        :param name: Name of group.
        """
        return self._make_request(f"/groups/{name}", method="delete")

    def delete_child(self, name: str, child_group: str) -> Dict:
        """
        Delete a child group from an Ansible device group.

        :param name: Name of group.
        :param child_group: Name of child group to delete.
        """
        return self._make_request(
            f"/groups/{name}/children/{child_group}", method="delete"
        )

    def delete_device(self, name: str, device: str) -> Dict:
        """
        Delete a device from an Ansible device group.

        :param name: Name of group.
        :param device: Name of device.
        """
        return self._make_request(f"/groups/{name}/devices/{device}", method="delete")

    def get(self, group_name: str) -> Dict:
        """
        Get information for an Ansible device group.

        :param group_name: Name of group.
        """
        return self._make_request(f"/groups/{group_name}")

    def get_children(self, group_name: str) -> Dict:
        """
        Get a list of child groups for an Ansible device group.

        :param group_name: Name of group.
        """
        return self._make_request(f"/groups/{group_name}/children")

    def get_devices(self, group_name: str) -> Dict:
        """
        Get the devices for an Ansible device group.

        :param group_name: Name of group.
        """
        return self._make_request(f"/groups/{group_name}/devices")

    def get_variable(self, group_name: str, variable_name) -> Dict:
        """
        Get the contents of a variable for an Ansible device group.

        :param group_name: Name of group.
        :param variable_name: Name of variable.
        """
        return self._make_request(f"/groups/{group_name}/variables/{variable_name}")

    def get_variables(self, group_name: str) -> Dict:
        """
        Get the variables for an Ansible device group.

        :param group_name: Name of group.
        """
        return self._make_request(f"/groups/{group_name}/variables")

    def get_all(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
    ) -> Dict:
        """
        Get a list of Ansible device groups.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'equals({"name":"asa"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        """
        return self._make_request(
            "/groups",
            params={"offset": offset, "limit": limit, "filter": filter, "order": order},
        )

    def update(self, name: str, config_object: Dict) -> Dict:
        """
        Update the variables in an Ansbile device group.

        :param name: Name of group
        :param config_object: Group variables.
        """
        return self._make_request(
            f"/groups/{name}", method="put", jsonbody=config_object
        )
