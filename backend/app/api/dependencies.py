from collections.abc import Generator
from typing import Callable
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import clerk_claims, decode_subject
from app.db.session import SessionLocal
from app.models.identity import Organization, OrganizationMembership, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try: yield db
    finally: db.close()
def require_identity(token: str = Depends(oauth2_scheme)) -> dict:
    claims = clerk_claims(token)
    if claims: return claims
    subject = decode_subject(token)
    if subject: return {"sub": subject}
    raise HTTPException(status_code=401, detail="Invalid or expired token")
def require_user(identity: dict = Depends(require_identity), db: Session = Depends(get_db)) -> User:
    user = db.scalar(select(User).where(User.clerk_user_id == identity["sub"]))
    if not user: raise HTTPException(status_code=401, detail="User is not synchronized")
    return user
def require_organization(identity: dict = Depends(require_identity), user: User = Depends(require_user), db: Session = Depends(get_db)) -> tuple[User, Organization, OrganizationMembership]:
    clerk_org_id = identity.get("org_id")
    if not clerk_org_id: raise HTTPException(status_code=400, detail="No active organization")
    membership = db.scalar(select(OrganizationMembership).join(Organization).where(Organization.clerk_organization_id == clerk_org_id, OrganizationMembership.user_id == user.id))
    if not membership: raise HTTPException(status_code=403, detail="User is not a member of this organization")
    return user, membership.organization, membership
def require_role(*roles: str) -> Callable:
    def dependency(context: tuple = Depends(require_organization)) -> tuple:
        if context[2].role not in roles: raise HTTPException(status_code=403, detail="Insufficient organization role")
        return context
    return dependency
