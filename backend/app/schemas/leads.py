from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field
class LeadCreate(BaseModel):
    first_name:str=Field(min_length=1); last_name:str=Field(min_length=1); email:EmailStr|None=None; phone:str|None=None; company_name:str|None=None; job_title:str|None=None; source:str="manual"; status:str="new"; owner_id:UUID|None=None; account_id:UUID|None=None; notes:str|None=None
class LeadUpdate(BaseModel):
    first_name:str|None=None; last_name:str|None=None; email:EmailStr|None=None; phone:str|None=None; company_name:str|None=None; job_title:str|None=None; source:str|None=None; status:str|None=None; owner_id:UUID|None=None; account_id:UUID|None=None; notes:str|None=None
class LeadResponse(LeadCreate):
    model_config=ConfigDict(from_attributes=True); id:UUID; full_name:str; score:int; organization_id:UUID; contact_id:UUID|None; created_at:datetime; updated_at:datetime
class LeadListResponse(BaseModel): items:list[LeadResponse]; total:int; page:int; page_size:int
class ConvertLeadRequest(BaseModel): account_id:UUID|None=None; create_account:bool=False
class ConvertLeadResponse(BaseModel): lead:LeadResponse; account_id:UUID; contact_id:UUID
