"""Abstraction layer on top of AWS Cloud Watch."""
import os

from aws_lambda_powertools import Logger
from boto3 import client
from botocore.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_cloudwatch import CloudWatchClient

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class CloudWatchService:
    """Main class to handle AWS Cloudwatch communication."""

    def __init__(self):
        """Initializes the CloudWatchService class.

        Create a boto3 CloudWatch client with the following configuration:
            - region_name: eu-west-1
            - config:
                - retries:
                    - max_attempts: 10
                    - mode: adaptive

        Assigns the client to the __cloudwatch_service attribute.
        """

        config = Config(retries={"max_attempts": 10, "mode": "adaptive"})
        self.__cloudwatch_service = self.create_client(region_name="eu-west-1", config=config)

    @staticmethod
    def create_client(region_name: str, config: Config) -> CloudWatchClient:
        """Creates a boto3 CloudWatch client.

        parameters:
            region_name (str): The AWS region name for the client.
            config (Config): The botocore configuration for the client.

        returns:
            CloudwatchClient: The boto3 CloudWatch client.
        """

        return client("cloudwatch", region_name=region_name, config=config)

    def put_metric(self, metric: list, name_space: str):
        """Puts metric data into CloudWatch.

        parameters:
            metric (list): The metric data to put.
            name_space (str): The namespace to put the metric in.

        try to call put_metric_data on the boto3 client to put the metric data into
        the given namespace.

        raises any ClientErrors that occur.

        logs errors if failed to put metric or namespace.
        """

        try:
            self.__cloudwatch_service.put_metric_data(MetricData=metric, Namespace=name_space)
        except ClientError as error:
            LOGGER.error(f"Failed to put metric data: {metric}")
            LOGGER.error(f"Failed to put metric in to namespace: {name_space}")
            raise error
