# Changelog

## [v1.3.6](https://github.com/user-sspmynxdvb/ua_alarm/tree/dafa5ab83878e4bc451d044c8c5385a756d85aaa) - 27.12.2023

### Improved
- **files: client.py**
- **functions: alert_loop**

### Added
- **libraries: from datetime import datetime**
- **functions: refactor_alert_type**

### More info
- **alert_loop: `utc = datetime.now().tzinfo
changed_str.astimezone(utc)`**


## [v1.3.5](https://github.com/user-sspmynxdvb/ua_alarm/tree/e2f9b29f3e26815305c0af7b782775f06bb1f52a) - 27.12.2023

### Improved
- **files: poetry.lock, client.py**
- **functions: _make_request**

### Added
- **libraries: from asyncio import sleep as async_sleep, from aiohttp.client_exceptions import ClientConnectorError**
- **functions: alert_loop**

### More info
- **_make_request: `match response.status:
                    case 200:
                        pass
                    case 401:
                        raise PermissionError("Invalid API token")
                    case 503:
                        raise Exception("API is currently unavailable")
                    case unknown_status:
                        raise Exception(f"Request failed with status code {unknown_status}\n{await response.text()}")`**


## [v1.3.4](https://github.com/user-sspmynxdvb/ua_alarm/tree/9c31e9a778af3e239ca153a40c42eeec91435bc1) - 04.12.2023

### Improved
- **functions: __init__, _make_request**
- **files: client.py**

### Added
- **libraries: from asyncio import run**

### More info
- **__init__: added run(self._make_request("GET", self._ALERTS_ENDPOINT))**
- **_make_request: `if response.status != 200: raise Exception("Invalid API token")`**


## [v1.3.3](https://github.com/user-sspmynxdvb/ua_alarm/tree/bb6e4f60d6362467e61cb3dd6b24b7d3beed668c) - 29.11.2023

### Improved
- **code: Code format**

### Added
- **variables: Links have been moved to constants**

### Removed
- **functions: get_region_alerts**

### More info
- **removed function get_region_alerts, functionality has been moved to get_alerts**
