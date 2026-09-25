from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, require_identity
from app.schemas.me import MeOrganization, MeResponse, MeUser
from app.services.identity import sync_identity

router = APIRouter(prefix="/auth", tags=["auth"])
@router.get("/me", response_model=MeResponse)
def me(claims: dict = Depends(require_identity), db: Session = Depends(get_db)) -> MeResponse:
    user, org, membership = sync_identity(db, claims)
    if not org or not membership:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No active organization")
    return MeResponse(user=MeUser(id=user.id, clerk_user_id=user.clerk_user_id, email=user.email, name=user.full_name), organization=MeOrganization(id=org.id, clerk_organization_id=org.clerk_organization_id, name=org.name), role=membership.role)
