from asyncio import sleep, run
from datetime import datetime
from typing import List, Optional, Union

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

from ua_alarm import types
from ua_alarm.enums.alert_type import AlertType


# from icecream import ic
class Client:
    """
    A client to interact with the UkraineAlert API, providing methods to access various endpoints.

    Attributes:
        base_url (str): The base URL for UkraineAlert API.
        headers (dict): The headers required for authorization in API requests.

    Methods:
        __init__(api_token: str): Initialize the UkraineAlertApiClient with an API token.
        _make_request(method: str, endpoint: str, params: Optional[dict] = None, data: Optional[dict] = None) -> Union[types.AlertRegionModel, types.AlertModification, types.RegionAlarmsHistory, types.RegionsViewModel, types.WebHook]: Make a request to the UkraineAlert API.
        get_alerts() -> List[types.AlertRegionModel]: Get a list of alerts.
        get_region_alerts(region_id: str|int) -> List[types.AlertRegionModel]: Get alerts for a specific region.
        get_alert_status() -> types.AlertModification: Get the status of alerts.
        get_region_history(region_id: str|int) -> types.RegionAlarmsHistory: Get the history of alerts for a specific region.
        get_regions() -> types.RegionsViewModel: Get information about regions.
        subscribe_to_webhook(webhook_data: dict) -> types.WebHook: Subscribe to a webhook.
        update_webhook(webhook_data: dict) -> None: Update an existing webhook.
        unsubscribe_from_webhook(webhook_data: dict) -> None: Unsubscribe from a webhook.
    """

    _ALERTS_ENDPOINT = "/api/v3/alerts"
    _ALERT_STATUS_ENDPOINT = "/api/v3/alerts/status"
    _REGION_HISTORY_ENDPOINT = "/api/v3/alerts/regionHistory"
    _REGIONS_ENDPOINT = "/api/v3/regions"
    _WEBHOOK_ENDPOINT = "/api/v3/webhook"

    def __init__(self, api_token: str):
        """
        Initializes the UkraineAlertApiClient with the provided API token.

        Args:
            api_token (str): The API token required for authorization.
        """
        self.base_url = "https://api.ukrainealarm.com"
        self.headers = {"Authorization": api_token}
        # test request
        run(self._make_request("GET", self._ALERTS_ENDPOINT))

    async def _make_request(
            self,
            method: str,
            endpoint: str,
            params: Optional[dict] = None,
            data: Optional[dict] = None,
    ) -> Union[
        types.AlertRegionModel,
        types.AlertModification,
        types.RegionAlarmsHistory,
        types.RegionsViewModel,
        types.WebHook,
    ]:
        """
        Makes a request to the UkraineAlert API.

        Args:
            method (str): The HTTP method for the request (e.g., GET, POST, PATCH, DELETE).
            endpoint (str): The specific API endpoint to access.
            params (Optional[dict]): Optional parameters for the request.
            data (Optional[dict]): Optional data payload for the request.

        Returns:
            Union[types.AlertRegionModel, types.AlertModification, types.RegionAlarmsHistory, types.RegionsViewModel, types.WebHook]: The response from the API based on the endpoint accessed.
        """
        url = f"{self.base_url}{endpoint}"
        async with ClientSession(headers=self.headers) as session:
            async with session.request(
                    method, url, params=params, json=data
            ) as response:
                match response.status:
                    case 200:
                        pass
                    case 401:
                        raise PermissionError("Invalid API token")
                    case 503:
                        raise Exception("API is currently unavailable")
                    case unknown_status:
                        raise Exception(f"Request failed with status code {unknown_status}\n{await response.text()}")

                response_json = await response.json()

                # Determine and return the appropriate model object based on the endpoint accessed
                if endpoint == self._ALERT_STATUS_ENDPOINT:
                    return types.AlertModification(**response_json)
                elif endpoint == self._REGION_HISTORY_ENDPOINT:
                    return [types.RegionAlarmsHistory(**item) for item in response_json]
                elif endpoint == self._REGIONS_ENDPOINT:
                    return types.RegionsViewModel(**response_json)
                elif endpoint == self._WEBHOOK_ENDPOINT:
                    return types.WebHook(**response_json)
                elif self._ALERTS_ENDPOINT in endpoint:
                    return [types.AlertRegionModel(**item) for item in response_json]

    async def get_alerts(self, region_id: str | int = None) -> List[types.AlertRegionModel]:
        """
        Retrieves alerts from the UkraineAlert API.

        Args:
            region_id (str or int, optional): The ID of the region for which alerts are requested. Defaults to None.

        Returns:
            List[types.AlertRegionModel]: A list of types.AlertRegionModel objects.
        """
        endpoint = self._ALERTS_ENDPOINT if not region_id else f"{self._ALERTS_ENDPOINT}/{region_id}"
        return await self._make_request("GET", endpoint)

    async def get_alert_status(self) -> types.AlertModification:
        """
        Retrieves the status of alerts from the UkraineAlert API.

        Returns:
            types.AlertModification: An object representing the status of alerts.
        """
        return await self._make_request("GET", self._ALERT_STATUS_ENDPOINT)

    async def get_region_history(
            self, region_id: str | int
    ) -> types.RegionAlarmsHistory:
        """
        Retrieves the history of alerts for a specific region from the UkraineAlert API.

        Args:
            region_id (str or int): The ID of the region for which the history of alerts is requested.

        Returns:
            types.RegionAlarmsHistory: An object representing the history of alerts for the specified region.
        """
        params = {"regionId": region_id}
        return await self._make_request(
            "GET", self._REGION_HISTORY_ENDPOINT, params=params
        )

    async def get_regions(self) -> types.RegionsViewModel:
        """
        Retrieves information about regions from the UkraineAlert API.

        Returns:
            types.RegionsViewModel: An object representing information about regions.
        """
        return await self._make_request("GET", self._REGIONS_ENDPOINT)

    async def subscribe_to_webhook(self, webhook_data: dict) -> types.WebHook:
        """
        Subscribes to a webhook in the UkraineAlert API.

        Args:
            webhook_data (dict): Data required for subscribing to the webhook.

        Returns:
            types.WebHook: An object representing the subscribed webhook.
        """
        return await self._make_request(
            "POST", self._WEBHOOK_ENDPOINT, data=webhook_data
        )

    async def update_webhook(self, webhook_data: dict) -> None:
        """
        Updates an existing webhook in the UkraineAlert API.

        Args:
            webhook_data (dict): Data required for updating the webhook.
        """
        await self._make_request("PATCH", self._WEBHOOK_ENDPOINT, data=webhook_data)

    async def unsubscribe_from_webhook(self, webhook_data: dict) -> None:
        """
        Unsubscribes from a webhook in the UkraineAlert API.

        Args:
            webhook_data (dict): Data required for unsubscribing from the webhook.
        """
        await self._make_request("DELETE", self._WEBHOOK_ENDPOINT, data=webhook_data)

    @staticmethod
    def refactor_alert_type(type: AlertType) -> str:
        """
        Converts an AlertType enum into a corresponding localized string representation.

        Args:
            type (AlertType): The AlertType enum value.

        Returns:
            str: A string representing the localized alert message corresponding to the AlertType.
                 Defaults to 'Повітряна тривога' if the AlertType is not found in the mapping.
        """
        ALERT_TYPE = {
            AlertType.ARTILLERY: "Загроза артобстрілу",
            AlertType.URBAN_FIGHTS: "Загроза вуличних боїв",
            AlertType.CHEMICAL: "Хімічна загроза",
            AlertType.NUCLEAR: "Радіаційна загроза ",
        }
        return ALERT_TYPE.get(type, "Повітряна тривога")

    async def alert_loop(self, region_id: str | int) -> None:
        """
        A loop that continuously monitors for changes in the alert state for a specific region.

        The loop fetches region alerts using the UkraineAlert API and checks for changes in the last update time.
        If a change is detected, it prints information about the active alert, if any.

        Note: The loop sleeps for 30 seconds between iterations.

        Raises:
            ClientConnectorError: If there's a connection issue during API request.

        Global Variables:
            alert_changed_time (str): A global variable to store the timestamp of the last alert change.

        API Token:
            The API token is hardcoded for demonstration purposes.

        API Client:
            An instance of UkraineAlertApiClient is used to interact with the UkraineAlert API.
        """
        # Initialize the alert_changed_time variable
        alert_changed_time = ""
        utc = datetime.now().tzinfo

        # Continuously monitor for changes in the alert state
        while True:
            try:
                # Fetch region alerts (region_id=28)
                data = await self.get_alerts(region_id)
                data = data[0]

                # Extract the last update time from the fetched data
                changed_str = data.lastUpdate

                # Check if there's a change in the alert state
                if not changed_str == alert_changed_time:
                    alert_old_changed_time = alert_changed_time
                    alert_changed_time = changed_str
                    changed_str = f"({changed_str.astimezone(utc).strftime('%d.%m.%Y %H:%M:%S')})"

                    # Skip if duration less than or equal to 10 seconds
                    if alert_old_changed_time:
                        if int((alert_changed_time - alert_old_changed_time).total_seconds()) <= 10:
                            continue

                        # Construct a text message based on the active alert status
                        if data.activeAlerts:
                            alert_type = self.refactor_alert_type(data.activeAlerts[0].type)
                            text = f"{changed_str} \033[38;5;202m[{alert_type}] \033[31m\033[1mОголошено тривогу"
                        else:
                            text = f"{changed_str} \033[32m\033[1mВідбій тривоги"

                        # Print the alert information
                        print(f"\033[34m\033[1m{text}\033[37m\033[1m")

            # Continue to the next iteration if there's a connection issue
            except ClientConnectorError:
                pass

            # Sleep for 30 seconds before checking for changes again
            await sleep(30)
