import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

import os
from dotenv import load_dotenv
from app.logger import logger

load_dotenv()

environment = os.getenv("ENVIRONMENT")


# loading environment variables for development
if environment == "development":
    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
    region_name = os.getenv("region_name")


class AwsService:
    def __init__(self):
        # Clients are created once

        self.s3 = boto3.client(
            "s3",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    # ---------------- S3 ---------------- #

    def upload_file_to_s3(
        self,
        bucket: str,
        body: bytes,
        content_type: str,
        key: str,
    ) -> None:
        try:
            self.s3.put_object(
                Bucket=bucket,
                Body=body,
                ContentType=content_type,
                Key=key,
            )

        except (ClientError, BotoCoreError, NoCredentialsError) as e:
            raise RuntimeError(f"S3 upload error: {e}")

    # ---------------- presigned_url ---------------- #
    def get_s3_presigned_url(self, key: str, bucket: str, expires_in: int = 3600):
        try:
            image_url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expires_in,
            )
            return image_url
        except (ClientError, BotoCoreError, NoCredentialsError) as e:
            raise RuntimeError(f"S3 Error: {e}")

    def remove_s3_image(self, bucket: str, key: str):
        try:
            result = self.s3.delete_object(Bucket=bucket, Key=key)
            logger.info(result)

        except (ClientError, BotoCoreError, NoCredentialsError) as e:
            raise RuntimeError(f"S3 delete error: {e}")
