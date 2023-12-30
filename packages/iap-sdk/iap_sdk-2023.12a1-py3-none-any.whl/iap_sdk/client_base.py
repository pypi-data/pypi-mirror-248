import logging
from typing import Any, Dict, Optional, Union

import json
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
        protocol: Optional[str] = "https",
        port: Optional[Union[int, str]] = 3443,
        verify: Optional[bool] = True,
        session: Optional[requests.session] = None,
        token: Optional[str] = None,
    ) -> None:
        """
        Constructor to build a new object. Automatically collects an
        authorization token and assembles the headers used for all
        future requests.

        :param host: Itential IAP FQDN or IP address.
        :param username: Username for IAP login.
        :param password: Password for IAP login.
        :param protocol: Option. Choose between "http" (default) and "https".
        :param port: Optonal. Select server port (default 8083).
        :param verify: Optional. Verify/ignore SSL certificates (default True)
        :param session: requests.session object (provided by IAP() class).
        :param token: Session token (provided by IAP() class).
        """
        self.host: str = host
        self.username: str = username
        self.password: str = password
        self.protocol: str = protocol
        self.port: str = str(port)
        self.verify: bool = verify
        self.session = session
        self.token = token
        self.auth_body: Dict[str, Dict[str, str]] = json.dumps(
            {"user": {"username": self.username, "password": self.password}}
        )

    def login(self) -> None:
        try:
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            auth_resp = self.session.post(
                f"{self.protocol}://{self.host}:{self.port}/login",
                headers=headers,
                data=self.auth_body,
                verify=self.verify,
            )
            auth_resp.raise_for_status()
            self.token = auth_resp.text
            self.headers["Cookie"] = f"token={self.token}"
            self.session.headers.update(headers)
        except requests.exceptions.RequestException as auth_error:
            logging.log(
                logging.ERROR,
                msg=f"Unable to authenticate with {self.host} using {self.username}.",
            )
            logging.log(logging.ERROR, msg=str(auth_error))

    def logout(self) -> None:
        self.session.close()

    def _make_request(
        self,
        endpoint: str,
        method: str = "get",
        data: Optional[Dict[str, Any]] = None,
        jsonbody: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[requests.Response]:
        """
        Issues a generic single request. Basically, a wrapper for "requests"
        using the already-stored host, headers, and verify parameters.

        :param endpoint: Itential IAP API endpoint. E.g. /devices.
        :param method: Optional. API method: get (default),post,put,patch,delete.
        :param data: Optional. A dictionary to send as the body.
        :param jsonbody: Optional. A JSON object to send as the body.
        :param params: Optional. A dictionary to send as URL parameters.
        """
        if not self.token:
            self.login()
        # check for and add missing leading forward slash in API endpoint
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(
                    url=f"{self.protocol}://{self.host}:{self.port}{endpoint}",
                    data=data,
                    json=jsonbody,
                    params=params,
                    verify=self.verify,
                )
            elif method.upper() == "POST":
                response = self.session.post(
                    url=f"{self.protocol}://{self.host}:{self.port}{endpoint}",
                    data=data,
                    json=jsonbody,
                    params=params,
                    verify=self.verify,
                )
            elif method.upper() == "PUT":
                response = self.session.put(
                    url=f"{self.protocol}://{self.host}:{self.port}{endpoint}",
                    data=data,
                    json=jsonbody,
                    params=params,
                    verify=self.verify,
                )
            elif method.upper() == "PATCH":
                response = self.session.patch(
                    url=f"{self.protocol}://{self.host}:{self.port}{endpoint}",
                    data=data,
                    json=jsonbody,
                    params=params,
                    verify=self.verify,
                )
            elif method.upper() == "DELETE":
                response = self.session.delete(
                    url=f"{self.protocol}://{self.host}:{self.port}{endpoint}",
                    data=data,
                    json=jsonbody,
                    params=params,
                    verify=self.verify,
                )

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            logging.log(
                logging.ERROR,
                msg=f"Failed to retrieve response from {self.protocol}://{self.host}:{self.port}{endpoint}.",
            )
            logging.log(logging.ERROR, msg=str(error))
            return None
