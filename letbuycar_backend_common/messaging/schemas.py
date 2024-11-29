from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum


class MessageType(str, Enum):
    IS_CARGO_IMAGES = 'IS_CARGO_IMAGES'
