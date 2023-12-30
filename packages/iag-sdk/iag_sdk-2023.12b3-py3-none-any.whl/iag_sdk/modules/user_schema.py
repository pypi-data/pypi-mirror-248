from typing import Dict, Optional, Union

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
        base_url: Optional[str] = "/api/v2.0",
        protocol: Optional[str] = "http",
        port: Optional[Union[int, str]] = 8083,
        verify: Optional[bool] = True,
        session = None,
        token: Optional[str] = None
    ) -> None:
        super().__init__(host, username, password, base_url, protocol, port, verify, session, token)

    def delete(self, schema_type: str, schema_name: str) -> Dict:
        """
        Remove a user schema.

        :param schema_type: Type of schema.
        :param schema_name: Name of schema.
        """
        return self._make_request(
            f"/user-schema/{schema_type}/{schema_name}", method="delete"
        )

    def update(self, schema_type: str, schema_name: str, config_object: Dict) -> Dict:
        """
        Update/Insert a user schema document.

        :param schema_type: Type of schema.
        :param schema_name: Name of schema.
        :param config_object: Schema to apply to entity in identified in path.
        """
        return self._make_request(
            f"/user-schema/{schema_type}/{schema_name}",
            method="put",
            jsonbody=config_object,
        )
