from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload
from app.api.dependencies import get_db, require_organization
from app.models.crm import Account, Contact
from app.schemas.crm import *

router = APIRouter(tags=["crm"])
def context(dep=Depends(require_organization)): return dep
def account_out(a: Account) -> AccountResponse: return AccountResponse.model_validate({**a.__dict__, "contact_count": len(a.contacts)})
def contact_out(c: Contact) -> ContactResponse: return ContactResponse.model_validate({**c.__dict__, "account_name": c.account.name if c.account else None})

@router.get("/accounts", response_model=AccountListResponse)
def list_accounts(q: str | None = None, industry: str | None = None, status_filter: str | None = Query(None, alias="status"), country: str | None = None, page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100), ctx=Depends(require_organization), db: Session=Depends(get_db)):
    org=ctx[1]; stmt=select(Account).where(Account.organization_id==org.id).options(joinedload(Account.contacts)); count=select(func.count()).select_from(Account).where(Account.organization_id==org.id)
    for condition in ([Account.name.ilike(f"%{q}%")] if q else []) + ([Account.industry==industry] if industry else []) + ([Account.status==status_filter] if status_filter else []) + ([Account.country==country] if country else []): stmt=stmt.where(condition); count=count.where(condition)
    total=db.scalar(count) or 0; items=db.scalars(stmt.order_by(Account.updated_at.desc()).offset((page-1)*page_size).limit(page_size)).unique().all(); return AccountListResponse(items=[account_out(a) for a in items],total=total,page=page,page_size=page_size)
@router.post("/accounts", response_model=AccountResponse, status_code=201)
def create_account(payload: AccountCreate, ctx=Depends(require_organization), db: Session=Depends(get_db)):
    a=Account(organization_id=ctx[1].id, **payload.model_dump()); db.add(a); db.commit(); db.refresh(a); return account_out(a)
@router.get("/accounts/{item_id}", response_model=AccountResponse)
def get_account(item_id: UUID, ctx=Depends(require_organization), db: Session=Depends(get_db)):
    a=db.scalar(select(Account).where(Account.id==item_id, Account.organization_id==ctx[1].id).options(joinedload(Account.contacts))); 
    if not a: raise HTTPException(404,"Account not found")
    return account_out(a)
@router.patch("/accounts/{item_id}", response_model=AccountResponse)
def update_account(item_id: UUID, payload: AccountUpdate, ctx=Depends(require_organization), db: Session=Depends(get_db)):
    a=db.scalar(select(Account).where(Account.id==item_id, Account.organization_id==ctx[1].id).options(joinedload(Account.contacts))); 
    if not a: raise HTTPException(404,"Account not found")
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(a,k,v)
    db.commit(); db.refresh(a); return account_out(a)
@router.delete("/accounts/{item_id}", status_code=204)
def delete_account(item_id: UUID, ctx=Depends(require_organization), db: Session=Depends(get_db)):
    a=db.scalar(select(Account).where(Account.id==item_id, Account.organization_id==ctx[1].id));
    if not a: raise HTTPException(404,"Account not found")
    db.delete(a); db.commit(); return Response(status_code=204)
@router.get("/accounts/{item_id}/contacts", response_model=ContactListResponse)
def account_contacts(item_id: UUID, ctx=Depends(require_organization), db: Session=Depends(get_db)):
    if not db.scalar(select(Account.id).where(Account.id==item_id, Account.organization_id==ctx[1].id)): raise HTTPException(404,"Account not found")
    items=db.scalars(select(Contact).where(Contact.account_id==item_id, Contact.organization_id==ctx[1].id).options(joinedload(Contact.account))).all(); return ContactListResponse(items=[contact_out(c) for c in items],total=len(items),page=1,page_size=len(items) or 1)

@router.get("/contacts", response_model=ContactListResponse)
def list_contacts(q: str | None=None, status_filter: str | None=Query(None,alias="status"), page:int=Query(1,ge=1), page_size:int=Query(25,ge=1,le=100), ctx=Depends(require_organization), db:Session=Depends(get_db)):
    org=ctx[1]; stmt=select(Contact).where(Contact.organization_id==org.id).options(joinedload(Contact.account)); conditions=[]
    if q: conditions.append(or_(Contact.full_name.ilike(f"%{q}%"),Contact.email.ilike(f"%{q}%"),Contact.job_title.ilike(f"%{q}%"))); stmt=stmt.where(conditions[-1])
    if status_filter: stmt=stmt.where(Contact.status==status_filter)
    total=db.scalar(select(func.count()).select_from(stmt.subquery())) or 0; items=db.scalars(stmt.order_by(Contact.updated_at.desc()).offset((page-1)*page_size).limit(page_size)).all(); return ContactListResponse(items=[contact_out(c) for c in items],total=total,page=page,page_size=page_size)
@router.post("/contacts", response_model=ContactResponse, status_code=201)
def create_contact(payload: ContactCreate, ctx=Depends(require_organization), db:Session=Depends(get_db)):
    data=payload.model_dump(); data["full_name"]=f"{data['first_name']} {data['last_name']}"; c=Contact(organization_id=ctx[1].id,**data); db.add(c); db.commit(); db.refresh(c); return contact_out(c)
@router.get("/contacts/{item_id}", response_model=ContactResponse)
def get_contact(item_id:UUID,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    c=db.scalar(select(Contact).where(Contact.id==item_id,Contact.organization_id==ctx[1].id).options(joinedload(Contact.account))); 
    if not c: raise HTTPException(404,"Contact not found")
    return contact_out(c)
@router.patch("/contacts/{item_id}", response_model=ContactResponse)
def update_contact(item_id:UUID,payload:ContactUpdate,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    c=db.scalar(select(Contact).where(Contact.id==item_id,Contact.organization_id==ctx[1].id).options(joinedload(Contact.account))); 
    if not c: raise HTTPException(404,"Contact not found")
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(c,k,v)
    if payload.first_name is not None or payload.last_name is not None: c.full_name=f"{c.first_name} {c.last_name}"
    db.commit(); db.refresh(c); return contact_out(c)
@router.delete("/contacts/{item_id}",status_code=204)
def delete_contact(item_id:UUID,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    c=db.scalar(select(Contact).where(Contact.id==item_id,Contact.organization_id==ctx[1].id));
    if not c: raise HTTPException(404,"Contact not found")
    db.delete(c); db.commit(); return Response(status_code=204)
