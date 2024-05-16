from fastapi import File, UploadFile, Form
from pydantic import BaseModel, EmailStr
from typing import Annotated

class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class AttorneyCreateRequest(BaseRequest):
    name: str
    email: EmailStr
    password: str


class ProspectCreateRequest(BaseRequest):
    
    name: str = Form(...)
    email: EmailStr = Form(...)
    file: UploadFile = Form(...)
    

class LeadUpdate(BaseRequest):
    email: EmailStr
    password: str
    lead_id: str

