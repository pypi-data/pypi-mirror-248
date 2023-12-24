"""Wrapper around default AWS SDK for using Systems Manager Parameter Store."""
import os

from typing import Literal

from aws_lambda_powertools import Logger
from boto3 import client
from botocore.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_ssm.client import SSMClient

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class SSMService:
    """Wrapper around default AWS SDK for using Systems Manager Parameter
    Store."""

    def __init__(self, region_name: str = "eu-west-1"):
        """Class init.

        :param region_name: The AWS region name which contains SSM
            Parameter store keys.
        """
        config = Config(retries={"max_attempts": 10, "mode": "adaptive"})
        self.__ssm = self.create_client(region_name=region_name, config=config)

    @staticmethod
    def create_client(region_name: str, config: Config) -> SSMClient:
        """Create a new SSM client.

        :return: A new SSM client
        """
        return client("ssm", region_name=region_name, config=config)

    def get_parameter(self, parameter: str, with_decryption: bool = True) -> str | None:
        """Deletes a parameter from AWS SSM Parameter Store.

        Parameters:
        - parameter_name (str): The name of the parameter to delete.

        Use the SSM delete_parameter API to delete the specified parameter.

        Log a message on success or failure.

        Raises:
        - ClientError: If the delete operation fails.
        """

        try:
            response = self.__ssm.get_parameter(Name=parameter, WithDecryption=with_decryption)
            LOGGER.info(f"Got param {parameter} from ssm")
            return response["Parameter"]["Value"]
        except ClientError:
            LOGGER.error(
                f"Failed to get SSM param {parameter}",
            )
            raise

    def get_parameters(self, parameters: list, with_decryption: bool = True) -> list:
        """Gets multiple parameters from SSM Parameter Store.

        Parameters:
        - parameters (list): A list of parameter names to get.
        - with_decryption (bool): Whether to decrypt secure string parameters.
            Default True.

        Returns:
        - list: A list containing the value of each parameter.

        For each parameter name, call get_parameter() to retrieve the
        value.
        Returns the list of parameter values.
        """

        return [self.get_parameter(x, with_decryption) for x in parameters]

    def get_parameters_dict(self, parameters, with_decryption: bool = True) -> dict:
        """Gets multiple SSM parameters and returns them as a dictionary.

        Parameters:
        - parameters (list): The list of parameter names to get.
        - with_decryption (bool): Whether to decrypt secure string parameters.
            Default True.

        Returns:
        - dict: A dictionary with the parameter names as keys and parameter
            values as values.

        Gets parameters in batches of 10 using get_parameters.

        Constructs a dictionary from the returned parameters with the
        parameter name as the key and value as the value.

        Raises:
        - ClientError: If there is an error calling SSM.
        """

        try:
            LOGGER.info(f"Getting params {parameters} from ssm")
            ssm_parameters = []
            parameters = parameters.copy()
            while len(parameters) > 0:
                params = parameters[:10]
                del parameters[:10]
                ssm_parameters.extend(
                    self.__ssm.get_parameters(Names=params, WithDecryption=with_decryption)["Parameters"],
                )

            return {param["Name"]: param["Value"] for param in ssm_parameters}
        except ClientError:
            LOGGER.error(
                f"Failed to get SSM params {parameters}",
            )
            raise

    def delete_parameter(self, parameter_name: str):
        """Deletes a parameter from AWS SSM Parameter Store.

        Parameters:
        - parameter_name (str): The name of the parameter to delete.

        Raises:
        - Exception: If an error occurs deleting the parameter.

        Returns: None.
        Delete the SSM parameter.
        """

        try:
            LOGGER.info(f"Deleting parameter for {parameter_name}")
            self.__ssm.delete_parameter(Name=parameter_name)
        except Exception as error:
            LOGGER.error(f"Failed to delete SSM parameter {parameter_name} {error}")
            raise

    def create_parameter(
        self,
        parameter_name: str,
        description: str,
        key_id: str,
        value: str,
        parameter_type: Literal["String", "SecureString", "StringList"] = "SecureString",
    ):
        """Creates a new parameter in AWS SSM Parameter Store.

        Parameters:
        - parameter_name (str): The name of the parameter to create.
        - description (str): A description for the parameter.
        - key_id (str): The KMS key ID to use to encrypt the parameter value.
        - value (str): The value to store in the parameter.
        - parameter_type (Literal["String", "SecureString"], optional): The type of parameter to create.
            defaults to "SecureString".

        raises:
        - Exception: If an error occurs, create the parameter.

        returns: None.
        create the SSM parameter.
        """

        try:
            LOGGER.info(f"Creating parameter for {parameter_name}")
            self.__ssm.put_parameter(
                Name=parameter_name,
                Description=description,
                Value=value,
                Type=parameter_type,
                KeyId=key_id,
                Overwrite=True,
            )
        except Exception as error:
            LOGGER.error(f"Failed to create SSM parameter {parameter_name} {error}")
            raise
