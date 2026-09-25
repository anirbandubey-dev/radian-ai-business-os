from datetime import datetime, timedelta, timezone
from typing import Any
import httpx
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def hash_password(password: str) -> str: return pwd_context.hash(password)
def verify_password(password: str, hashed: str) -> bool: return pwd_context.verify(password, hashed)
def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    return jwt.encode({"sub": subject, "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)}, settings.jwt_secret, algorithm="HS256")
def decode_subject(token: str) -> str | None:
    try: return str(jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])["sub"])
    except (JWTError, KeyError): return None
def clerk_claims(token: str) -> dict[str, Any] | None:
    if not settings.clerk_jwks_url: return None
    try:
        jwks = httpx.get(settings.clerk_jwks_url, timeout=5).json()
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])
        return jwt.decode(token, key, algorithms=["RS256"], issuer=settings.clerk_jwt_issuer or None, options={"verify_aud": False})
    except (httpx.HTTPError, KeyError, StopIteration, JWTError): return None
