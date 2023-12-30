from typing import Dict, List, Optional, Union

from iap_sdk.client_base import ClientBase


class PronghornCore(ClientBase):
    """
    Class that contains methods for the IAP pronghorn-core API routes.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        protocol: Optional[str] = "https",
        port: Optional[Union[int, str]] = 3443,
        verify: Optional[bool] = True,
        session=None,
        token: Optional[str] = None,
    ) -> None:
        super().__init__(
            host, username, password, protocol, port, verify, session, token
        )

    def get_adapter(self, name: str) -> Dict:
        """
        Get a single adapter in IAP.

        :param name: Name of the adapter.
        """
        return self._make_request(f"/adapters/{name}")

    def get_adapters(self, limit: int = 50) -> Dict:
        """
        Get all adapters in IAP.
        For custom filtering sse the 'query' method instead.

        :param limit: Optional. Number of results to return (default 50).
        """
        return self._make_request(
            f"/adapters",
            jsonbody={"queryOptions": {"sort": "package_id", "limit": limit}},
        )

    def get_adapter_health(self, name: str) -> Dict:
        """
        Get the health of a single adapter in IAP.
        :param name: Name of the adapter.
        """
        return self._make_request(f"/health/adapters/{name}")

    def get_adapters_health(self, limit: int = 50) -> Dict:
        """
        Get the health of all the adapters in IAP.
        For custom filtering sse the 'query' method instead.

        :param limit: Optional. Number of results to return (default 50).
        """
        return self._make_request(
            f"/health/adapters",
            jsonbody={"queryOptions": {"sort": "package_id", "limit": limit}},
        )

    def get_application(self, name: str) -> Dict:
        """
        Get a single application in IAP.

        :param name: Name of the application.
        """
        return self._make_request(f"/applications/{name}")

    def get_applications(self, limit: int = 25) -> Dict:
        """
        Get all applications in IAP.
        For custom filtering use the 'query' method instead.

        :param limit: Optional. Number of results to return (default 25).
        """
        return self._make_request(
            f"/applications", jsonbody={"queryOptions": {"sort": "id", "limit": limit}}
        )

    def get_application_health(self, name: str) -> Dict:
        """
        Get the health of a single application in IAP.

        :param application: Name of the application.
        """
        return self._make_request(f"/health/applications/{name}")

    def get_applications_health(self, limit: int = 25) -> Dict:
        """
        Get the health of all the applications in IAP.
        For custom filtering use the 'query' method instead.

        :param limit: Optional. Number of results to return (default 25).
        """
        return self._make_request(
            f"/health/applications",
            jsonbody={"queryOptions": {"sort": "id", "limit": limit}},
        )

    def restart_adapter(self, name: str) -> Dict:
        """
        Restart an adapter in IAP.

        :param name: Name of the adapter.
        """
        return self._make_request(f"/adapters/{name}/restart", method="put")

    def restart_application(self, name: str) -> Dict:
        """
        Restart an application in IAP.

        :param name: Name of the application.
        """
        return self._make_request(f"/applications/{name}/restart", method="put")

    def start_adapter(self, name: str) -> Dict:
        """
        Start an adapter in IAP.

        :param name: Name of the adapter.
        """
        return self._make_request(f"/adapters/{name}/start", method="put")

    def start_application(self, name: str) -> Dict:
        """
        Start an application in IAP.

        :param name: Name of the application.
        """
        return self._make_request(f"/applications/{name}/start", method="put")

    def stop_adapter(self, name: str) -> Dict:
        """
        Stop an adapter in IAP.

        :param name: Name of the adapter.
        """
        return self._make_request(f"/adapters/{name}/stop", method="put")

    def stop_application(self, name: str) -> Dict:
        """
        Stop an application in IAP.

        :param name: Name of the application.
        """
        return self._make_request(f"/applications/{name}/stop", method="put")
