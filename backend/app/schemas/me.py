from uuid import UUID
from pydantic import BaseModel
class MeUser(BaseModel): id: UUID; clerk_user_id: str; email: str; name: str
class MeOrganization(BaseModel): id: UUID; clerk_organization_id: str; name: str
class MeResponse(BaseModel): user: MeUser; organization: MeOrganization; role: str
