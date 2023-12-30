from typing import Dict, Optional, Union

from iag_sdk.client_base import ClientBase


class SecurityQuestion(ClientBase):
    """
    Class that contains methods for the IAG security_questions API routes.
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

    def get_security_questions(self) -> Dict:
        """
        Get security questions for the IAG server.
        """
        return self._make_request("/security_questions")

    def get_security_questions_user(self, email: str) -> Dict:
        """
        Get security questions for email id on the IAG server.

        :param email: Email ID of user account.
        """
        return self._make_request(f"/security_questions/{email}")

    def validate_security_answers_user(
        self,
        email: str,
        security_ques1: str,
        security_ques1_ans: str,
        security_ques2: str,
        security_ques2_ans: str,
    ) -> Dict:
        """
        Validate security answers for email id on the IAG server.

        :param email: Email ID of user account.
        :param security_ques1: Security question #1.
        :param security_ques1_ans: Answer to security question #1.
        :param security_ques2: Security question #2.
        :param security_ques2_ans: Answer to security question #2.
        """
        parameters = {
            "email": email,
            "security_ques1": security_ques1,
            "security_ques1_ans": security_ques1_ans,
            "security_ques2": security_ques2,
            "security_ques2_ans": security_ques2_ans,
        }
        return self._make_request(
            "security_questions/validate_answers", method="post", jsonbody=parameters
        )
