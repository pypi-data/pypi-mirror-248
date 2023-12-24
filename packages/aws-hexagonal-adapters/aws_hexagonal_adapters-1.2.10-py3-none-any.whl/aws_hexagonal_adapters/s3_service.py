"""Library to simplify working with S3."""
import os

from typing import Any

from aws_lambda_powertools import Logger
from boto3 import client
from botocore.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class S3Service:
    """Simplify S3 actions."""

    def __init__(self, region_name="eu-west-1"):
        """Initializes the S3Service class.

        Parameters:
        - region_name (str, optional): The AWS region name for the S3 client.
            Defaults to "eu-west-1".

        Creates a new S3Client instance using the provided region name and
        assigns it to __s3 property.
        """
        config = Config(retries={"max_attempts": 10, "mode": "adaptive"})
        self.__s3 = self.create_client(region_name=region_name, config=config)

    @staticmethod
    def create_client(region_name: str, config: Config) -> S3Client:
        """Creates an S3 client.

        Parameters:
        - region_name (str): The AWS region name for the client.
        - config (botocore.config.Config): The botocore configuration for the client.

        Returns:
        - S3Client: The S3 client instance.

        Use the boto3 client() function to create a new S3Client instance
        configured for the given region and with the provided botocore
        configuration.
        """

        return client("s3", region_name=region_name, config=config)

    def upload(self, *, bucket: str, local_path: str, remote_path: str, extra_args=None) -> None:
        """Uploads a file to an S3 bucket.

        Parameters:
        - bucket (str): The name of the S3 bucket.
        - local_path (str): The local path of the file to upload.
        - remote_path (str): The destination path in the S3 bucket.
        - extra_args (dict, optional): Extra arguments to pass to S3 upload_file.
            Defaults to None.

        Upload the file from local_path to the given bucket and remote_path.
        Extra arguments can be passed to the S3 upload API via extra_args.

        Raises:
        - ClientError: If the file upload fails.
        """

        if extra_args is None:
            extra_args = {}
        try:
            self.__s3.upload_file(local_path, bucket, remote_path, ExtraArgs=extra_args)
            LOGGER.info(f"Uploaded file {local_path} into s3://{bucket}/{remote_path}")
        except ClientError:
            LOGGER.error(f"Failed to upload file {local_path} into s3://{bucket}/{remote_path}")
            raise

    def download(self, *, bucket: str, local_path: str, remote_path: str) -> None:
        """Downloads a file from an S3 bucket.

        parameters:
        - bucket (str): The name of the S3 bucket.
        - local_path (str): The local path to download the file to.
        - remote_path (str): The path of the file in the S3 bucket.

        download the file from the given S3 bucket and remote path
        to the specified local path.

        raises:
        - ClientError: If the file download fails.
        """

        try:
            self.__s3.download_file(bucket, remote_path, local_path)
            LOGGER.info(f"Downloaded file s3://{bucket}/{remote_path} into {local_path}")
        except ClientError:
            LOGGER.error("Failed to download file s3://{bucket}/{remote_path} into {local_path}")
            raise

    def list_files(self, *, bucket: str, prefix: str, page_size=1000) -> list[str]:
        """Lists files in an S3 bucket.

        parameters:
        - bucket (str): The name of the S3 bucket.
        - prefix (str): Only fetch keys that start with this prefix.
        - page_size (int, optional): Max number of results to return per page.
            default is 1000.

        use the S3 list_objects_v2 API to fetch a list of files in the given
        bucket that match the prefix.
        results are paged with page_size.

        returns:
        - List[str]: A list of S3 object keys.

        raises:
        - ClientError: If the file listing fails.
        """

        try:
            token = None
            files: list[str] = []
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=page_size)
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=prefix,
                        MaxKeys=page_size,
                        ContinuationToken=token,
                    )
                if "Contents" in response.keys():
                    files.extend(file["Key"] for file in response["Contents"])
                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(f"Found {len(files)} search results with prefix {prefix}")
            return files
        except ClientError:
            LOGGER.error(f"Failed to list files in bucket {bucket} with prefix {prefix}")
            raise

    def list_prefixes(self, *, bucket, delimiter, path_prefix="", page_size=1000) -> list[str]:
        """Lists prefixes in an S3 bucket using a delimiter.

        Parameters:
        - bucket (str): The name of the S3 bucket.
        - delimiter (str): The delimiter to use for grouping prefixes.
        - path_prefix (str, optional): Only fetch keys starting with this prefix.
        - page_size (int, optional): Max number of results per page.
        Default 1000.

        Use the S3 list_objects_v2 API to fetch a list of prefixes (directories)
        in the given bucket using the delimiter.
        Results are paged with page_size.

        Returns:
        - list[str]: A list of S3 prefixes.

        Raises:
        - ClientError: If the prefix listing fails.
        """

        try:
            token = None
            prefixes: list[str] = []
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=path_prefix,
                        Delimiter=delimiter,
                        MaxKeys=page_size,
                    )
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=path_prefix,
                        Delimiter=delimiter,
                        MaxKeys=page_size,
                        ContinuationToken=token,
                    )
                if "CommonPrefixes" in response.keys():
                    prefixes.extend(
                        prefix["Prefix"].replace(path_prefix, "").replace(delimiter, "")
                        for prefix in response["CommonPrefixes"]
                    )

                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(f"Found {len(prefixes)} prefixes with delimiter {delimiter}")
            return prefixes
        except ClientError:
            LOGGER.error(f"Failed to list prefixes in bucket {bucket} with delimiter {delimiter}")
            raise

    def delete_object(self, *, bucket: str, key: str) -> None:
        """Deletes an object from an S3 bucket.

        Parameters:
        - bucket (str): The name of the S3 bucket.
        - key (str): The key of the object to delete.

        Use the S3 delete_object API to delete the specified object.

        Log a message if the object is deleted successfully.

        Raises:
        - ClientError: If the deleting fails, including if the object does not exist.
        """

        try:
            self.__s3.delete_object(Bucket=bucket, Key=key)
            LOGGER.info(f"Deleted file s3://{bucket}/{key}")
        except ClientError as client_error:
            if client_error.response["Error"]["Code"] == "404":
                LOGGER.exception(f"Object not found: {bucket}, {key}")
            LOGGER.error(f"Failed to delete file s3://{bucket}/{key}")
            raise

    def delete_objects(self, *, bucket: str, keys: list[Any | None]):
        """Deletes multiple objects from an S3 bucket.

        Parameters:
        - bucket (str): The name of the S3 bucket.
        - keys (List[str]): A list of object keys to delete.

        Delete the objects in batches of 1000 using the S3
        delete_objects API.

        Log the number of objects deleted on success.

        Raises:
        - ClientError: If the bulk deleting fails.
        """

        try:
            for idx in range(0, len(keys), 1000):
                objects = [{"Key": key} for key in keys[idx : idx + 1000]]
                self.__s3.delete_objects(Bucket=bucket, Delete={"Objects": objects})  # type: ignore
            LOGGER.info(f"Deleted {len(keys)} objects from bucket {bucket}")
        except ClientError:
            LOGGER.error(f"Failed to delete objects from bucket {bucket}")
            raise

    def delete_prefix(self, *, bucket: str, prefix: str):
        """Deletes all objects with a given prefix from an S3 bucket.

        Parameters:
        - bucket (str): The name of the S3 bucket.
        - prefix (str): The prefix of objects to delete.

        Lists all objects in the bucket that match the prefix
        using list_files().

        Then delete all the listed objects using delete_objects().

        Log messages about starting and completing the deleting.
        """

        LOGGER.info(f"Deleting prefix {prefix} from bucket {bucket}")
        keys = self.list_files(bucket=bucket, prefix=prefix)
        self.delete_objects(bucket=bucket, keys=keys)
        LOGGER.info(f"Deleted prefix {prefix} from bucket {bucket}")

    def copy(self, *, source_bucket: str, source_key: str, target_bucket: str, target_key: str):
        """Copies an object from one S3 location to another.

        Parameters:
        - source_bucket (str): The source S3 bucket name.
        - source_key (str): The source object key.
        - target_bucket (str): The target S3 bucket name.
        - target_key (str): The target object key.

        Use the S3 copy API to copy the object from the source
        location to the target location.

        Log any errors, including if the source object does not exist.

        Raises:
        - ClientError: If there is an error calling S3.
        - Exception: For any unexpected errors.
        """

        try:
            copy_source = {"Bucket": source_bucket, "Key": source_key}
            self.__s3.copy(copy_source, target_bucket, target_key)
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                LOGGER.error(
                    f"Failed to copy objects s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}",
                )

        except Exception as error:
            LOGGER.critical(f"Unexpected error in download_object function of s3 helper: {error}")
            raise Exception(f"Unexpected error in download_object function of s3 helper: {error}") from error

    def move_object(self, *, source_bucket: str, source_key: str, target_bucket: str, target_key: str):
        """Moves an object from one S3 location to another.

        Parameters:
        - source_bucket (str): The source S3 bucket name.
        - source_key (str): The source object key.
        - target_bucket (str): The target S3 bucket name.
        - target_key (str): The target object key.

        First copies the object from the source location to the target
        location using copy().

        Then deletes the object from the source location using
        delete_object().

        Log a message if the object is moved successfully.

        Raises:
        - ClientError: If the copy or delete fails.
        """

        try:
            self.copy(
                source_bucket=source_bucket,
                source_key=source_key,
                target_bucket=target_bucket,
                target_key=target_key,
            )
            self.delete_object(bucket=source_bucket, key=source_key)
            LOGGER.info(f"Object moved s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}")
        except ClientError:
            LOGGER.error(
                f"Failed to move object s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}",
            )
            raise

    def move_objects(self, *, source_bucket: str, source_prefix: str, target_bucket: str, target_prefix: str):
        """Moves multiple objects from one S3 prefix to another.

        Parameters:
        - source_bucket (str): The source S3 bucket name.
        - source_prefix (str): The source prefix to move.
        - target_bucket (str): The target S3 bucket name.
        - target_prefix (str): The target prefix to move to.

        Use list_objects_v2() to get a list of objects with the source prefix.

        For each object, calls move_object() to move it to the target location,
        replacing the source prefix with the target prefix in the key.

        Moves objects in batches of 1000.

        Logs when the move starts and completes.

        Raises:
        - ClientError: If there is an error moving any object.
        """

        try:
            LOGGER.info(
                f"Starting moving objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}",
            )
            token = None
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix, MaxKeys=1000)
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=source_bucket,
                        Prefix=source_prefix,
                        MaxKeys=1000,
                        ContinuationToken=token,
                    )
                if "Contents" in response.keys():
                    for file in response["Contents"]:
                        if file["Key"] == source_prefix:
                            continue
                        target_key = f"{file['Key'].replace(source_prefix, target_prefix)}"
                        self.move_object(
                            source_bucket=source_bucket,
                            source_key=file["Key"],
                            target_bucket=target_bucket,
                            target_key=target_key,
                        )
                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(
                f"Finished moving objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}",
            )
        except ClientError:
            LOGGER.error(
                "Failed to move objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}",
            )
            raise
