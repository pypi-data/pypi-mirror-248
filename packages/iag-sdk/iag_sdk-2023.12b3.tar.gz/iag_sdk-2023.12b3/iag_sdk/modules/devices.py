from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class Device(ClientBase):
    """
    Class that contains methods for the IAG Devices API routes.
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
        Add a new device to Ansible inventory.
        Tip: Use get_device() to get an idea of the format of the config_object.

        :param config_object: Dictionary containing the device definition.
        """
        return self._make_request(f"/devices", method="post", jsonbody=config_object)

    def delete(self, name: str) -> Dict:
        """
        Delete a device from Ansible inventory.

        :param name: Name of the device.
        """
        return self._make_request(f"/devices/{name}", method="delete")

    def get(self, name: str) -> Dict:
        """
        Get information for an Ansible device.

        :param name: Name of device.
        """
        return self._make_request(f"/devices/{name}")

    def get_state(self, name: str) -> Dict:
        """
        Get the connectivity state for an Ansible device.

        :param name: Name of device.
        """
        return self._make_request(f"/devices/{name}/state")

    def get_variable(self, name: str, variable_name: str) -> Dict:
        """
        Get the value of a connection variable for an Ansible device.

        :param name: Name of device.
        :param variable_name: Name of variable.
        """
        return self._make_request(f"/devices/{name}/variables/{variable_name}")

    def get_variables(self, name: str) -> Dict:
        """
        Get the connection variables for an Ansible device.

        :param name: Name of device.
        """
        return self._make_request(f"/devices/{name}/variables")

    def get_all(self, offset: int = 0, limit: int = 100, filter: str = None) -> Dict:
        """
        Get a list of Ansible devices.

        :param offset: The number of items to skip before starting to collect the result set.
        :param limit: The number of items to return (default 100).
        :param filter: Response filter function with JSON name/value pair argument as string, i.e., 'contains({"name":"SW"})' Valid filter functions - contains, equals, startswith, endswith
        """
        return self._make_request(
            "/devices", params={"offset": offset, "limit": limit, "filter": filter}
        )

    def update(self, name: str, config_object: Dict, method: str = "put") -> Dict:
        """
        Replace the variables for a device in the Ansible inventory.
        Use get_device() to get an idea of the format of the config_object.

        :param name: Name of the device.
        :param config_object: Dictionary containing the variables to be updated.
        :param method: Optional. Choose between 'put' (default) and 'patch'.
        """
        return self._make_request(
            f"/devices/{name}", method=method, jsonbody=config_object
        )
