from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, require_organization
from app.models.leads import Lead
from app.schemas.leads import *
from app.services.leads import calculate_lead_score, convert_lead
router=APIRouter(prefix="/leads",tags=["leads"])
def out(x): return LeadResponse.model_validate(x)
@router.get("",response_model=LeadListResponse)
def list_leads(q:str|None=None,status_filter:str|None=Query(None,alias="status"),source:str|None=None,owner_id:UUID|None=None,min_score:int|None=None,page:int=Query(1,ge=1),page_size:int=Query(25,ge=1,le=100),ctx=Depends(require_organization),db:Session=Depends(get_db)):
    conditions=[Lead.organization_id==ctx[1].id]
    if q: conditions.append(or_(Lead.full_name.ilike(f"%{q}%"),Lead.email.ilike(f"%{q}%"),Lead.company_name.ilike(f"%{q}%")))
    if status_filter: conditions.append(Lead.status==status_filter)
    if source: conditions.append(Lead.source==source)
    if owner_id: conditions.append(Lead.owner_id==owner_id)
    if min_score is not None: conditions.append(Lead.score>=min_score)
    stmt=select(Lead).where(*conditions); total=db.scalar(select(func.count()).select_from(stmt.subquery())) or 0; rows=db.scalars(stmt.order_by(Lead.updated_at.desc()).offset((page-1)*page_size).limit(page_size)).all(); return LeadListResponse(items=[out(x) for x in rows],total=total,page=page,page_size=page_size)
@router.post("",response_model=LeadResponse,status_code=201)
def create_lead(payload:LeadCreate,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    data=payload.model_dump(); data["full_name"]=f"{data['first_name']} {data['last_name']}"; lead=Lead(organization_id=ctx[1].id,**data); lead.score=calculate_lead_score(lead); db.add(lead); db.commit(); db.refresh(lead); return out(lead)
@router.get("/{item_id}",response_model=LeadResponse)
def get_lead(item_id:UUID,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    x=db.scalar(select(Lead).where(Lead.id==item_id,Lead.organization_id==ctx[1].id));
    if not x: raise HTTPException(404,"Lead not found")
    return out(x)
@router.patch("/{item_id}",response_model=LeadResponse)
def update_lead(item_id:UUID,payload:LeadUpdate,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    x=db.scalar(select(Lead).where(Lead.id==item_id,Lead.organization_id==ctx[1].id));
    if not x: raise HTTPException(404,"Lead not found")
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(x,k,v)
    x.full_name=f"{x.first_name} {x.last_name}"; x.score=calculate_lead_score(x); db.commit(); db.refresh(x); return out(x)
@router.delete("/{item_id}",status_code=204)
def delete_lead(item_id:UUID,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    x=db.scalar(select(Lead).where(Lead.id==item_id,Lead.organization_id==ctx[1].id));
    if not x: raise HTTPException(404,"Lead not found")
    db.delete(x); db.commit(); return Response(status_code=204)
@router.post("/{item_id}/score",response_model=LeadResponse)
def score_lead(item_id:UUID,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    x=db.scalar(select(Lead).where(Lead.id==item_id,Lead.organization_id==ctx[1].id));
    if not x: raise HTTPException(404,"Lead not found")
    x.score=calculate_lead_score(x); db.commit(); db.refresh(x); return out(x)
@router.post("/{item_id}/convert",response_model=ConvertLeadResponse)
def convert(item_id:UUID,payload:ConvertLeadRequest,ctx=Depends(require_organization),db:Session=Depends(get_db)):
    x=db.scalar(select(Lead).where(Lead.id==item_id,Lead.organization_id==ctx[1].id));
    if not x: raise HTTPException(404,"Lead not found")
    try: account,contact=convert_lead(db,x,payload.account_id,payload.create_account)
    except ValueError as e: raise HTTPException(400,str(e)) from e
    return ConvertLeadResponse(lead=out(x),account_id=account.id,contact_id=contact.id)
