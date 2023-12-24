"""Simplify operations against AWS Simple Email Service using AWS Python SDK
boto3."""
import os

from pathlib import Path

from aws_lambda_powertools import Logger
from boto3 import client
from botocore.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_ses.client import SESClient

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class SESService:
    """Simplify sending emails - text and html with attachment via AWS Simple Email Service."""

    def __init__(self, region_name="eu-west-1"):
        """Initializes an SESService instance.

        Parameters:
        - region_name (str): The AWS region name (default 'eu-west-1').

        Create an SES client with retry configuration.
        """

        config = Config(retries={"max_attempts": 10, "mode": "adaptive"})
        self.__ses = self.create_client(region_name=region_name, config=config)

    @staticmethod
    def create_client(region_name: str, config: Config) -> SESClient:
        """Creates an SES client.

        Parameters:
        - region_name (str): The AWS region for the client.
        - config (botocore.config.Config): The botocore configuration for the client.

        Returns:
        - SESClient: The SES client instance.

        Use the boto3 client() function to create a new SESClient
        configured for the given region and with the provided botocore configuration.
        """

        return client("ses", region_name=region_name, config=config)

    def send_email(
        self,
        email_body_text: str,
        email_body_html: str,
        destination: str,
        sender: str,
        subject: str,
    ) -> bool:
        """Sends an email using SES.

        Parameters:
        - email_body_text (str): The text body of the email.
        - email_body_html (str): The HTML body of the email.
        - destination (str): The recipient email address.
        - sender (str): The sender email address.
        - subject (str): The subject of the email.

        Call SES SendEmail API to send the email.

        Log and check the response.

        Raises:
        - ValueError: If the sending fails.

        Returns:
        - bool: True if the sending succeeded, False otherwise.
        """

        charset = "UTF-8"

        try:
            response = self.__ses.send_email(
                Destination={"ToAddresses": [destination]},
                Message={
                    "Body": {
                        "Html": {"Charset": charset, "Data": email_body_html},
                        "Text": {"Charset": charset, "Data": email_body_text},
                    },
                    "Subject": {"Charset": charset, "Data": subject},
                },
                Source=sender,
            )
            LOGGER.info(f"Email response: {response}")

            if response.get("ResponseMetadata").get("HTTPStatusCode") != 200:
                LOGGER.error(f"Message not sent due to: {response}")
                raise ValueError(f"Message not sent due to: {response}")
            LOGGER.info(f"Email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
            LOGGER.error(e.response["Error"]["Message"])
            raise

        return True

    # pylint: disable=C0415
    def send_raw_email(
        self,
        email_body_html: str,
        destinations: list,
        sender: str,
        subject: str,
        attachment_list: list | None = None,
        picture_list: list | None = None,
    ) -> bool:
        """Sends a raw email using SES.

        Parameters:
        - email_body_html (str): The HTML body of the email.
        - destinations (list): List of recipient email addresses.
        - sender (str): The sender email address.
        - subject (str): The subject of the email.
        - attachment_list (list): Optional list of attachment file paths.
        - picture_list (list): Optional list of embedded picture file paths.

        Creates a MIMEMultipart message with HTML body, subject, sender, recipients.

        Attach any attachments and embedded pictures.

        Call SES SendRawEmail API to send the raw MIME message.

        Log and check the response.

        Raises:
        - ValueError: If the sending fails.

        Returns:
        - bool: True if the sending succeeded, False otherwise.
        """

        from email.mime.application import MIMEApplication
        from email.mime.image import MIMEImage
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = ", ".join(destinations)

        part = MIMEText(email_body_html, "html")
        message.attach(part)

        # attachment
        if attachment_list:
            for attachment in attachment_list:
                attachment_name = attachment.split("/")[-1]
                _attachment = Path(attachment)
                with _attachment.open("rb") as file:
                    part = MIMEApplication(file.read())  # type: ignore
                part.add_header("Content-Disposition", "attachment", filename=attachment_name)
                message.attach(part)

        # picture attachment
        if picture_list:
            for picture in picture_list:
                picture_name = picture.split("/")[-1]
                _picture_name = Path(picture_name)
                with _picture_name.open("rb") as file:
                    part = MIMEImage(file.read(), name=picture_name)  # type: ignore
                message.attach(part)

        try:
            response = self.__ses.send_raw_email(
                Source=message["From"],
                Destinations=destinations,
                RawMessage={"Data": message.as_string()},
            )

            LOGGER.info(f"Response RAW email: {response}")

            if response.get("ResponseMetadata").get("HTTPStatusCode") != 200:
                LOGGER.error(f"Message not sent due to: {response}")
                raise ValueError(f"Message not sent due to: {response}")
            LOGGER.info(f"Email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
            LOGGER.error(e.response["Error"]["Message"])
            raise

        return True
