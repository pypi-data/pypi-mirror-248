# itential-iag-sdk
Lightweight SDK to simplify the process of interacting with the Itential automation gateway API.

This is an beta release. Please ensure the package works as expected in your environment before using it in production as there may still be bugs.

This package was written for Itential Automation Gateway 2023.1. 

## Getting Started
Make sure you have a supported version of Python installed and then create and activate a virtual environment:
```bash
python -m venv venv

source /venv/bin/activate
```
You can install the iag_sdk from Pypi as follows:
```bash
pip install iag-sdk
```
Or you can install it from source as follows:
```bash
git clone https://github.com/awetomate/itential-iag-sdk.git
cd itential-iag-sdk
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Usage
```python
from iag_sdk import Iag

username = "admin@itential"
password = "your_password"
host = "your_server"

iag = Iag(host=host, username=username, password=password, verify=False)

iag.accounts.get(name="admin@itential")
#{'email': 'admin@itential.com', 'firstname': None, 'lastname': None, 'username': 'admin@itential'}
```
iag_sdk uses the following default values. You can overwrite any of them during instantiation:
```python
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
```

The iag_sdk methods are grouped in the same manner as in Itential's API documentation. 
I.e. all API calls related to collections are available under iag.collections. and all API calls related to (Ansible) devices are available under iag.devices.

### Examples
```python
# get the server status
iag.system.get_status()

# list the first 10 Ansible devices that have 'SW' in their hostname
iag.devices.get_all(limit=10, filter='contains({"name": "SW"})')

# get a specific Ansible device
iag.devices.get(name="device1")

# check the state for a specific Ansible device
iag.devices.get_state(name="device1")
```

Work with Ansible collections:
```python
# get one collection
iag.collections.get(collection_name="cisco.asa")

# get modules for a specific collection
iag.collections.get_modules(collection_name="cisco.asa")

# list all collections
iag.collections.get_all()

# refresh collections / perform a collection discovery
iag.collections.refresh()
```
Work with Netmiko:
```python
# IAG native
iag.netmiko.execute_send_command_native(
    host="device1", 
    command_string="show version"
)

# legacy
iag.netmiko.execute_send_command_legacy(
    host="device1", 
    commands=["show version"], 
    device_type="cisco_ftd", 
    username="your_username", 
    password="your_password", 
    port=22
)
```

### The all-purpose 'query' method
The iag_sdk includes a generic 'query' method that can be used for every Itential automation gateway API call. In fact, all the other methods ultimately use the generic 'query' method to send calls to AG.

The query method by default sends GET requests without any data or parameters. 
However, you can use the 'query' method to send get, delete, post, put, and patch requests by changing the 'method' argument. You can also send data by various means (params, data, jsonbody).

The generic 'query' method potentially could come in handy to overcome differences in the API between automation gateway versions. If any of the existing methods don't work with your AG version, try the generic 'query' method as a fallback.

The 'query' method takes the following arguments:
| argument | description |
| --- | --- |
| endpoint | Itential IAG API endpoint. E.g. /devices.|
| method | Optional. API method: get (default),post,put,patch,delete.|
| data | Optional. A dictionary to send as the body.|
| jsonbody | Optional. A JSON object to send as the body.|
| params | Optional. A dictionary to send as URL parameters.|

#### Basic GET call using 'query'
```python
# get the server status
iag.query("/status")
# or to be more explicit
iag.query("/status", method="get")

# get a specific collection
collection_name = "cisco.asa"
iag.query(f"collections/{collection_name}")
# or define the endpoint statically
iag.query("collections/cisco.asa")

# list the first 10 Ansible devices that have 'SW' in their hostname
iag.query("/devices", params={"limit": 10, "filter": 'contains({"name":"SW"})'})
```

#### Basic POST call using 'query'
```python
iag.query("/collections/refresh", method="post")

iag.query("/netmiko/send_command/execute", method="post", jsonbody={"host": "networkdevice", "command_string": "show version"})
```

