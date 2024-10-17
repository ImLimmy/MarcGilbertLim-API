from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.user_services import UserService
from app.models.users import User
from app.database import db
import jwt
import os
from bson import ObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY', 'default_secret_key'), algorithms=["HS256"])
        user_email = payload.get("sub")

        # Fetch the user from the database using the email
        user = await db.db.users.find_one({"email": user_email})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user  # Return the user object
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post('/register')
async def register(user: User):
    user_id = await UserService.register_user(user)
    return {'user_id': user_id}

@router.post('/login')
async def login(email: str = Form(...), password: str = Form(...)):
    token = await UserService.authenticate_user(email, password)
    if token:
        return {'token': token}
    raise HTTPException(status_code=401, detail='Invalid Credentials')

@router.get('/users')
async def list_users(current_user: User = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="You do not have access to this resource.")

    users = await db.db.users.find().to_list(100)  # Fetch all users
    return [{"user_id": str(user['_id']), "username": user['username'], "role": user['role']} for user in users]

@router.get('/users/{user_id}')
async def get_user_profile(user_id: str, current_user: User = Depends(get_current_user)):
    user = await db.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Access control: Admin can view any profile; regular user can view only their own
    if current_user['role'] == 'user' and str(user['_id']) != str(current_user['_id']):
        raise HTTPException(status_code=403, detail="You do not have access to this resource.")

    return {"user_id": str(user['_id']), "username": user['username'], "role": user['role']}

@router.put('/users/{user_id}')
async def update_user_profile(user_id: str, user_data: User, current_user: User = Depends(get_current_user)):
    user = await db.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Access control: Admin can update any profile; regular user can update only their own
    if current_user['role'] == 'user' and str(user['_id']) != str(current_user['_id']):
        raise HTTPException(status_code=403, detail="You do not have access to this resource.")

    updated_user = {**user, **user_data.dict(exclude_unset=True)}  # Merge existing and new data
    await db.db.users.replace_one({"_id": ObjectId(user_id)}, updated_user)

    return {"message": "User profile updated successfully", "user_id": user_id}

@router.delete('/users/{user_id}')
async def delete_user_profile(user_id: str, current_user: User = Depends(get_current_user)):
    user = await db.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Access control: Admin can delete any profile; regular user can delete only their own
    if current_user['role'] == 'user' and str(user['_id']) != str(current_user['_id']):
        raise HTTPException(status_code=403, detail="You do not have access to this resource.")

    await db.db.users.delete_one({"_id": ObjectId(user_id)})

    return {"message": "User profile deleted successfully"}
