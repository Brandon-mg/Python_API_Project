from pydantic import BaseModel, ConfigDict, EmailStr

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class AccessTokenResponse(BaseResponse):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int

class AttorneyResponse(BaseResponse):
    attorney_id: str
    email: EmailStr

class ProspectResponse(BaseResponse):
    prospect_id: str
    attorney_id: str
    email: EmailStr
    lead_id: str

class IDList(BaseResponse):
    ids: list[str]

class LeadInfo(BaseResponse):
    prospect_id: str
    attorney_id: str
    lead_id: str
    state: str