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

@router.post(
    "/filelead",
    response_model=ProspectResponse,
    description="File a new lead",
    status_code=status.HTTP_201_CREATED,
)
async def register_new_prospect(
    file: Annotated[UploadFile, File()],
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    session: AsyncSession = Depends(deps.get_session),
) -> ProspectResponse:
    user = await session.scalar(select(Prospect).where(Prospect.email == email))
    if user is None:
        file_path = getcwd()+"/app/resume/"+file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            f.close
        user = Prospect(
            email=email,
            name=name,
            resume=file_path
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
    #attorney_id = await session.scalar(select(Attorney))
    id_tuple = await session.scalar(select(Prospect).where(Prospect.email == email)), await session.scalar(select(Attorney).order_by(func.random()).limit(1))

    lead = Lead(
        prospect_id = id_tuple[0].prospect_id,
        attorney_id = id_tuple[1].attorney_id,
        state = "PENDING"
    )
    
    session.add(lead)
    try:
        await session.commit()
    except IntegrityError:  # pragma: no cover
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.EMAIL_ADDRESS_ALREADY_USED,
        )
    ret = ProspectResponse(
        prospect_id = id_tuple[0],
        attorney_id = id_tuple[1],
        lead_id = lead.lead_id,
        email = user.email
    )

    if Settings.enable_email:
        await send_email_async("New Lead Pair", id_tuple[1].email, id_tuple[0].email, {'title': f"{user.name} has a new lead attached to {id_tuple[1].name}, id:{lead.lead_id}", 'data': f"status for lead {lead.lead_id} is {lead.state}."})

    return ret





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