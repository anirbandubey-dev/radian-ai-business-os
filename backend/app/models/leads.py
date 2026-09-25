from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class Lead(Base):
    __tablename__="leads"
    id: Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    organization_id: Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
    first_name: Mapped[str]=mapped_column(String(100)); last_name: Mapped[str]=mapped_column(String(100)); full_name: Mapped[str]=mapped_column(String(205),index=True)
    email: Mapped[str|None]=mapped_column(String(320),index=True); phone: Mapped[str|None]=mapped_column(String(40)); company_name: Mapped[str|None]=mapped_column(String(200),index=True); job_title: Mapped[str|None]=mapped_column(String(120)); source: Mapped[str]=mapped_column(String(60),default="manual",index=True); status: Mapped[str]=mapped_column(String(40),default="new",index=True); score: Mapped[int]=mapped_column(Integer,default=0,index=True)
    owner_id: Mapped[UUID|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"),index=True); account_id: Mapped[UUID|None]=mapped_column(ForeignKey("accounts.id",ondelete="SET NULL"),index=True); contact_id: Mapped[UUID|None]=mapped_column(ForeignKey("contacts.id",ondelete="SET NULL"),index=True); notes: Mapped[str|None]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); updated_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    __table_args__=(Index("ix_leads_org_status","organization_id","status"),)
