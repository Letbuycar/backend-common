from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'Admin'
    MANAGER = 'Manager'
    ACCOUNTANT = 'Accountant'
    DEALER = 'Dealer'
    LOGISTICIAN = 'Logistician'
    BROKER = 'Broker'
    CUSTOMER = 'Customer'


class UserSchema(BaseModel):
    sub: UUID
    email: EmailStr
    email_verified: bool
    role: UserRole
    