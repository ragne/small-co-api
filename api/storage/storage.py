from os import path
from typing import BinaryIO

from botocore.exceptions import ClientError
from flask import current_app
import mimetypes


import boto3


def mime_by_filename(filename: str) -> str:
    mime, _ = mimetypes.guess_type(filename)
    return mime if mime else "application/octet-stream"


def get_s3_client():
    s3 = boto3.resource("s3")
    if current_app.config["DEBUG"]:
        print("in debug")
        s3 = boto3.resource("s3", endpoint_url="http://localhost:8000")
    return s3


def upload_file(
    file: BinaryIO, filename: str, bucket: str, prefix: str = "/", **extra_meta
):
    # @todo: error handling
    s3 = get_s3_client()
    bucket = s3.Bucket(bucket)
    bucket.create()
    return bucket.upload_fileobj(
        file,
        path.join(prefix, filename),
        ExtraArgs={"ContentType": mime_by_filename(filename), "Metadata": extra_meta},
    )


def get_file(filename: str, bucket: str, prefix: str = "/") -> (str, BinaryIO):
    s3 = get_s3_client()
    obj = s3.Object(bucket, path.join(prefix, filename)).get()
    return obj["ContentType"], obj["Body"]


def delete_file(filename: str, bucket: str, prefix: str = "/"):
    s3 = get_s3_client()
    obj = s3.Object(bucket, path.join(prefix, filename))
    return obj.delete()


def file_exists(filename: str, bucket: str, prefix: str = "/") -> bool:
    s3 = get_s3_client()
    obj = s3.Object(bucket, path.join(prefix, filename))
    try:
        obj.load()
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False


def health_status() -> bool:
    try:
        from ..app import S3_BUCKET

        s3 = get_s3_client()
        s3.Bucket(S3_BUCKET).load()
        return True
    except Exception:
        return False
