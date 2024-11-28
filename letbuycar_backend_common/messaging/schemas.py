from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum


class MessageType(str, Enum):
    IS_PHOTO = 'is_photo'
