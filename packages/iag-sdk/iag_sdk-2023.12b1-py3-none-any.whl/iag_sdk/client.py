import logging
from typing import Dict, Union

import requests

from iag_sdk.modules.accounts import Account
from iag_sdk.modules.collections import Collection
from iag_sdk.modules.config import Config
from iag_sdk.modules.devices import Device
from iag_sdk.modules.groups import Group
from iag_sdk.modules.http_requests import HttpRequest
from iag_sdk.modules.inventory import Inventory
from iag_sdk.modules.ldap import Ldap
from iag_sdk.modules.modules import Module
from iag_sdk.modules.netconf import Netconf
from iag_sdk.modules.netmiko import Netmiko
from iag_sdk.modules.nornir import Nornir
from iag_sdk.modules.password_reset import PasswordReset
from iag_sdk.modules.playbooks import Playbook
from iag_sdk.modules.pronghorn import Pronghorn
from iag_sdk.modules.rbac import Rbac
from iag_sdk.modules.roles import Role
from iag_sdk.modules.scripts import Script
from iag_sdk.modules.secrets import Secret
from iag_sdk.modules.security_questions import SecurityQuestion
from iag_sdk.modules.system import System
from iag_sdk.modules.terraforms import Terraform
from iag_sdk.modules.user_schema import UserSchema

logging.basicConfig(level=logging.INFO)


class Iag:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
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
        :param base_url: Optional. The initial part of the IAG API URL (default "/api/v2.0").
        :param protocol: Option. Choose between "http" (default) and "https".
        :param port: Optonal. Select server port (default 8083).
        :param verify: Optional. Verify/ignore SSL certificates (default True)
        """
        self.host: str = host
        self.username: str = username
        self.password: str = password
        self.base_url: str = base_url
        self.protocol: str = protocol
        self.port: str = str(port)
        self.verify: bool = verify

        # If verify is false, we should disable unnecessary SSL logging
        if not verify:
            requests.packages.urllib3.disable_warnings()

        # Build common headers
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        # ensure base_url starts with a forward slash
        if not self.base_url.startswith("/"):
            self.base_url = f"/{self.base_url}"

        # ensure host value does not contain protocol or port information
        if "://" in self.host:
            self.host = self.host.split(":")[1]
        if ":" in self.host:
            self.host = self.host.split(":")[0]

        try:
            auth_resp = requests.request(
                "POST",
                f"{self.protocol}://{self.host}:{self.port}{self.base_url}/login",
                headers=self.headers,
                json={"username": self.username, "password": self.password},
                verify=self.verify,
            )
            auth_resp.raise_for_status()
            self.headers["Authorization"] = f"{auth_resp.json()['token']}"
        except requests.RequestException as auth_error:
            logging.log(
                logging.ERROR,
                msg=f"Unable to authenticate with {self.host} using {username}.",
            )
            logging.log(logging.ERROR, msg=str(auth_error))

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

    @property
    def accounts(self) -> Account:
        return Account(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def collections(self) -> Collection:
        return Collection(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def config(self) -> Config:
        return Config(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def devices(self) -> Device:
        return Device(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def groups(self) -> Group:
        return Group(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def http_requests(self) -> HttpRequest:
        return HttpRequest(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def inventory(self) -> Inventory:
        return Inventory(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def ldap(self) -> Ldap:
        return Ldap(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def modules(self) -> Module:
        return Module(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def netconf(self) -> Netconf:
        return Netconf(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def netmiko(self) -> Netmiko:
        return Netmiko(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def nornir(self) -> Nornir:
        return Nornir(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def password_reset(self) -> PasswordReset:
        return PasswordReset(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def playbooks(self) -> Playbook:
        return Playbook(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def pronghorn(self) -> Pronghorn:
        return Pronghorn(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def rbac(self) -> Rbac:
        return Rbac(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def roles(self) -> Role:
        return Role(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def scripts(self) -> Script:
        return Script(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def secrets(self) -> Secret:
        return Secret(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def security_questions(self) -> SecurityQuestion:
        return SecurityQuestion(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def system(self) -> System:
        return System(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def terraforms(self) -> Terraform:
        return Terraform(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )

    @property
    def user_schema(self) -> UserSchema:
        return UserSchema(
            self.host,
            self.username,
            self.password,
            self.headers,
            self.base_url,
            self.protocol,
            self.port,
            self.verify,
        )
