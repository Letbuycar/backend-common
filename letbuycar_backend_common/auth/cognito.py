import boto3
import os
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from botocore.exceptions import ClientError, BotoCoreError
from .schemas import UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AWS_Common_Cognito:
    def __init__(self, AWS_REGION_NAME:str = None):
        if not AWS_REGION_NAME:
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
        
    def get_user_full_info(self, token: str):
        try:
            user_req = self.get_user(token)

            user_info = self.client.admin_get_user(
                UserPoolId=os.getenv('AWS_COGNITO_USER_POOL_ID'),
                Username=user_req['email']
            )
            return user_req
        except ClientError as e:
            return {"Error": e.response['Error']['Message']}
        except BotoCoreError as e:
            return {"Error": str(e)}
        except Exception as e:
            return {"Error": str(e)}
        
    def _get_user_role(self, user_id: UUID) -> UserRole:
        try:
            groups = self.client.admin_list_groups_for_user(
                UserPoolId=os.getenv('AWS_COGNITO_USER_POOL_ID'),
                Username=user_id
            )['Groups']
            groups_names = [group['GroupName'] for group in groups]
            if 'Admin' in groups_names:
                return UserRole.ADMIN
            if not groups_names:
                return UserRole.CUSTOMER
            return groups_names[0]
        except ClientError as e:
            return {"Error": e.response['Error']['Message']}
        except BotoCoreError as e:
            return {"Error": str(e)}
        except Exception as e:
            return {"Error": str(e)}
        
    def check_user_role(self, user_id: UUID, role: UserRole) -> bool:
        return self._get_user_role(user_id) == role
        
    def check_user_role_by_token(self, role: UserRole) -> bool:
        def dependency(token: str = Depends(oauth2_scheme)) -> bool:
            if not token:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing token")
            user = self.get_user(token)
            if not user:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing token")
            if 'Error' in user:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=user['Error'])
            has_access = self.check_user_role(user['sub'], role)
            if not has_access:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role permissions")
            return has_access
        return dependency

