from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class PasswordReset(ClientBase):
    """
    Class that contains methods for the IAG password_reset API routes.
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

    def reset(
        self,
        username: str,
        email: str,
        new_password: str,
        old_password: str,
        security_ques1: str,
        security_ques1_ans: str,
        security_ques2: str,
        security_ques2_ans: str,
    ) -> Dict:
        """
        Reset password for user on the AG server.

        :param username: Username of account.
        :param email: Email address of account.
        :param new_password: The new password.
        :param old_password: The old/temp password.
        :param security_ques1: Security question #1.
        :param security_ques1_ans: Answer to security question #1.
        :param security_ques2: Security question #2.
        :param security_ques2_ans: Answer to security question #2.
        """
        parameters = {
            "email": email,
            "new_password": new_password,
            "old_password": old_password,
            "security_ques1": security_ques1,
            "security_ques1_ans": security_ques1_ans,
            "security_ques2": security_ques2,
            "security_ques2_ans": security_ques2_ans,
            "username": username,
        }
        return self._make_request("/password_reset", method="post", jsonbody=parameters)

    def update(
        self,
        username: str,
        email: str,
        new_password: str,
        security_ques1: str = None,
        security_ques1_ans: str = None,
        security_ques2: str = None,
        security_ques2_ans: str = None,
    ) -> Dict:
        """
        Update password for user on the AG server.

        :param username: Username of account.
        :param email: Email address of account.
        :param new_password: The new password.
        :param security_ques1: Optional. Security question #1.
        :param security_ques1_ans: Optional. Answer to security question #1.
        :param security_ques2: Optional. Security question #2.
        :param security_ques2_ans: Optional. Answer to security question #2.
        """
        parameters = {
            "email": email,
            "new_password": new_password,
            "security_ques1": security_ques1,
            "security_ques1_ans": security_ques1_ans,
            "security_ques2": security_ques2,
            "security_ques2_ans": security_ques2_ans,
            "username": username,
        }
        return self._make_request(
            "/password_reset/update", method="post", jsonbody=parameters
        )

    def update_change_flag(self, username: str) -> Dict:
        """
        Update the password change flag to false on the AG server.

        :param username: Username of account.
        """
        return self._make_request(
            f"/password_reset/update_flag/{username}", method="post"
        )

    def update_security_questions(
        self,
        username: str,
        security_ques1: str,
        security_ques1_ans: str,
        security_ques2: str,
        security_ques2_ans: str,
    ) -> Dict:
        """
        Update security questions and answers for user on the AG server.

        :param username: Username of account.
        :param security_ques1: Optional. Security question #1.
        :param security_ques1_ans: Optional. Answer to security question #1.
        :param security_ques2: Optional. Security question #2.
        :param security_ques2_ans: Optional. Answer to security question #2.
        """
        parameters = {
            "security_ques1": security_ques1,
            "security_ques1_ans": security_ques1_ans,
            "security_ques2": security_ques2,
            "security_ques2_ans": security_ques2_ans,
            "username": username,
        }
        return self._make_request(
            "/password_reset/update_questions", method="post", jsonbody=parameters
        )

    def validate_password_change(self, username: str) -> Dict:
        """
        Validate if password is changed in the IAG server

        :param username: Username of account.
        """
        return self._make_request(
            f"/password_reset/validate_pass_change/{username}", method="post"
        )
