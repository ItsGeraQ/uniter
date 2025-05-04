from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import datetime, timezone
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str

class Confirm(BaseModel):
    username: str
    email_code: Optional[str] = None
    phone_code: Optional[str] = None
    mfa_code: Optional[str] = None

class User(BaseModel):
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    age: int
    phone_number: str
    is_active: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "XXXXXXX",
                "password": "XXXXXX",
                "email": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                "phone": "1234567890",
                "country_code": "+1"
            }
        }
        
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    @classmethod
    def default_updated_at(cls) -> datetime:
        return datetime.now(timezone.utc)
    