from typing import Dict, Union

from iag_sdk.client_base import ClientBase


class Netconf(ClientBase):
    """
    Class that contains methods for the IAG Netconf API routes.
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

    def execute_rpc(self, host: str, rpc: str) -> Dict:
        """
        Execute proprietary operations on a device using the NETCONF protocol.

        :param host: Name of device in netconf inventory to execute against.
        :param rpc: Name of RPC operation to be executed on the remote device.
        """
        parameters = {"host": host, "rpc": rpc}
        return self.query(
            "/netconf/exec_rpc/execute", method="post", jsonbody=parameters
        )

    def execute_get_config(
        self,
        host: str,
        filter: str = None,
        lock: bool = False,
        target_datastore: str = "running",
    ) -> Dict:
        """
        Retrieve configuration from a device using the NETCONF protocol

        :param host: Either hostname or ip address accepted.
        :param filter: Optional. An xml string which acts as a filter to restrict the data retrieved from the device.
        :param lock: Optional. Lock the datastore specified in 'target_datastore' (default=False).
        :param target_datastore: Optional. Name of the datastore from which to retrieve configuration data (candidate, running (default), startup).
        """
        parameters = {
            "filter": filter,
            "host": host,
            "lock": lock,
            "target_datastore": target_datastore,
        }
        return self.query(
            "/netconf/get_config/execute", method="post", jsonbody=parameters
        )

    def execute_set_config(
        self,
        host: str,
        config_content: str,
        lock: bool = True,
        save_to_startup: bool = False,
        target_datastore: str = "candidate",
        validate: bool = False,
    ) -> Dict:
        """
        Configure a device using the NETCONF protocol

        :param host: Either hostname or ip address accepted.
        :param config_content: The configuration data in xml string format.
        :param lock: Optional. Lock the datastore specified in 'target_datastore' (default=True).
        :param save_to_startup: Optional. Save the config updates of the datastore specified in 'target_datastore' to the startup-config (default=False).
        :param target_datastore: Optional. Name of the datastore from which to retrieve configuration data (candidate (default), running, startup).
        :param validate: Optional. Validate the config updates of the datastore specified in 'target_datastore' (default=False).
        """
        parameters = {
            "config_content": config_content,
            "host": host,
            "lock": lock,
            "save_to_startup": save_to_startup,
            "target_datastore": target_datastore,
            "validate": validate,
        }
        return self.query(
            "/netconf/set_config/execute", method="post", jsonbody=parameters
        )

    def get_history(
        self,
        netconf_command: str,
        offset: int = 0,
        limit: int = 10,
        order: str = "descending",
    ) -> Dict:
        """
        Get execution log events for Netconf command.
        Tip: Use get_audit_log() and the audit_id returned by this call, to get the details of the execution.

        :param netconf_command: Name of netconf command. Available values : set_config, get_config, exec_rpc
        :param offset: Optional.The number of items to skip before starting to collect the result set.
        :param limit: Optional.The number of items to return (default 10).
        :param order: Optional. Sort indication. Available values : 'ascending', 'descending' (default).
        """
        return self.query(
            f"/netconf/{netconf_command}/history",
            params={"offset": offset, "limit": limit, "order": order},
        )
