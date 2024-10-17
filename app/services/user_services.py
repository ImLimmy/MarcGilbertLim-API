from app.models.users import User  # Correcting the import
from app.database import db 
import bcrypt
import jwt
import os  # For loading environment variables

class UserService:
    @staticmethod
    async def register_user(user: User):
        # Hash password and save user
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')  # Convert bytes to string for storage
        result = await db.db.users.insert_one(user.dict())
        return str(result.inserted_id)

    @staticmethod
    async def authenticate_user(email: str, password: str):
        # Authenticate user logic
        user = await db.db.users.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):  # Ensure to encode for verification
            # Create JWT token
            token = jwt.encode({'sub': user['email']}, os.getenv('JWT_SECRET_KEY', 'default_secret_key'), algorithm='HS256')
            return token
        return None
