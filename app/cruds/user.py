from app.models.user import User, UserLogin
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
import boto3
import jwt
from datetime import timedelta
from datetime import datetime
from datetime import timezone

# Configuración de AWS Cognito
COGNITO_REGION = "us-east-1"  # Cambia según tu región
COGNITO_USERPOOL_ID = "us-east-1_xQnXpZkzw"  # Reemplaza con tu User Pool ID
COGNITO_CLIENT_ID = "26qit1a4gue0blmponc2va1n5o"  # Reemplaza con tu Client ID
COGNITO_CLIENT_SECRET = "1mpf8jevq5ua06r93sg1os6oiohldaksb9spceigj5a6krk7u8uq"  # Reemplaza con tu Client Secret (si aplica)

# Inicializar cliente de Cognito
cognito_client = boto3.client("cognito-idp", region_name=COGNITO_REGION)

# Configuración JWT
SECRET_KEY = "your-secret-key"  # Cambia por una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



async def login_user(user: UserLogin, db: AsyncIOMotorClient):
    try:
        # Autenticar con Cognito
        response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": user.username,
                "PASSWORD": user.password,
            },
        )
        
        # Obtener tokens
        id_token = response["AuthenticationResult"]["IdToken"]
        access_token = response["AuthenticationResult"]["AccessToken"]
        
        # Verificar usuario en MongoDB o crearlo
        db_user = await db.users.find_one({"username": user.username})
        if not db_user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Crear token JWT local
        token = create_access_token(data={"sub": user.username})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "cognito_id_token": id_token,
            "cognito_access_token": access_token
        }
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_user(user: User, db: AsyncIOMotorClient):
    pass

async def recover_password(user: UserLogin, db: AsyncIOMotorClient):
    pass



