from celery import Celery
from app.aws_logic import AwsService


celery_app = Celery("tasks", broker="amqp://guest:guest@rabbitmq:5672//")
aws_client = AwsService()


@celery_app.task(bind=True, max_retries=5)
def upload_image_to_s3_task(
    self, body: bytes, content_type: str, key: str, bucket: str
):
    try:
        aws_client.upload_file_to_s3(
            body=body, content_type=content_type, key=key, bucket=bucket
        )
        return "Images uploaded successfully"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
