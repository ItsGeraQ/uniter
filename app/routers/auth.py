from fastapi import APIRouter, Depends
from app.models.user import UserLogin, User
from app.cruds.user import login_user, register_user, recover_password
from app.db.client import get_db

router = APIRouter()


@router.post("/login", tags=["login"])
async def login(user: UserLogin, db = Depends(get_db)):
    return await login_user(user, db)

@router.post("/signup", tags=["signup"]) 
async def signup(db = Depends(get_db)):
    return [{"msg": "signup"}]

@router.post("/recovering", tags=["recovering"])
async def recovering(db= Depends(get_db)):
    return [{"msg": "recovering"}]


