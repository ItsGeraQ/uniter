from fastapi import APIRouter, Depends
from app.models.user import UserLogin, User, Confirm
from app.cruds.user import login_user, register_user, confirm_email, resend_email_code
from app.db.client import get_db

router = APIRouter()


@router.post("/login", tags=["login"])
async def login(user: UserLogin, db = Depends(get_db)):
    return await login_user(user, db)

@router.post("/signup", tags=["signup"]) 
async def signup(user: User, db = Depends(get_db)):
    return await register_user(user, db)

@router.post("/confirm-signup", tags=["confirm-signup"])
async def confirm_signup(confirm: Confirm, db = Depends(get_db)):
    return await confirm_email(confirm, db)

@router.post("/resend-code", tags=["resend-code"])
async def resend_code_confirmation(confirm: Confirm):
    return await resend_email_code(confirm)

@router.post("/recovering", tags=["recovering"])
async def recovering(db= Depends(get_db)):
    return [{"msg": "recovering"}]


