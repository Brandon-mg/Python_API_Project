from fastapi import UploadFile, Form
from pydantic import BaseModel, EmailStr

class BaseRequest(BaseModel):
    pass

class RefreshTokenRequest(BaseRequest):
    refresh_token: str

class AttorneyCreateRequest(BaseRequest):
    name: str
    email: EmailStr
    password: str

class ProspectCreateRequest(BaseRequest):
    fname: str = Form(...)
    lname: str = Form(...)
    email: EmailStr = Form(...)
    file: UploadFile = Form(...)
    
class LeadUpdate(BaseRequest):
    email: EmailStr
    password: str
    lead_id: str

