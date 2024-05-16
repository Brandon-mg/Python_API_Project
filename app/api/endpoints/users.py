from sqlite3 import IntegrityError
from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from os import getcwd
from app.api import api_messages, deps
from app.models import Lead, Prospect, Attorney
from app.schemas.responses import IDList, ProspectResponse
from app.core.send_mail import send_email_async
from app.core.config import Settings

router = APIRouter()

# File Lead API Endpoint. Takes multipart form for File, lname, fname, email
# Creates a prospect record and a lead record
# Saves the file uploaded in the app/resumes folder
# Gets random attorney in attorney table to assign to lead
# Then runs the Email func with data

@router.post(
    "/filelead",
    response_model=ProspectResponse,
    description="File a new lead",
    status_code=status.HTTP_201_CREATED,
)
async def register_new_prospect(
    file: Annotated[UploadFile, File()],
    fname: Annotated[str, Form()],
    lname: Annotated[str, Form()],
    email: Annotated[str, Form()],
    session: AsyncSession = Depends(deps.get_session),
) -> ProspectResponse:
    name=f"{fname} {lname}"
    user = await session.scalar(select(Prospect).where(Prospect.email == email))
    if user is None:
        file_path = getcwd()+"\\app\\resume\\"+fname+"_"+lname+"_"+file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            f.close
        user = Prospect(
            email=email,
            name=name,
            resume=fname+"_"+lname+"_"+file.filename
        )
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:  # pragma: no cover
            await session.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=api_messages.EMAIL_ADDRESS_ALREADY_USED,
            )
    else:
        with open(getcwd()+"\\app\\resume\\"+user.resume, "wb") as f:
            f.write(file.file.read())
            f.close
    
    prospect, attorney = await session.scalar(select(Prospect).where(Prospect.email == email)), await session.scalar(select(Attorney).order_by(func.random()).limit(1))
    if attorney is None:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=api_messages.NO_VALID_ATTORNEY_FOUND,
            )
    lead = Lead(
        prospect_id = prospect.prospect_id,
        attorney_id = attorney.attorney_id,
        state = "PENDING"
    )
    
    session.add(lead)
    try:
        await session.commit()
    except IntegrityError:  # pragma: no cover
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.ERROR_CREATING_LEAD,
        )
    ret = ProspectResponse(
        prospect_id = lead.prospect_id,
        attorney_id = lead.attorney_id,
        lead_id = lead.lead_id,
        email = user.email
    )

    await send_email_async("New Lead Pair", attorney.email, prospect.email, {'title': f"{user.name} has a new lead attached to {attorney.name}, id:{lead.lead_id}", 'data': f"status for lead {lead.lead_id} is {lead.state}."})

    return ret

# The following endpoints are getter functions that will return the list of the ids for the specified type
# /getpendingleads returns list of lead ids where lead.state == "PENDING"
# /getreachedleads returns list of lead ids where lead.state == "REACHED_OUT"
# /getattorneys returns list of attorney ids
# /getprospects returns list of prospect ids
# can be expanded to take auth access and return more info 

@router.post("/getpendingleads", response_model=IDList, description="Get pending leads")
async def read_current_user(session: AsyncSession = Depends(deps.get_session)) -> None:
    q = select(Lead).where(Lead.state == "PENDING")
    leads_list = await session.execute(q)
    ret = IDList(
        ids=[]
    )
    for lead in leads_list.scalars().all():
        ret.ids.append(lead.lead_id)
    return ret

@router.post("/getreachedleads", response_model=IDList, description="Get reached out leads")
async def read_current_user(session: AsyncSession = Depends(deps.get_session)) -> None:
    q = select(Lead).where(Lead.state == "REACHED_OUT")
    leads_list = await session.execute(q)
    ret = IDList(
        ids=[]
    )
    for lead in leads_list.scalars().all():
        ret.ids.append(lead.lead_id)
    return ret

@router.post("/getattorneys", response_model=IDList, description="Get attorneys")
async def read_current_user(session: AsyncSession = Depends(deps.get_session)) -> None:
    q = select(Attorney)
    attorneys_list = await session.execute(q)
    ret = IDList(
        ids=[]
    )
    for attorney in attorneys_list.scalars().all():
        ret.ids.append(attorney.attorney_id)
    return ret

@router.post("/getprospects", response_model=IDList, description="Get prospects")
async def read_current_user(session: AsyncSession = Depends(deps.get_session)) -> None:
    q = select(Prospect)
    prospects_list = await session.execute(q)
    ret = IDList(
        ids=[]
    )
    for prospect in prospects_list.scalars().all():
        ret.ids.append(prospect.prospect_id)
    return ret