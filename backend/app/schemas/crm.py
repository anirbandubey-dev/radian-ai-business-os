from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class AccountBase(BaseModel):
    name: str = Field(min_length=1, max_length=200); account_type: str = "company"; industry: str | None = None; website: str | None = None; phone: str | None = None; email: EmailStr | None = None; address: str | None = None; city: str | None = None; state: str | None = None; country: str | None = None; postal_code: str | None = None; description: str | None = None; owner_id: UUID | None = None; status: str = "active"
class AccountCreate(AccountBase): pass
class AccountUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200); account_type: str | None = None; industry: str | None = None; website: str | None = None; phone: str | None = None; email: EmailStr | None = None; address: str | None = None; city: str | None = None; state: str | None = None; country: str | None = None; postal_code: str | None = None; description: str | None = None; owner_id: UUID | None = None; status: str | None = None
class AccountResponse(AccountBase):
    model_config = ConfigDict(from_attributes=True); id: UUID; organization_id: UUID; created_at: datetime; updated_at: datetime; contact_count: int = 0
class AccountListResponse(BaseModel): items: list[AccountResponse]; total: int; page: int; page_size: int
class ContactBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100); last_name: str = Field(min_length=1, max_length=100); email: EmailStr | None = None; phone: str | None = None; account_id: UUID | None = None; job_title: str | None = None; department: str | None = None; status: str = "active"; owner_id: UUID | None = None; notes: str | None = None
class ContactCreate(ContactBase): pass
class ContactUpdate(BaseModel):
    first_name: str | None = None; last_name: str | None = None; email: EmailStr | None = None; phone: str | None = None; account_id: UUID | None = None; job_title: str | None = None; department: str | None = None; status: str | None = None; owner_id: UUID | None = None; notes: str | None = None
class ContactResponse(ContactBase):
    model_config = ConfigDict(from_attributes=True); id: UUID; organization_id: UUID; full_name: str; created_at: datetime; updated_at: datetime; account_name: str | None = None
class ContactListResponse(BaseModel): items: list[ContactResponse]; total: int; page: int; page_size: int
