from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum


class MessageType(str, Enum):
    NOTIFICATION = 'notification'
    CARGO = 'cargo'
