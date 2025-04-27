import motor.motor_asyncio

MONGO_URI = "mongodb://mongodb:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)


def get_db():
    return client


