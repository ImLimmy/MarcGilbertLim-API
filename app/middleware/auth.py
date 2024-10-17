from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from typing import Dict, Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Optional[str]]:
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, 'S_KEY', algorithms=['HS256'])  # Ensure 'S_KEY' is securely stored
        user_email = payload.get("sub")
        user_role = payload.get("role")  # Assuming 'role' is part of the JWT payload

        # Check if user role exists
        if user_role not in ["user", "admin"]:
            raise HTTPException(status_code=403, detail="Invalid role")

        # Return user information along with role
        return {"email": user_email, "role": user_role}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
