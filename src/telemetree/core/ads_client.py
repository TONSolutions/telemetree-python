import logging
from uuid import UUID
from typing import Union

from telemetree.schemas.telemetree_schemas import Config
from telemetree.schemas.ads_network_schemas import (
    AdsClientOptions,
    StatsChangeSuccessResponse,
    FetchedTask,
)
from telemetree.http.http_client import HttpClient
from telemetree.schemas.ads_network_schemas import FetchedTaskResponse
from telemetree.schemas.constants import (
    ENDPOINT_URL,
    FETCH_TASKS_ENDPOINT,
    DISPLAY_TASKS_ENDPOINT,
    VERIFY_TASKS_ENDPOINT,
)

logger = logging.getLogger("telemetree.ads_client")


class TelemetreeAds:
    def __init__(
        self,
        ads_user_id: str,
        # config: BotTrackingConfig,
        options: AdsClientOptions = AdsClientOptions(),
    ):
        self.ads_user_id = ads_user_id
        self.__check_uuid_format(ads_user_id)

        # self.config = config
        self.options = options

    def __check_uuid_format(self, ads_user_id: str) -> bool:
        try:
            UUID(ads_user_id)
            return True
        except ValueError:
            raise ValueError("Invalid UUID format")

    def __update_task_performance(self, user_id: int, task: FetchedTask, url: str):
        http_client = HttpClient(self.ads_user_id)

        query_params = {
            "user_id": user_id,
            "task_id": task.id,
            "debug_mode": self.options.debug_mode,
        }

        response = http_client.get(url, query_params)

        try:
            response.raise_for_status()
        except Exception as e:
            logger.error(
                f"Error code: {response.status_code}. Failed to display tasks: {e}"
            )
            return None

        try:
            return StatsChangeSuccessResponse(**response.json())
        except Exception as e:
            logger.error(
                f"Error code: {response.status_code}. Failed to parse tasks: {e}"
            )
            return None

    def fetch(self) -> FetchedTaskResponse:
        request_url = f"{ENDPOINT_URL}{FETCH_TASKS_ENDPOINT}"
        http_client = HttpClient(self.ads_user_id)

        request_params = self.options.model_dump(mode="json")
        response = http_client.get(request_url, query_params=request_params)

        try:
            response.raise_for_status()
        except Exception as e:
            logger.error(
                f"Error code: {response.status_code}. Failed to fetch tasks: {e}"
            )
            return None

        try:
            return FetchedTaskResponse(**response.json())
        except Exception as e:
            logger.error(
                f"Error code: {response.status_code}. Failed to parse tasks: {e}"
            )
            return None

    def display(self, user_id: int, task: FetchedTask):
        request_url = f"{ENDPOINT_URL}{DISPLAY_TASKS_ENDPOINT}"
        return self.__update_task_performance(user_id, task, request_url)

    def verify(self, user_id: int, task: FetchedTask):
        request_url = f"{ENDPOINT_URL}{VERIFY_TASKS_ENDPOINT}"
        return self.__update_task_performance(user_id, task, request_url)
