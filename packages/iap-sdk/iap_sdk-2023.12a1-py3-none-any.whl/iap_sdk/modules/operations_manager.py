from typing import Dict, List, Optional, Union

from iap_sdk.client_base import ClientBase


class OperationsManager(ClientBase):
    """
    Class that contains methods for the IAP app-operations_manager API routes.
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

    def get_jobs(self, limit: int = 25, status: Optional[List[str]] = None) -> Dict:
        """
        Search the Job collection for running jobs.
        For custom filtering use the 'query' method instead.

        :param limit: Optional. Number of results to return (default 25).
        :param status: Optional. List of status to value to filter on (e.g. running, paused)
        """
        if status:
            status = ",".join(status)
        else:
            status = "running"
        return self._make_request(
            f"/operations-manager/jobs",
            jsonbody={
                "queryParameters": {
                    "limit": limit,
                    "include": "name,status",
                    "in": {"status": status},
                }
            },
        )

    def pause_jobs(self, job_ids: Optional[List[str]] = None) -> Dict:
        """
        Pause active Jobs.
        Requires a list of job IDs. Will pause all running jobs if nothing is provided.

        :param job_ids: Optional. List of job IDs to be paused.
        """
        if job_ids:
            return self._make_request(
                f"/operations-manager/jobs/pause",
                method="post",
                jsonbody={"jobIds": job_ids},
            )
        else:
            # get all running jobs
            jobs = self.get_jobs(limit=500)
            job_ids = [job["_id"] for job in jobs["data"]]
            return self._make_request(
                f"/operations-manager/jobs/pause",
                method="post",
                jsonbody={"jobIds": job_ids},
            )
        
    def resume_jobs(self, job_ids: Optional[List[str]] = None) -> Dict:
        """
        Resume paused Jobs.
        Requires a list of job IDs. Will resume all paused jobs if nothing is provided.

        :param job_ids: Optional. List of job IDs to be resumed.
        """
        if job_ids:
            return self._make_request(
                f"/operations-manager/jobs/resume",
                method="post",
                jsonbody={"jobIds": job_ids},
            )
        else:
            # get all paused jobs
            jobs = self.get_jobs(limit=500, status=["paused"])
            job_ids = [job["_id"] for job in jobs["data"]]
            return self._make_request(
                f"/operations-manager/jobs/pause",
                method="post",
                jsonbody={"jobIds": job_ids},
            )
