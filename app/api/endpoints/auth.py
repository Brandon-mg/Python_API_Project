import secrets
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import api_messages, deps
from app.core.config import get_settings
from app.core.security.jwt import create_jwt_token
from app.core.security.password import (
    DUMMY_PASSWORD,
    get_password_hash,
    verify_password,
)
from app.models import RefreshToken, Attorney, Lead
from app.schemas.requests import LeadUpdate, RefreshTokenRequest, AttorneyCreateRequest
from app.schemas.responses import AccessTokenResponse, AttorneyResponse, LeadInfo

router = APIRouter()

ACCESS_TOKEN_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {
        "description": "Invalid email or password",
        "content": {
            "application/json": {"example": {"detail": api_messages.PASSWORD_INVALID}}
        },
    },
}

REFRESH_TOKEN_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {
        "description": "Refresh token expired or is already used",
        "content": {
            "application/json": {
                "examples": {
                    "refresh token expired": {
                        "summary": api_messages.REFRESH_TOKEN_EXPIRED,
                        "value": {"detail": api_messages.REFRESH_TOKEN_EXPIRED},
                    },
                    "refresh token already used": {
                        "summary": api_messages.REFRESH_TOKEN_ALREADY_USED,
                        "value": {"detail": api_messages.REFRESH_TOKEN_ALREADY_USED},
                    },
                }
            }
        },
    },
    404: {
        "description": "Refresh token does not exist",
        "content": {
            "application/json": {
                "example": {"detail": api_messages.REFRESH_TOKEN_NOT_FOUND}
            }
        },
    },
}

# Access token endpoint that takes the email and password and generates a jwt token and attaches it to the session

@router.post(
    "/access-token",
    response_model=AccessTokenResponse,
    responses=ACCESS_TOKEN_RESPONSES,
    description="OAuth2 compatible token, get an access token for future requests using username and password",
)
async def login_access_token(
    session: AsyncSession = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> AccessTokenResponse:
    user = await session.scalar(select(Attorney).where(Attorney.email == form_data.username))

    if user is None:
        # this is naive method to not return early
        verify_password(form_data.password, DUMMY_PASSWORD)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.PASSWORD_INVALID,
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.PASSWORD_INVALID,
        )

    jwt_token = create_jwt_token(user_id=user.attorney_id)

    refresh_token = RefreshToken(
        attorney_id=user.attorney_id,
        refresh_token=secrets.token_urlsafe(32),
        exp=int(time.time() + get_settings().security.refresh_token_expire_secs),
    )
    session.add(refresh_token)
    await session.commit()

    return AccessTokenResponse(
        access_token=jwt_token.access_token,
        expires_at=jwt_token.payload.exp,
        refresh_token=refresh_token.refresh_token,
        refresh_token_expires_at=refresh_token.exp,
    )

# Refresh token endpoint as part of JWT refresh specs

@router.post(
    "/refresh-token",
    response_model=AccessTokenResponse,
    responses=REFRESH_TOKEN_RESPONSES,
    description="OAuth2 compatible token, get an access token for future requests using refresh token",
)
async def refresh_token(
    data: RefreshTokenRequest,
    session: AsyncSession = Depends(deps.get_session),
) -> AccessTokenResponse:
    token = await session.scalar(
        select(RefreshToken)
        .where(RefreshToken.refresh_token == data.refresh_token)
        .with_for_update(skip_locked=True)
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=api_messages.REFRESH_TOKEN_NOT_FOUND,
        )
    elif time.time() > token.exp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.REFRESH_TOKEN_EXPIRED,
        )
    elif token.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.REFRESH_TOKEN_ALREADY_USED,
        )

    token.used = True
    session.add(token)

    jwt_token = create_jwt_token(user_id=token.attorney_id)

    refresh_token = RefreshToken(
        attorney_id=token.attorney_id,
        refresh_token=secrets.token_urlsafe(32),
        exp=int(time.time() + get_settings().security.refresh_token_expire_secs),
    )
    session.add(refresh_token)
    await session.commit()

    return AccessTokenResponse(
        access_token=jwt_token.access_token,
        expires_at=jwt_token.payload.exp,
        refresh_token=refresh_token.refresh_token,
        refresh_token_expires_at=refresh_token.exp,
    )

# Register Attorney Endpoint creates a new record with the attorney details sent in
@router.post(
    "/register",
    response_model=AttorneyResponse,
    description="Create new Attorney",
    status_code=status.HTTP_201_CREATED,
)
async def register_new_attorney(
    new_user: AttorneyCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
) -> Attorney:
    user = await session.scalar(select(Attorney).where(Attorney.email == new_user.email))
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.EMAIL_ADDRESS_ALREADY_USED,
        )

    user = Attorney(
        name=new_user.name,
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
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

    return user

# Update Lead endpoint that takes the attorney login creds, can be swapped to session token check if the app session was made persistent.
# Checks valid login, then tries to grab the lead and update it
@router.post("/updatelead", response_model=LeadInfo, description="Update Lead")
async def read_current_user(update_form: LeadUpdate, session: AsyncSession = Depends(deps.get_session)) -> None:
    user = await session.scalar(select(Attorney).where(Attorney.email == update_form.email))
    if user is None:
        # this is naive method to not return early
        verify_password(update_form.password, DUMMY_PASSWORD)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.PASSWORD_INVALID,
        )

    if not verify_password(update_form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.NO_VALID_ATTORNEY_FOUND,
        )    
    
    lead = await session.scalar(select(Lead).where(Lead.lead_id == update_form.lead_id))
    if lead is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=api_messages.ERROR_CREATING_LEAD,
        )
    lead.state = "REACHED_OUT"
    session.add(lead)
    await session.commit()
    return lead