# itential-iap-sdk
Lightweight SDK to simplify the process of interacting with the Itential Automation Platform API.

This is an alpha release. It is incomplete and will change.

This package was written for Itential Automation Platform 2023.1. 

## Getting Started
Make sure you have a supported version of Python installed and then create and activate a virtual environment:
```bash
python -m venv venv

source /venv/bin/activate
```
You can install the iap_sdk from Pypi as follows:
```bash
pip install iap-sdk
```
Or you can install it from source as follows:
```bash
git clone https://github.com/awetomate/itential-iap-sdk.git
cd itential-iap-sdk
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Usage
```python
from iap_sdk import Iap

username = "your_username"
password = "your_password"
host = "your_server"

iap = Iap(host=host, username=username, password=password, verify=False)

iap.core.get_application(name="Jst")
```
iap_sdk uses the following default values. You can overwrite any of them during instantiation:
```python
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
```

The iap_sdk methods are grouped in the same manner as in Itential's API documentation. 
I.e. all API calls related to AGManager are available under iap.ag_manager. and all API calls related to pronghorn-core are available under iap.core.

### Examples
```python
# get information about the AGManager application
iap.core.get_application(name="AGManager")

# get health information for the AGManager application
iap.core.get_application_health(name="AGManager")

# restart the AGManager application
iap.core.restart_application(name="AGManager")

# get first 10 jobs from OperationsManager that are in running, paused, or error state
iap.operations_manager.get_jobs(limit=10, status=["running", "paused", "error"])
```


### The all-purpose 'query' method
The iap_sdk includes a generic 'query' method that can be used for every Itential automation gateway API call. In fact, all the other methods ultimately use the generic 'query' method to send calls to IAP.

The query method by default sends GET requests without any data or parameters. 
However, you can use the 'query' method to send get, delete, post, put, and patch requests by changing the 'method' argument. You can also send data by various means (params, data, jsonbody).

The generic 'query' method potentially could come in handy to overcome differences in the API between Automation Platform versions. If any of the existing methods don't work with your IAP version, try the generic 'query' method as a fallback.

The 'query' method takes the following arguments:
| argument | description |
| --- | --- |
| endpoint | IAP API endpoint. E.g. /health/applications.|
| method | Optional. API method: get (default),post,put,patch,delete.|
| data | Optional. A dictionary to send as the body.|
| jsonbody | Optional. A JSON object to send as the body.|
| params | Optional. A dictionary to send as URL parameters.|

#### Basic GET call using 'query'
```python
# get health information for the AGManager application
iap.query("/health/applications/AGManager")
# or to be more explicit
iap.query("/health/applications/AGManager", method="get")

# get jobs from OperationsManager
iap.query(
    "/operations-manager/jobs",
    jsonbody={
        "queryParameters": {
            "limit": 10,
            "include": "name,status",
            "in": {"status": "running"},
        }
    }
)
```

#### Basic PUT call using 'query'
```python
# restart the AGManager application
iap.query("/applications/AGManager/restart", method="put")
```

