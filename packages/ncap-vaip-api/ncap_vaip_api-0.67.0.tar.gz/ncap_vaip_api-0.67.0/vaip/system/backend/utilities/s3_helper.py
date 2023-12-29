import os
import logging

def check_for_content(s3_client, bucket, key):
    """
    Checks content exists.
    :param s3_client: Use the same client to save some effort.
    :param key: Object key
    :param bucket: Object bucket

    with json extension. Added an AIP folder before the basename.
    :return: None if no AIP already exists. The JSON if so.
    """
    try:
        s3_client.head_object(
            Bucket=bucket,
            Key=key
        )
        logging.info("Foundobject. Will return it.")
        content = s3_client.get_object(
            Bucket=bucket,
            Key=key
        )
        return content["Body"].read()
    except s3_client.exceptions.ClientError:
        logging.debug("No key currently exists. Make a new one.")
        return None

def write_s3_content(client, body, bucket, key):
    """
    Write content to s3
    :param client: Use the same s3 client to save effort.
    :param body: Content to persist to s3
    :param key: Object key
    :param bucket: Object bucket
    :return: n/a
    """

    return client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body.encode('utf-8'),
        StorageClass='STANDARD'
    )

def get_filename(path):
    basename = os.path.basename(path)
    return basename