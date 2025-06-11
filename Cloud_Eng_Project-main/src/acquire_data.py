import logging
import sys
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

logger = logging.getLogger('heartattack')

def read_data(s3_uri: str) -> bytes:
    """Reads data from an S3 path.

    Args:
        s3_uri (str): The S3 URI in the format s3://bucket-name/path/to/file.

    Returns:
        bytes: The data read from the file.

    Raises:
        FileNotFoundError: If the file cannot be found in S3.
        IOError: If an error occurs during file reading.
    """
    # Parse the S3 URI
    if not s3_uri.startswith('s3://'):
        raise ValueError('The s3_uri should be in the format \'s3://bucket-name/path/to/file\'')

    s3_path = s3_uri[5:]
    bucket_name = s3_path.split('/')[0]
    key = '/'.join(s3_path.split('/')[1:])

    # Initialize a boto3 client
    s3_client = boto3.client('s3')

    try:
        # Get the object from the bucket
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read()
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            logger.error('File not found: %s. Please check the S3 URI.', s3_uri)
            raise FileNotFoundError(f'File not found in S3 bucket: {s3_uri}') from e
        logger.error('An AWS error occurred: %s', e)
        raise IOError(e) from e
    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error('Credentials issue: %s', e)
        raise IOError('AWS credential errors encountered.') from e
    except Exception as e:
        logger.error('An error occurred while reading from S3: %s', e)
        raise IOError(e) from e

def write_data(data: bytes, save_path: Path) -> None:
    """Writes data to a specified file path.

    Args:
        data: Data to be written.
        save_path: Path to the file where data should be written.
    """
    try:
        with open(save_path, 'wb') as f:
            f.write(data)
    except FileNotFoundError:
        logger.error('File not found: %s. Please check the provided file path.', save_path)
        raise
    except Exception as e:
        logger.error('An error occurred while writing data to %s: %s', save_path, e)
        raise

def acquire_data(file_path: Path, save_path: Path) -> None:
    """Acquires data from a local file and writes it to another location.

    Args:
        file_path: Local path of the data file to be read.
        save_path: Local path to write data to.
    """
    try:
        file_contents = read_data(file_path)
        write_data(file_contents, save_path)
        logger.info('Data successfully transferred from %s to %s', file_path, save_path)
    except FileNotFoundError:
        logger.error('Invalid file location provided: %s. Please check the file path.', file_path)
        sys.exit(1)
    except IOError as e:
        logger.error('I/O error occurred while transferring data: %s: %s', file_path, e)
        sys.exit(1)
