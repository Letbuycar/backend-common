from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserSchema(BaseModel):
    sub: UUID
    email: EmailStr
    email_verified: bool