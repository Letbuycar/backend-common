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
            
            message_attributes = self._attrs_from_dict(attrs)
            response = self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                DelaySeconds=0,
                MessageAttributes=message_attributes
            )
            return response
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Error with message send: {e}")

    def receive_messages(self, messages_number) -> list:
        try:
            response = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=messages_number,
                WaitTimeSeconds=10,
                MessageAttributeNames=["All"],
            )
            return response.get("Messages", [])
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Error with message receive: {e}")


    def receive_one_message(self) -> dict:
        try:

            messages = self.receive_messages(1)

            if not messages:
                return None
            
            message = messages[0]
            receipt_handle = message["ReceiptHandle"]

            return {
                "message_type": message["Body"],
                "message_attrs": self._attrs_to_dict(message["MessageAttributes"]),
                "receipt_handle": receipt_handle
            }
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Error with message receive: {e}")
        

    def delete_message(self, receipt_handle: str) -> None:
        try:
            self.client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle,
            )
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Error with message delete: {e}")
        

    def _attrs_from_dict(self, attrs: dict) -> dict:
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
        return message_attributes

    def _attrs_to_dict(self, attrs: dict) -> dict:
        message_attributes = {}
        for key, value in (attrs or {}).items():
            if value['DataType'] == 'Number':
                message_attributes[key] = int(value['StringValue'])
            elif value['DataType'] == 'String':
                message_attributes[key] = str(value['StringValue'])
            else:
                message_attributes[key] = value['StringValue']
        return message_attributes
