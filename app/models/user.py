from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    password: str
    email: str
    firs_name: str
    second_name: str
    age: int
    is_active: bool = True
    