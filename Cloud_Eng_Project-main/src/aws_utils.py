import logging
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

logger = logging.getLogger("heartattack")

def upload_artifacts(artifacts: Path, config: dict) -> list[str]:
    """Upload all the artifacts in the specified directory to S3.

    Args:
        artifacts (Path): Directory containing all the artifacts from a given experiment.
        config (dict): Config required to upload artifacts to S3; see example config file for structure.

    Returns:
        list[str]: List of S3 URI's for each file that was uploaded.
    """
    bucket_name = config["bucket_name"]
    prefix = config.get("prefix", "")
    uploaded_uris = []
    try:
        s3_client = boto3.client("s3")
        logging.info("Initializing the S3 client.")
    except NoCredentialsError:
        logging.error("AWS credentials not found. Please configure your AWS CLI.")
        raise
    except PartialCredentialsError:
        logging.error("Incomplete AWS credentials. Please check your configuration.")
        raise

    for item in artifacts.iterdir():
        if item.is_file():
            try:
                s3_key = f"{prefix}/{item.name}"
                s3_client.upload_file(Filename=str(item), Bucket=bucket_name, Key=s3_key)
                s3_uri = f"s3://{bucket_name}/{s3_key}"
                uploaded_uris.append(s3_uri)
                logger.info("Successfully uploaded %s to %s", item, s3_uri)
            except Exception as err:
                logging.error("Failed to upload %s: %s", item, str(err))
                raise
    return uploaded_uris
