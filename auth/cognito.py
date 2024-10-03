import boto3
import os
from botocore.exceptions import ClientError, BotoCoreError


class AWS_Common_Cognito:
    def __init__(self):

        AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
        self.client = boto3.client("cognito-idp", region_name=AWS_REGION_NAME)

    def get_user(self, token: str):
        try:
            user_req = self.client.get_user(
                AccessToken=token
            )
            user_info = {attr['Name']: attr['Value'] for attr in user_req['UserAttributes']}
            return user_info
        except ClientError as e:
            return {"Error": e.response['Error']['Message']}
        except BotoCoreError as e:
            return {"Error": str(e)}
        except Exception as e:
            return {"Error": str(e)}