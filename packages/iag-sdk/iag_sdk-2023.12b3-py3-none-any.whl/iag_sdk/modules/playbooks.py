from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class Playbook(ClientBase):
    """
    Class that contains methods for the IAG Playbooks API routes.
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
        Remove an Ansible playbook schema.

        :param name: Name of playbook.
        """
        return self._make_request(f"/playbooks/{name}/schema", method="delete")

    def execute(self, name: str, parameters: Dict, dry_run: bool = False) -> Dict:
        """
        Execute an Ansible playbook.
        Tip: Use get_playbook_schema() to get the format of the parameters object.

        :param name: Name of playbook to be executed.
        :param parameters: Playbook Execution Parameters.
        :param dry_run: Optional. Set to True to run playbook in check mode (dry run).
        """
        if dry_run:
            return self._make_request(
                f"/playbooks/{name}/dry_run", method="post", jsonbody=parameters
            )
        else:
            return self._make_request(
                f"/playbooks/{name}/execute", method="post", jsonbody=parameters
            )

    def get(self, name: str) -> Dict:
        """
        Get information for an Ansible playbook.

        :param name: Name of playbook to retrieve.
        """
        return self._make_request(f"/playbooks/{name}")

    def get_history(
        self, name: str, offset: int = 0, limit: int = 10, order: str = "descending"
    ) -> Dict:
        """
        Get execution log events for an Ansible playbook.
        Tip: Use get_audit_log() and the audit_id returned by this call, to get the details of the execution.

        :param name: Name of playbook to retrieve.
        :param offset: Optional. The number of items to skip before starting to collect the result set (default 0).
        :param limit: Optional. The number of items to return (default 10).
        :param order: Optional. Sort indication. Available values : ascending, descending (default).
        """
        return self._make_request(
            f"/playbooks/{name}/history",
            params={"offset": offset, "limit": limit, "order": order},
        )

    def get_schema(self, name: str) -> Dict:
        """
        Get the schema for an Ansible playbook.

        :param name: Name of playbook to retrieve.
        """
        return self._make_request(f"/playbooks/{name}/schema")

    def get_all(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
        detail: str = "summary",
    ) -> Dict:
        """
        Get a list of Ansible playbooks.

        :param offset: Optional. The number of items to skip before starting to collect the result set (default 0).
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'equals({"name":"sample"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : ascending (default), descending.
        :param detail: Optional. Select detail level between 'full' (a lot of data) or 'summary' for each item.
        """
        return self._make_request(
            "/playbooks",
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
        Perform Ansible playbook discovery and update internal cache.
        """
        return self._make_request("/playbooks/refresh", method="post")

    def update_schema(self, name: str, config_object: Dict) -> Dict:
        """
        Update/Insert an Ansible playbook schema document.
        Tip: Use get_playbook_schema() to get an idea of the format of the config_object.

        :param name: Name of playbook.
        :param config_object: Dictionary containing the updated playbook schema definition.
        """
        return self._make_request(
            f"/playbooks/{name}/schema", method="put", jsonbody=config_object
        )
