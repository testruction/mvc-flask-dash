import jwt
from flask import request

def get_openid_user():
    user_id = 'n/a' 
    try:
        encoded_jwt = request.headers.get('X-Amzn-Oidc-Accesstoken')
        user_id = jwt.decode(encoded_jwt, algorithms=["RS256"], options={"verify_signature": False}).get("sub")
    finally:
        return user_id
