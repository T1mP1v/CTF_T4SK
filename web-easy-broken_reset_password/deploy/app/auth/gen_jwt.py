import time, os
from typing import Dict

import jwt

JWT_SECRET = os.getenv("JWT_SECRET")  
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def token_response(token: str):
    return {
        "access_token": token
    }

def sign_jwt(user_id, name: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000,
        "username": name
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}