"""Library to simplify working with SQS."""
import json
import os

from collections.abc import Sequence
from typing import Literal

from aws_lambda_powertools import Logger
from boto3 import client
from botocore.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_sqs.client import SQSClient

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]))


class BatchProcessingFailedException(Exception):
    """Raise for failed messages during processing in batch."""


class SQSService:
    """Simplify queue operations via AWS Simple Queue Service."""

    def __init__(self, region_name="eu-west-2"):
        """Initializes a SQSService instance.

        Parameters:
        - region_name (str): The AWS region name (default 'eu-west-2')

        Create an SQS client with retry configuration.
        """

        config = Config(retries={"max_attempts": 10, "mode": "adaptive"})

        self.sqs = self.create_client(region_name=region_name, config=config)

    @staticmethod
    def create_client(region_name: str, config: Config) -> SQSClient:
        """Creates an SQS client.

        Parameters:
        - region_name (str): The AWS region for the client.
        - config (botocore.config.Config): The botocore configuration for the client.

        Returns:
        - SQSClient: The SQS client instance.

        Use the boto3 client() function to create a new SQSClient
        configured for the given region and with the provided botocore configuration.
        """
        return client("sqs", region_name=region_name, config=config)

    def send_message_to_fifo(self, message: dict, queue_url: str):
        """Sends a message to a FIFO SQS queue.

        Parameters:
        - message (dict): The message to send. Must contain MessageBody, DelaySeconds,
          MessageAttributes, MessageGroupId and MessageDeduplicationId fields.
        - queue_url (str): The URL of the FIFO SQS queue.

        Calls SQS SendMessage API to send the message to the queue.

        Logs success or failure.

        Raises:
        - ClientError: If the sending fails.
        """

        try:
            self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message["MessageBody"],
                DelaySeconds=message["DelaySeconds"],
                MessageAttributes=message["MessageAttributes"],
                MessageGroupId=message["MessageGroupId"],
                MessageDeduplicationId=message["Id"],
            )
            LOGGER.info(f"Message sent to queue {queue_url}")
        except ClientError:
            LOGGER.error(f"Failed to send message to queue {queue_url}")
            raise

    def send_message(self, message: dict, queue_url: str):
        """Sends a message to an SQS queue.

        Parameters:
        - message (dict): The message to send. Must contain a MessageBody field. Can optionally
          contain DelaySeconds and MessageAttributes.
        - queue_url (str): The URL of the SQS queue.

        Calls SQS SendMessage API to send the message to the queue.

        Logs success or failure.

        Raises:
        - ClientError: If the send fails.
        """

        try:
            self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message["MessageBody"],
                DelaySeconds=message.get("DelaySeconds", 0),
                MessageAttributes=message.get("MessageAttributes", {}),
            )
            LOGGER.info(f"Message sent to queue {queue_url}")
        except ClientError:
            LOGGER.error(f"Failed to send message to queue {queue_url}")
            raise

    @staticmethod
    def _retry_failed_messages(queue_url: str, response, messages, retry, retry_function):
        """Retries failed messages from a batch SQS send.

        Parameters:
        - queue_url (str): The SQS queue URL.
        - response (dict): The response from the batch send operation.
        - messages (list): The original list of messages that was sent.
        - retry (int): The number of times to retry failed messages.
        - retry_function: The batch sends function to use for retrying.

        Get any failed messages from the response.
        Retries sending those failed messages up to the retry limit.
        Raises error if any messages still fail after all retries.

        It Can be used to retry failures from send_message_batch().
        """

        failed = response.get("Failed")
        while failed and retry > 0:
            LOGGER.info(f"Retry {len(failed)} failed messages")
            failed_ids = [fail["Id"] for fail in failed]
            failed_messages = [message for message in messages if message["Id"] in failed_ids]
            response = retry_function(QueueUrl=queue_url, Entries=failed_messages)
            failed = response.get("Failed")
            retry -= 1
        if failed:
            LOGGER.error(f"Failed to process message batch {queue_url} due to {json.dumps(failed)}")
            raise BatchProcessingFailedException()

    def send_messages(self, messages: list[dict], queue_url: str, retry=3):
        """Sends a batch of messages to an SQS queue.

        parameters:
        - messages (list): The list of messages to send.
        - queue_url (str): The URL of the SQS queue.
        - retry (int): Number of times to retry failed messages in the batch.

        sends the messages in batches of 10 (chunk_size).

        calls SQS SendMessageBatch API to send each batch.

        retries any failed messages from each batch up to the retry limit.

        logs total number of messages sent.

        raises:
        - ClientError: If the batch sending fails.
        """

        try:
            chunk_size = 10
            for idx in range(0, len(messages), chunk_size):
                chunk = messages[idx : idx + chunk_size]
                response = self.sqs.send_message_batch(QueueUrl=queue_url, Entries=chunk)
                self._retry_failed_messages(queue_url, response, chunk, retry, self.sqs.send_message_batch)
            LOGGER.info(f"Sent {len(messages)} message to queue {queue_url}")
        except ClientError:
            LOGGER.error(f"Failed to send message batch to queue {queue_url}")
            raise

    def receive_messages(self, queue_url: str, **kwargs):
        """Receives messages from an SQS queue.

        parameters:
        - queue_url (str): The URL of the SQS queue.

        Keyword Arguments:
        - max_number_of_messages (int): Max number of messages to receive (default 1).
        - attribute_names (list): Names of attributes to receive (default "All").
        - max_messages (int): Max number of messages to receive per poll (default 10).
        - message_attribute_names (list): Names of message attributes to receive (default "All").
        - wait_time (int): Wait time for long polling (default 3).

        calls SQS ReceiveMessage API to receive messages from the queue.
        gets messages in batches up to max_messages per poll.
        continues polling until max_number_of_messages is reached.

        returns a list of received message objects.

        raises:
        - ClientError: If receive fails.
        """
        attribute_names: Sequence[
            Literal[
                "AWSTraceHeader",
                "All",
                "ApproximateFirstReceiveTimestamp",
                "ApproximateNumberOfMessages",
                "ApproximateNumberOfMessagesDelayed",
                "ApproximateNumberOfMessagesNotVisible",
                "ApproximateReceiveCount",
                "ContentBasedDeduplication",
                "CreatedTimestamp",
                "DeduplicationScope",
                "DelaySeconds",
                "FifoQueue",
                "FifoThroughputLimit",
                "KmsDataKeyReusePeriodSeconds",
                "KmsMasterKeyId",
                "LastModifiedTimestamp",
                "MaximumMessageSize",
                "MessageDeduplicationId",
                "MessageGroupId",
                "MessageRetentionPeriod",
                "Policy",
                "QueueArn",
                "ReceiveMessageWaitTimeSeconds",
                "RedriveAllowPolicy",
                "RedrivePolicy",
                "SenderId",
                "SentTimestamp",
                "SequenceNumber",
                "SqsManagedSseEnabled",
            ]
        ] = [kwargs.get("attribute_names", "All")]  # type: ignore

        try:
            num_of_messages = kwargs.get("max_number_of_messages", 1)
            messages = []

            while num_of_messages > 0:
                max_messages = min(num_of_messages, 10)
                response = self.sqs.receive_message(
                    QueueUrl=queue_url,
                    AttributeNames=attribute_names,
                    MaxNumberOfMessages=kwargs.get("max_messages", max_messages),
                    MessageAttributeNames=[kwargs.get("message_attribute_names", "All")],
                    WaitTimeSeconds=kwargs.get("wait_time", 3),
                )
                new_messages = response.get("Messages", [])
                if not new_messages:
                    LOGGER.info("No messages in queue")
                    return "No messages in queue"
                messages.extend(new_messages)
                num_of_messages -= max_messages
            LOGGER.info(f"Received {len(messages)} messages from queue {queue_url}")
            return messages
        except ClientError:
            LOGGER.error(f"Failed to receive messages from queue {queue_url}")
            raise

    def delete_message(self, queue_url: str, receipt_handle: str):
        """Deletes a message from an SQS queue.

        Parameters:
        - queue_url (str): The URL of the SQS queue.
        - receipt_handle (str): The receipt handle of the message to delete.

        Calls SQS DeleteMessage API to delete the message.

        Raises:
        - ClientError: If the deleting fails.
        """

        try:
            self.sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
            LOGGER.debug("Removed message from queue")
        except ClientError:
            LOGGER.error(f"Failed to delete message from queue {queue_url}")
            raise

    def delete_messages(self, queue_url: str, messages, retry=3):
        """Deletes a batch of messages from an SQS queue.

        parameters:
        - queue_url (str): The URL of the SQS queue.
        - messages (list): The list of messages to delete.
        - retry (int): Number of times to retry failed deletes.

        delete the messages in batches of 10 (chunk_size).

        calls SQS DeleteMessageBatch API to delete each batch.

        retries any failed deleting from each batch up to the retry limit.

        logs total number of messages deleted.

        raises:
        - ClientError: If the batch deleting fails.
        """

        try:
            chunk_size = 10
            for i in range(0, len(messages), chunk_size):
                chunk = messages[i : i + chunk_size]
                entries = [{"Id": x["MessageId"], "ReceiptHandle": x["ReceiptHandle"]} for x in chunk]
                response = self.sqs.delete_message_batch(QueueUrl=queue_url, Entries=entries)
                self._retry_failed_messages(queue_url, response, chunk, retry, self.sqs.delete_message_batch)
            LOGGER.info(f"Deleted {len(messages)} message from queue {queue_url}")
        except ClientError:
            LOGGER.error(f"Failed to delete messages from queue {queue_url}")
            raise

    def get_queue_attr(self, queue_url: str, attribute_names: list):
        """Get queue attributes.

        Parameters:
        - queue_url (str): The URL of the SQS queue to get attributes for.
        - attribute_names (list): A list of attribute names to get.

        Returns:
        - dict: A dictionary containing the requested attributes.

        Calls the SQS GetQueueAttributes API to get the requested
        attributes for the specified queue.

        Log the retrieved attributes at info level.

        Raises:
        - ClientError: If the API call fails.
        """

        try:
            response = self.sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=attribute_names)
            LOGGER.info(f"Got {attribute_names} attributes for queue {queue_url}")
            return response["Attributes"]
        except ClientError:
            LOGGER.error(f"Failed to get attributes for queue {queue_url}")
            raise

    def queue_has_messages(self, queue_name: str) -> int:
        """Check if a queue has messages available.

        Parameters:
        - queue_name (str): The name of the SQS queue to check.

        Returns:
        - bool: True if the queue has messages, False otherwise.

        Get the ApproximateNumberOfMessages attribute from the queue.
        Compare it to 0 to determine if messages are available.
        """

        attr = self.get_queue_attr(queue_name, ["ApproximateNumberOfMessages"])
        return int(attr["ApproximateNumberOfMessages"]) > 0

    def queue_has_messages_in_flight(self, queue_name: str) -> int:
        """Check if a queue has messages in flight.

        Parameters:
        - queue_name (str): The name of the SQS queue to check.

        Returns:
        - bool: True if the queue has messages in flight, False otherwise.

        Get the ApproximateNumberOfMessagesNotVisible attribute from the queue.
        Compare it to 0 to determine if messages are in flight.

        Messages in flight are messages that have been retrieved from the queue but
        have not yet been deleted after being processed.
        """

        attr = self.get_queue_attr(queue_name, ["ApproximateNumberOfMessagesNotVisible"])
        return int(attr["ApproximateNumberOfMessagesNotVisible"]) > 0
