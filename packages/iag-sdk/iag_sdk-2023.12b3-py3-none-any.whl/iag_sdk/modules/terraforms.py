from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class Terraform(ClientBase):
    """
    Class that contains methods for the IAG Terraforms API routes.
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
        Remove a Terraform module schema.

        :param name: Name of the terraform module.
        """
        return self._make_request(f"/terraforms/{name}/schema", method="delete")

    def execute_apply(self, name: str, parameters: Dict) -> Dict:
        """
        Apply the configuration of a Terraform module.

        :param name: Name of terraform module to apply.
        :param parameters: Terraform apply Parameters.
        """
        return self._make_request(
            f"/terraforms/{name}/terraform_apply", method="post", jsonbody=parameters
        )

    def execute_destroy(self, name: str, parameters: Dict) -> Dict:
        """
        Destroy the resources of a Terraform module.

        :param name: Name of terraform module to destroy.
        :param parameters: Terraform destroy Parameters.
        """
        return self._make_request(
            f"/terraforms/{name}/terraform_destroy", method="post", jsonbody=parameters
        )

    def execute_init(self, name: str, parameters: Dict) -> Dict:
        """
        Initialize the providers of a Terraform module.

        :param name: Name of terraform module to init.
        :param parameters: Terraform init Parameters.
        """
        return self._make_request(
            f"/terraforms/{name}/terraform_init", method="post", jsonbody=parameters
        )

    def execute_plan(self, name: str, parameters: Dict) -> Dict:
        """
        Plan the execution of a Terraform module.

        :param name: Name of terraform module to plan.
        :param parameters: Terraform plan Parameters.
        """
        return self._make_request(
            f"/terraforms/{name}/terraform_plan", method="post", jsonbody=parameters
        )

    def execute_validate(self, name: str, parameters: Dict) -> Dict:
        """
        Validate the configuration of a Terraform module.

        :param name: Name of terraform module to validate.
        :param parameters: Terraform validate Parameters.
        """
        return self._make_request(
            f"/terraforms/{name}/terraform_validate", method="post", jsonbody=parameters
        )

    def get(self, name) -> Dict:
        """
        Get information on a Terraform module.

        :param name: Name of the terraform module.
        """
        return self._make_request(f"/terraforms/{name}")

    def get_history(
        self, name: str, offset: int = 0, limit: int = 10, order: str = "descending"
    ) -> Dict:
        """
        Get execution log events for a Terraform module.
        Tip: Use get_audit_log() and the audit_id returned by this call, to get the details of the execution.

        :param name: Name of the terraform module.
        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return.
        :param order: Optional. Sort indication. Available values : ascending, descending (default).
        """
        return self._make_request(
            f"/terraforms/{name}/history",
            params={"offset": offset, "limit": limit, "order": order},
        )

    def get_schema(self, name: str) -> Dict:
        """
        Get the schema for a Terraform module.

        :param name: Name of the terraform module.
        """
        return self._make_request(f"/terraforms/{name}/schema")

    def get_all(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
        detail: str = "summary",
    ) -> Dict:
        """
        Get list of Terraform modules.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. The number of items to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument as string, i.e., 'equals({"name":"sample"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : ascending (default), descending.
        :param detail: Optional. Select detail level between 'full' (a lot of data) or 'summary' for each item.
        """
        return self._make_request(
            "/terraforms",
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
        Perform Terraform discovery and update internal cache.
        """
        return self._make_request(f"/terraforms/refresh", method="post")

    def update_schema(self, name: str, config_object: Dict) -> Dict:
        """
        Update/Insert a Terraform schema document.

        :param name: Name of script.
        :param config_object: Schema to apply to terraform module identified in path.
        """
        return self._make_request(
            f"/terraforms/{name}/schema", method="put", jsonbody=config_object
        )
