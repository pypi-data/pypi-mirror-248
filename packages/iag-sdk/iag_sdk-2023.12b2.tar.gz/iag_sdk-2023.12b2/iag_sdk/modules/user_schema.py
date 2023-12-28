from typing import Dict, Union

from iag_sdk.client_base import ClientBase


class UserSchema(ClientBase):
    """
    Class that contains methods for the IAG User Schema API routes.
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

    def delete(self, schema_type: str, schema_name: str) -> Dict:
        """
        Remove a user schema.

        :param schema_type: Type of schema.
        :param schema_name: Name of schema.
        """
        return self.query(f"/user-schema/{schema_type}/{schema_name}", method="delete")

    def update(
        self, schema_type: str, schema_name: str, config_object: Dict
    ) -> Dict:
        """
        Update/Insert a user schema document.

        :param schema_type: Type of schema.
        :param schema_name: Name of schema.
        :param config_object: Schema to apply to entity in identified in path.
        """
        return self.query(
            f"/user-schema/{schema_type}/{schema_name}",
            method="put",
            jsonbody=config_object,
        )
