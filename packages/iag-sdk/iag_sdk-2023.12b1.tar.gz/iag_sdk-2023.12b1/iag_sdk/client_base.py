import logging
from typing import Dict, Union

import requests

logging.basicConfig(level=logging.INFO)


class ClientBase:
    """
    Base class the module classes inherit from. Provides generic query method. 
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
        """
        Constructor to build a new object. Automatically collects an
        authorization token and assembles the headers used for all
        future requests.

        :param host: Itential IAG FQDN or IP address.
        :param username: Username for IAG login.
        :param password: Password for IAG login.
        :param headers: Headers dictionary incl. the token (provided by client()).
        :param base_url: Optional. The initial part of the IAG API URL (default "/api/v2.0").
        :param protocol: Option. Choose between "http" (default) and "https".
        :param port: Optonal. Select server port (default 8083).
        :param verify: Optional. Verify/ignore SSL certificates (default True)
        """
        self.host: str = host
        self.username: str = username
        self.password: str = password
        self.headers: Dict = headers
        self.base_url: str = base_url
        self.protocol: str = protocol
        self.port: str = str(port)
        self.verify: bool = verify

    def query(
        self,
        endpoint: str,
        method: str = "get",
        data: Dict = None,
        jsonbody: Dict = None,
        params: Dict = None,
    ) -> requests.Response:
        """
        Issues a generic single request. Basically, a wrapper for "requests"
        using the already-stored host, headers, and verify parameters.

        :param endpoint: Itential IAG API endpoint. E.g. /devices.
        :param method: Optional. API method: get (default),post,put,patch,delete.
        :param data: Optional. A dictionary to send as the body.
        :param jsonbody: Optional. A JSON object to send as the body.
        :param params: Optional. A dictionary to send as URL parameters.
        """
        # check for and add missing leading forward slash in API endpoint
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=f"{self.protocol}://{self.host}:{self.port}{self.base_url}{endpoint}",
                headers=self.headers,
                data=data,
                json=jsonbody,
                params=params,
                verify=self.verify,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            logging.log(
                logging.ERROR,
                msg=f"Failed to retrieve response from {self.protocol}://{self.host}:{self.port}{self.base_url}{endpoint}.",
            )
            logging.log(logging.ERROR, msg=str(error))
        return response.json()
