from pydantic import BaseModel, EmailStr, constr, validator
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None  # Use Optional for the id field
    username: constr(min_length=3, max_length=255)  # Usernames must be between 3 and 255 characters # type: ignore
    password: constr(min_length=3, max_length=255)  # Passwords must be between 3 and 255 characters # type: ignore
    role: str  # Initial declaration of role as string
    email: EmailStr  # Validates that the email is in the correct format

    @validator('role')
    def validate_role(cls, role: str):
        if role not in ('user', 'admin'):
            raise ValueError('Role must be either "user" or "admin"')
        return role

    class Config:
        # Allow the model to serialize ObjectId types to string
        json_encoders = {
            ObjectId: str
        }
