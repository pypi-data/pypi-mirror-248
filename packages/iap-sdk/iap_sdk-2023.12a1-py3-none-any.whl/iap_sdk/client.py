import logging
from typing import Any, Dict, Optional, Union

import json
import requests

from iap_sdk.client_base import ClientBase
from iap_sdk.modules.pronghorn_core import PronghornCore
from iap_sdk.modules.operations_manager import OperationsManager


logging.basicConfig(level=logging.INFO)


class Iap(ClientBase):
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        protocol: Optional[str] = "https",
        port: Optional[Union[int, str]] = 3443,
        verify: Optional[bool] = True,
    ) -> None:
        """
        Constructor to build a new object. Automatically collects an
        authorization token and assembles the headers used for all
        future requests.

        :param host: Itential IAP FQDN or IP address.
        :param username: Username for IAP login.
        :param password: Password for IAP login.
        :param protocol: Option. Choose between "https" (default) and "http".
        :param port: Optonal. Select server port (default 3443).
        :param verify: Optional. Verify/ignore SSL certificates (default True)
        """
        self.host: str = host
        self.username: str = username
        self.password: str = password
        self.protocol: str = protocol
        self.port: str = str(port)
        self.verify: bool = verify
        self.session = requests.Session()
        self.token = None
        self.auth_body: Dict[str, Dict[str, str]] = json.dumps(
            {"user": {"username": self.username, "password": self.password}}
        )
        # If verify is false, we should disable unnecessary SSL logging
        if not verify:
            requests.packages.urllib3.disable_warnings()
        # Build common headers
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        # ensure host value does not contain protocol or port information
        if "://" in self.host:
            self.host = self.host.split(":")[1]
        if ":" in self.host:
            self.host = self.host.split(":")[0]
        # get a token
        self.login()
        # update headers with authorization token
        self.session.headers.update(self.headers)
        super().__init__(
            self.host,
            self.username,
            self.password,
            self.protocol,
            self.port,
            self.verify,
            self.session,
            self.token,
        )

    def login(self) -> None:
        try:
            auth_resp = self.session.post(
                f"{self.protocol}://{self.host}:{self.port}/login",
                headers=self.headers,
                data=self.auth_body,
                verify=self.verify,
            )
            auth_resp.raise_for_status()
            self.token = auth_resp.text
            self.headers["Cookie"] = f"token={self.token}"
        except requests.exceptions.RequestException as auth_error:
            logging.log(
                logging.ERROR,
                msg=f"Unable to authenticate with {self.host} using {self.username}.",
            )
            logging.log(logging.ERROR, msg=str(auth_error))

    def logout(self) -> None:
        self.session.close()

    def query(
        self,
        endpoint: str,
        method: Optional[str] = "get",
        data: Optional[Dict[str, Any]] = None,
        jsonbody: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Issues a generic single request. Basically, a wrapper for "requests"
        using the already-stored host, headers, and verify parameters.

        :param endpoint: Itential IAP API endpoint. E.g. /devices.
        :param method: Optional. API method: get (default),post,put,patch,delete.
        :param data: Optional. A dictionary to send as the body.
        :param jsonbody: Optional. A JSON object to send as the body.
        :param params: Optional. A dictionary to send as URL parameters.
        """
        return self._make_request(
            endpoint=endpoint,
            method=method,
            data=data,
            jsonbody=jsonbody,
            params=params,
        )

    @property
    def core(self) -> PronghornCore:
        return PronghornCore(
            self.host,
            self.username,
            self.password,
            self.protocol,
            self.port,
            self.verify,
            self.session,
            self.token,
        )
    
    @property
    def operations_manager(self) -> OperationsManager:
        return OperationsManager(
            self.host,
            self.username,
            self.password,
            self.protocol,
            self.port,
            self.verify,
            self.session,
            self.token,
        )
