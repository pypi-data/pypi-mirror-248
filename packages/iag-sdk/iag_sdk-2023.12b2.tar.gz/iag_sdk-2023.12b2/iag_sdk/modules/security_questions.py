from typing import Dict, Union

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
        headers: Dict,
        base_url: str = "/api/v2.0",
        protocol: str = "http",
        port: Union[int, str] = 8083,
        verify: bool = True,
    ) -> None:
        super().__init__(host, username, password, headers, base_url, protocol, port, verify)

    def get_security_questions(self) -> Dict:
        """
        Get security questions for the IAG server.
        """
        return self.query("/security_questions")

    def get_security_questions_user(self, email: str) -> Dict:
        """
        Get security questions for email id on the IAG server.

        :param email: Email ID of user account.
        """
        return self.query(f"/security_questions/{email}")

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
        return self.query(
            "security_questions/validate_answers", method="post", jsonbody=parameters
        )
