from pydantic import BaseModel


class UserLogin(BaseModel):
	username: str
	password: str
 
class User(BaseModel):
	username: str
	password: str
	email: str
	age: int
