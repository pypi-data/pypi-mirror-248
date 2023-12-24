"""Abstraction layer on top of AWS Event Bridge."""
import os

from aws_lambda_powertools import Logger
from boto3 import client
from botocore.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_events.client import EventBridgeClient

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class EventsService:
    """Main class to handle AWS EventBridge communication."""

    def __init__(self, event_bus_name, region_name: str):
        """Initializes an EventsService instance.

        Parameters:
        - event_bus_name (str): The name of the event bus to use.
        - region_name (str): The AWS region name.

        Create an EventBridge client with retry configuration.

        Set the event bus name.
        """

        config = Config(retries={"max_attempts": 10, "mode": "adaptive"})
        self.__client = self.create_client(region_name=region_name, config=config)
        self.event_bus_name = event_bus_name

    @staticmethod
    def create_client(region_name: str, config: Config) -> EventBridgeClient:
        """Creates an EventBridge client.

        Parameters:
        - region_name (str): The AWS region for the client.
        - config (botocore.config.Config): The botocore configuration for the client.

        Returns:
        - EventBridgeClient: The EventBridge client instance.

        Use the boto3 client() function to create a new EventBridgeClient
        configured for the given region and with the provided botocore configuration.
        """

        return client("events", region_name=region_name, config=config)

    def put_event(self, item: dict):
        """Puts an event into EventBridge.

        Parameters:
        - item (dict): The event to put.

        Add the configured event bus name to the event.

        Calls PutEvents API to put the event.

        Raises:
        - ClientError: If the API call fails.

        Put a single event into the configured event bus.
        """

        try:
            item["EventBusName"] = self.event_bus_name

            self.__client.put_events(Entries=[item])
        except ClientError as error:
            LOGGER.error(f"Failed to put event: {repr(error)} into EventBridge: {self.event_bus_name}")
            raise
