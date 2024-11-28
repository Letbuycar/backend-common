import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os
from .schemas import MessageType


class SQSService:
    def __init__(self, AWS_REGION_NAME, AWS_SQS_QUEUE_URL):
        if not AWS_REGION_NAME:
            AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
        if not AWS_SQS_QUEUE_URL:
            AWS_SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')
        self.client = boto3.client(
            "sqs",
            region_name=AWS_REGION_NAME
        )
        self.queue_url = AWS_SQS_QUEUE_URL

    def send_message(self, message_body: MessageType, attrs: dict = None) -> dict:
        try:
            response = self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                DelaySeconds=0,
                MessageAttributes=attrs
            )
            return response
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Ошибка отправки сообщения: {e}")

    def receive_messages(self, max_messages: int = 1, wait_time: int = 10) -> list:
        try:
            response = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
            )
            return response.get("Messages", [])
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Ошибка получения сообщений: {e}")

    def delete_message(self, receipt_handle: str) -> None:
        try:
            self.client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle,
            )
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Ошибка удаления сообщения: {e}")
        