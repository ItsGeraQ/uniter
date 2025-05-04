from app.models.user import User, UserLogin, Confirm
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
import boto3
import jwt
from datetime import timedelta
from datetime import datetime
from datetime import timezone
from settings import settings
import base64, hmac, hashlib
import logging

# Inicializar cliente de Cognito
cognito_client = boto3.client("cognito-idp", region_name=settings.COGNITO_REGION)
logger = logging.getLogger(__name__)


async def login_user(user: UserLogin, db: AsyncIOMotorClient):
    try:
        # Autenticar con Cognito
        cognito = cognito_client.initiate_auth(
            ClientId=settings.COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": user.username,
                "PASSWORD": user.password,
            },
        )
        
        # Obtener tokens
        id_token = cognito["AuthenticationResult"]["IdToken"]
        access_token = cognito["AuthenticationResult"]["AccessToken"]
        expires_in = cognito["AuthenticationResult"]["ExpiresIn"]
        
        # Verificar usuario en MongoDB o devolver error
        db_user = await db.users.find_one({"username": user.username})
        if not db_user:
             raise HTTPException(status_code=401, detail="Could not find user in database")
        
        # Crear token JWT local
        token = create_access_token(data={"sub": user.username})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "cognito_id_token": id_token,
            "cognito_access_token": access_token,
            "expires_in": expires_in
        }
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def register_user(user: User, db: AsyncIOMotorClient):
        validate_user_to_register(user, db)
        # Sign up en Cognito
        secret_hash = get_secret_hash(user.username)
        try:
            response = cognito_client.sign_up(
                ClientId=settings.COGNITO_CLIENT_ID,
                SecretHash=secret_hash,
                Username=user.username,
                Password=user.password,
                UserAttributes=[
                    {
                        "Name": "name",
                        "Value": user.first_name    
                    },
                    {
                        "Name": "middle_name",
                        "Value": user.last_name    
                    },
                    {
                        "Name": "email",
                        "Value": user.email    
                    },
                    {
                        "Name": "phone_number",
                        "Value": user.phone_number    
                    },
                ]
                
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        if not response["UserConfirmed"]: 
            raise HTTPException(status_code=500, detail="Error, user not confirmed by Auth provider")
        
        user_data = user.model_dump(exclude={"password"})
        response_db = db.users.insert_one(user_data)
        if not response_db.inserted_id:
            raise HTTPException(status_code=500, detail="Error, user not created in database")
        return response 

async def confirm_email(confirm: Confirm, db: AsyncIOMotorClient):
    secret_hash = get_secret_hash(confirm.username)
    try:
        response = cognito_client.confirm_sign_up(
            ClientId=settings.COGNITO_CLIENT_ID,
            SecretHash=secret_hash,
            Username=confirm.username,
            ConfirmationCode=confirm.email_code,
        )
        update = db.users.update_one(
            {"username": confirm.username},
            {"$set": {"is_active": True}}
        )
        
        return response
    except cognito_client.exceptions.CodeMismatchException:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    except Exception as e:
        raise HTTPException(status_code=501, detail=str(e))

async def resend_email_code(confirm: Confirm):
    try:
        secret_hash = get_secret_hash(confirm.username)
        response = cognito_client.resend_confirmation_code(
            ClientId=settings.COGNITO_CLIENT_ID,
            SecretHash=secret_hash,
            Username=confirm.username,
        )
        return response
    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=501, detail=str(e))
    
async def recover_password(user: UserLogin, db: AsyncIOMotorClient):
    pass        

def get_secret_hash(username):
        """
        Calculates a secret hash from a user name and a client secret.

        :param user_name: The user name to use when calculating the hash.
        :return: The secret hash.
        """
        key = settings.COGNITO_CLIENT_SECRET.encode()
        msg = bytes(username + settings.COGNITO_CLIENT_ID, "utf-8")
        secret_hash = base64.b64encode(
            hmac.new(key, msg, digestmod=hashlib.sha256).digest()
        ).decode()
        logger.info("Made secret hash for %s: %s.", username, secret_hash)
        return secret_hash


async def validate_user_to_register(user: User, db: AsyncIOMotorClient):
    # Find a user where either username OR email matches
    exists = await db.users.find_one({
        "$or": [
            {"username": user.username},
            {"email": user.email}
        ]
    })
    
    if exists:
        raise HTTPException(status_code=400, detail="Username or email already registered")




