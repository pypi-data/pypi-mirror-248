"""Abstraction layer on top of AWS Event Bridge."""
import os

from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from aws_lambda_powertools import Logger
from boto3 import client, resource
from boto3.dynamodb.transform import TransformationInjector
from boto3.dynamodb.types import TypeDeserializer
from botocore.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class DynamoDBService:
    """Interact with DynamoDB using the AWS boto3 library."""

    def __init__(self, region_name="eu-west-1"):
        """Initializes a DynamoDBService instance.

        Parameters:
        - region_name (str): The AWS region to connect to.
            Default "eu-west-1".

        Create a botocore Config enabling retries.

        Call create_resource() and create_client() to instantiate
        a DynamoDB resource and client for the region.

        Creates a TransformationInjector that will be used to deserialize
        DynamoDB types when scanning.
        """

        config = Config(retries={"max_attempts": 10, "mode": "adaptive"})
        self.__resource = self.create_resource(region_name=region_name, config=config)
        self.__client = self.create_client(region_name=region_name, config=config)

        self.__transformation = TransformationInjector(deserializer=TypeDeserializer())

    @staticmethod
    def create_client(region_name: str, config: Config) -> DynamoDBClient:
        """Creates a DynamoDB client.

        Parameters:
        - region_name (str): The AWS region name for the client.
        - config (botocore.config.Config): The botocore configuration for
            the client.

        Returns:
        - DynamoDBClient: The DynamoDB client instance.

        Use the boto3 client() function to create a new DynamoDBClient
        instance configured for the given region and with the provided
        botocore configuration.
        """

        return client("dynamodb", region_name=region_name, config=config)

    @staticmethod
    def create_resource(region_name: str, config: Config) -> DynamoDBServiceResource:
        """Creates a DynamoDB resource.

        Parameters:
        - region_name (str): The AWS region name for the resource.
        - config (botocore.config.Config): The botocore configuration for
            the resource.

        Returns:
        - DynamoDBServiceResource: The DynamoDB resource instance.

        Use the boto3 resource() function to create a new
        DynamoDBServiceResource instance configured for the given region
        and with the provided botocore configuration.

        The endpoint URL is constructed using the region name.
        """

        return resource(
            "dynamodb",
            region_name=region_name,
            config=config,
            endpoint_url=f"https://dynamodb.{region_name}.amazonaws.com/",
        )

    def scan_items(self, table_name: str, index_name: str | None = None) -> list:
        """Scans items from a DynamoDB table.

        Parameters:
        - table_name (str): The name of the table to scan.
        - index_name (str|None): The name of a secondary index to scan.
            Default None.

        Use the DynamoDB Scan API to paginate through results.

        Injects attribute value transformation to deserialize DynamoDB
        types.

        Returns the list of scanned items if successful.

        Raises ClientError on failure.
        """

        paginator = self.__client.get_paginator("scan")
        operation_parameters = {"TableName": table_name}

        if index_name:
            operation_parameters["IndexName"] = index_name

        page_iterator = paginator.paginate(**operation_parameters)
        service_model = self.__client._service_model.operation_model("Scan")
        try:
            for page in page_iterator:
                self.__transformation.inject_attribute_value_output(page, service_model)
                status_code = page.get("ResponseMetadata").get("HTTPStatusCode")
                if status_code == 200:
                    return page["Items"]
        except ClientError as error:
            LOGGER.error(f"Failed to scan table {table_name} table due to {repr(error)}")
            raise

    def put_item(self, table_name: str, item: dict) -> dict:
        """Puts an item into a DynamoDB table.

        Parameters:
        - table_name (str): The name of the table.
        - item (dict): The item to put as a dict.

        Get the table resource.

        Call put_item() to add the item to the table.

        Log a message on success.

        Raises:
        - ClientError: If the put_item call fails.

        Returns:
        - dict: The response from DynamoDB.
        """

        table = self.__resource.Table(table_name)

        try:
            item = table.put_item(Item=item)
            LOGGER.info(f"Put item into {table_name} table")
            return item
        except ClientError as error:
            LOGGER.error(f"Failed to put item into {table_name} table due to {error}")
            raise

    def batch_put_items(self, table_name: str, items) -> None:
        """Batch puts multiple items into a DynamoDB table.

        Parameters:
        - table_name (str): The name of the table.
        - items (list): A list of item dicts to put.

        Get the table resource.

        Use the table's batch_writer() context manager to put each item.

        Logs the number of items put on success.

        Raises:
        - ClientError: If there is an error batch putting.
        """

        table = self.__resource.Table(table_name)

        try:
            with table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)
            LOGGER.info(f"Put {len(items)} items into {table_name} table")
        except ClientError as error:
            LOGGER.error(f"Failed to batch put for {table_name} table due to {error}")
            raise

    def delete_item(self, table_name, item: dict) -> dict:
        """Deletes an item from a DynamoDB table.

        Parameters:
        - table_name (str): The name of the table.
        - item (dict): The primary key of the item to delete.

        Get the table resource.

        Call delete_item() to delete the item.

        Log a message on success.

        Raises:
        - ClientError: If the delete_item call fails.

        Returns:
        - dict: The response from DynamoDB.
        """

        table = self.__resource.Table(table_name)

        try:
            item = table.delete_item(Key=item)
            LOGGER.info(f"Delete item in {table_name} table")
            return item
        except ClientError as error:
            LOGGER.error(f"Failed to delete item from {table_name} table due to {error}")
            raise

    def get_item(self, table_name, key: dict) -> dict:
        """Gets an item from a DynamoDB table.

        Parameters:
        - table_name (str): The name of the table.
        - key (dict): The primary key of the item to get.

        Get the table resource.

        Call get_item() to retrieve the item.

        Log a message on success.

        Raises:
        - ClientError: If the get_item call fails.

        Returns:
        - dict: The requested item if found, else None.
        """

        table = self.__resource.Table(table_name)

        try:
            response = table.get_item(Key=key)
            LOGGER.info(f"Got item from {table_name} table")
            return response.get("Item")
        except ClientError as error:
            LOGGER.error(f"Failed to get item from {table_name} table due to {error}")
            raise

    def update_item(
        self,
        table_name,
        key,
        expression=None,
        values=Mapping[
            str,
            bytes
            | bytearray
            | str
            | int
            | Decimal
            | bool
            | set[int]
            | set[Decimal]
            | set[str]
            | set[bytes]
            | set[bytearray]
            | Sequence
            | Mapping[str, Any]
            | None,
        ],
        condition="",
    ):
        """Updates an item in a DynamoDB table.

        parameters:
        - table_name (str): The name of the table.
        - key (dict): The primary key of the item to update.
        - expression (dict): The update expression defining the update.
        - values (str): The expression attribute value mappings.
        - condition (str): An optional condition expression.

        get the table resource.

        call update_item() to update the item.

        log a message on success.

        raises:
        - ClientError: If the update fails.

        the update expression and expression attribute values are optional.
        """

        if expression is None:
            expression = {}
        table = self.__resource.Table(table_name)
        try:
            table.update_item(
                Key=key,
                UpdateExpression=expression,
                ExpressionAttributeValues=values,
                ConditionExpression=condition,
            )
            LOGGER.info(f"Updated item in {table_name} table")
        except ClientError as error:
            LOGGER.error(f"Failed to update item in {table_name} table due to {repr(error)}")
            raise

    def get_items(self, table_name, filter_expression=None):
        """Gets items from a DynamoDB table.

        Parameters:
        - table_name (str): The name of the table.
        - filter_expression (str): Optional filter expression to apply.

        Get the table resource.

        Performs a scan on the table, with optional filter.

        Paginates through all results using LastEvaluatedKey.

        Log the number of items returned.

        Raises:
        - ClientError: If there is an error scanning.

        Returns:
        - list: The list of item dicts returned.
        """

        table = self.__resource.Table(table_name)

        try:
            if filter_expression:
                response = table.scan(FilterExpression=filter_expression)
            else:
                response = table.scan()
            data = response["Items"]
            while "LastEvaluatedKey" in response:
                response = table.scan(
                    ExclusiveStartKey=response["LastEvaluatedKey"],
                    FilterExpression=filter_expression,
                )
                data.extend(response["Items"])
            LOGGER.info(f"Got {len(data)} items from {table_name} table")
            return data
        except ClientError as error:
            LOGGER.error(f"Failed to scan items from {table_name} table due to {error}")
            raise

    def get_items_page(self, table_name, filter_expression, last_evaluated_key=None, limit=500) -> dict:
        """Gets a page of items from a DynamoDB table.

        Parameters:
        - table_name (str): The name of the table.
        - filter_expression (str): Filter expression to apply.
        - last_evaluated_key (dict): The primary key of the last
            evaluated item from a previous page.
        - limit (int): Max number of items to return.
        Default 500.

        Get the table resource.

        Performs a scan on the table with filter and optional
        exclusive start key to get the next page.

        Log the number of items returned.

        Raises:
        - ClientError: If there is an error scanning.

        Returns:
        - dict: The scan response dict.
        Example below:
        {
            "Count": 1,
            "Items": [
                {
                    "id": "1"
                }
            ],
            "ResponseMetadata": {
                "HTTPHeaders": {
                    "date": "Fri, 22 Dec 2023 11:36:47 GMT",
                    "server": "amazon.com",
                    "x-amz-crc32": "2265552731",
                    "x-amzn-requestid": "PSIzQd5QRblPIUG5joY8s37l1U45VyAdlp8Be9PNWDHFlMfKadVN"
                },
                "HTTPStatusCode": 200,
                "RequestId": "PSIzQd5QRblPIUG5joY8s37l1U45VyAdlp8Be9PNWDHFlMfKadVN",
                "RetryAttempts": 0
            },
            "ScannedCount": 2
        }
        """

        table = self.__resource.Table(table_name)
        try:
            if last_evaluated_key is None:
                response = table.scan(FilterExpression=filter_expression, Limit=limit)
            else:
                response = table.scan(
                    ExclusiveStartKey=last_evaluated_key,
                    FilterExpression=filter_expression,
                    Limit=limit,
                )
            LOGGER.info(f"Got {response['Count']} items from {table_name} table")
            return response
        except ClientError as error:
            LOGGER.error(f"Failed to scan items from {table_name} table due to {error}")
            raise

    def query(self, table_name, **kwargs) -> list:
        """Queries items from a DynamoDB table.

        Parameters:
        - table_name (str): The name of the table to query.
        - **kwargs: Query parameters like KeyConditionExpression,
            ExpressionAttributeValues, etc.

        Get the table resource.

        Perform the query on the table with the provided parameters.

        Paginates through all results using LastEvaluatedKey.

        Log the number of items returned.

        Raises:
        - ClientError: If there is an error querying.

        Returns:
        - list: The list of item dicts returned by the query.
        """

        table = self.__resource.Table(table_name)
        try:
            response = table.query(**kwargs)
            data = response["Items"]
            while "LastEvaluatedKey" in response:
                kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
                response = table.query(**kwargs)
                data.extend(response["Items"])
            LOGGER.info(f"Got {len(data)} items from {table_name} table")
            return data
        except ClientError as error:
            LOGGER.error(f"Failed to query items from {table_name} table due to {repr(error)}")
            raise
