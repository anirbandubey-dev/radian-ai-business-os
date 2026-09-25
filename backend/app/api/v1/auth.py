from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import uuid4
from app.api.dependencies import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.identity import Organization, User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=409, detail="Email is already registered")
    org = Organization(clerk_organization_id=f"legacy-org-{uuid4()}", name=payload.organization_name, slug=f"{payload.organization_name.lower().replace(' ', '-')}-{uuid4().hex[:8]}")
    user = User(clerk_user_id=f"legacy-user-{uuid4()}", email=payload.email, full_name=payload.full_name, password_hash=hash_password(payload.password))
    from app.models.identity import OrganizationMembership
    user.memberships.append(OrganizationMembership(organization=org, role="owner"))
    db.add(user); db.commit(); db.refresh(user)
    return TokenResponse(access_token=create_access_token(str(user.id)), user_id=user.id, organization_id=org.id)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash) or not user.memberships:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(str(user.id)), user_id=user.id, organization_id=user.memberships[0].organization_id)

