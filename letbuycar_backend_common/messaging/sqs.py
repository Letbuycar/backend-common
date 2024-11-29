import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os
from .schemas import MessageType


class SQSService:
    def __init__(self):
        AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
        AWS_SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')
        self.client = boto3.client(
            "sqs",
            region_name=AWS_REGION_NAME
        )
        self.queue_url = AWS_SQS_QUEUE_URL

    def send_message(self, message_body: MessageType, attrs: dict = None) -> dict:
        try:
            
            message_attributes = {}
            for key, value in (attrs or {}).items():
                if isinstance(value, bool):
                    message_attributes[key] = {
                        "StringValue": "1" if value else "0",
                        "DataType": "Number"
                    }
                elif isinstance(value, int) or isinstance(value, float):
                    message_attributes[key] = {
                        "StringValue": str(value),
                        "DataType": "Number"
                    }
                else:
                    message_attributes[key] = {
                        "StringValue": str(value),
                        "DataType": "String"
                    }
                
            print('message_attributes', message_attributes)


            response = self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                DelaySeconds=0,
                MessageAttributes=message_attributes
            )
            return response
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Ошибка отправки сообщения: {e}")

    def receive_messages(self) -> list:
        try:
            response = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10,
                MessageAttributeNames=["All"],
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
        