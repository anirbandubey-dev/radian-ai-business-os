from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.crm import Account, Contact
from app.models.leads import Lead
def calculate_lead_score(lead: Lead) -> int:
    score=0
    if lead.email: score+=25
    if lead.phone: score+=15
    if lead.company_name: score+=20
    if lead.job_title: score+=15
    if lead.source in {"referral","campaign","website"}: score+=15
    if lead.status=="qualified": score+=10
    return min(score,100)
def convert_lead(db: Session, lead: Lead, account_id=None, create_account=False):
    account=None
    if account_id: account=db.scalar(select(Account).where(Account.id==account_id,Account.organization_id==lead.organization_id))
    if not account and lead.company_name: account=db.scalar(select(Account).where(Account.organization_id==lead.organization_id,Account.name.ilike(lead.company_name)))
    if not account and (create_account or lead.company_name):
        account=Account(organization_id=lead.organization_id,name=lead.company_name or lead.full_name,account_type="company",status="active",owner_id=lead.owner_id); db.add(account); db.flush()
    if not account: raise ValueError("An existing account or company name is required")
    contact=db.scalar(select(Contact).where(Contact.organization_id==lead.organization_id,Contact.email==lead.email)) if lead.email else None
    if not contact:
        contact=Contact(organization_id=lead.organization_id,account_id=account.id,first_name=lead.first_name,last_name=lead.last_name,full_name=lead.full_name,email=lead.email,phone=lead.phone,job_title=lead.job_title,status="active",owner_id=lead.owner_id,notes=lead.notes); db.add(contact); db.flush()
    lead.account_id=account.id; lead.contact_id=contact.id; lead.status="converted"; db.commit(); db.refresh(lead)
    return account,contact
