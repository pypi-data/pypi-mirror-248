from typing import Dict, Union

from iag_sdk.client_base import ClientBase


class Account(ClientBase):
    """
    Class that contains methods for the IAG Accounts API routes.
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

    def add(
        self, username: str, password: str, firstname: str, lastname: str, email: str
    ) -> Dict:
        """
        Add a new user account.

        :param username: Username for the account.
        :param password: Password for the account.
        :param firstname: First name of user.
        :param lastname: Last name of user.
        :param email: Email address of user.
        """
        account = {
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "password": password,
            "username": username,
        }
        return self.query("/accounts", method="post", jsonbody=account)

    def confirm_eula(self, name: str) -> Dict:
        """
        Confirm EULA for an account.

        :param name: Name of user account
        """
        return self.query(f"/accounts/{name}/confirm_eula", method="post")

    def delete(self, name: str) -> Dict:
        """
        Delete a user account.

        :param name: Name of user account
        """
        return self.query(f"/accounts/{name}", method="delete")

    def get(self, name: str) -> Dict:
        """
        Get information for a user account.

        :param name: Name of the user account.
        """
        return self.query(f"/accounts/{name}")

    def get_all(
        self,
        offset: int = 0,
        limit: int = 50,
        filter: str = None,
        order: str = "ascending",
    ) -> Dict:
        """
        Get a list of user accounts.

        :param offset: Optional. The number of items to skip before starting to collect the result set.
        :param limit: Optional. Number of results to return (default 50).
        :param filter: Optional. Response filter function with JSON name/value pair argument, i.e., 'contains({"username":"admin"})' Valid filter functions - contains, equals, startswith, endswith
        :param order: Optional. Sort indication. Available values : 'ascending' (default), 'descending'.
        """
        return self.query(
            f"/accounts",
            params={"offset": offset, "limit": limit, "filter": filter, "order": order},
        )

    def update(self, name: str, config_object: Dict) -> Dict:
        """
        Update details of a user account.
        Tip: Use get_account() to get an idea of the format of the config_object.

        :param name: Name of user account
        :param config_object: Dictionary containing the variables to be updated.
        """
        return self.query(f"/accounts/{name}", method="put", jsonbody=config_object)

    def update_password(self, name: str, old_password: str, new_password: str) -> Dict:
        """
        Update user login credentials.

        :param name: Name of user account
        :param old_password: Old user password.
        :param new_password: New user password.
        """
        account = {"new_password": new_password, "old_password": old_password}
        return self.query(
            f"/accounts/{name}/update_password", method="post", jsonbody=account
        )
