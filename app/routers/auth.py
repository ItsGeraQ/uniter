from fastapi import APIRouter

router = APIRouter()

@router.get("/login", tags=["login"])
async def login():
    return [{"msg": "login"}]

@router.get("/signup", tags=["signup"])
async def signup():
    return [{"msg": "signup"}]

@router.get("/recovering", tags=["recovering"])
async def recovering():
    return [{"msg": "recovering"}]