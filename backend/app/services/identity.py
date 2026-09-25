from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.identity import Organization, OrganizationMembership, User

def sync_identity(db: Session, claims: dict) -> tuple[User, Organization | None, OrganizationMembership | None]:
    clerk_user_id = str(claims["sub"])
    email = str(claims.get("email") or claims.get("email_address") or f"{clerk_user_id}@clerk.local")
    name = str(claims.get("name") or claims.get("first_name") or email.split("@")[0])
    user = db.scalar(select(User).where(User.clerk_user_id == clerk_user_id))
    if not user:
        user = User(clerk_user_id=clerk_user_id, email=email, full_name=name)
        db.add(user); db.flush()
    else:
        user.email, user.full_name = email, name
    org_id = claims.get("org_id")
    if not org_id: db.commit(); return user, None, None
    org_id = str(org_id)
    org = db.scalar(select(Organization).where(Organization.clerk_organization_id == org_id))
    if not org:
        org = Organization(clerk_organization_id=org_id, name=str(claims.get("org_name") or "Radian organization"), slug=org_id.lower())
        db.add(org); db.flush()
    membership = db.scalar(select(OrganizationMembership).where(OrganizationMembership.organization_id == org.id, OrganizationMembership.user_id == user.id))
    if not membership:
        membership = OrganizationMembership(organization_id=org.id, user_id=user.id, role=str(claims.get("org_role") or "member")); db.add(membership)
    db.commit(); db.refresh(user); db.refresh(org); db.refresh(membership)
    return user, org, membership
