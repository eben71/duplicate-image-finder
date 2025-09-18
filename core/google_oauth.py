from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Any
from urllib.parse import urlencode

import httpx
from fastapi import Depends
from sqlmodel import Session

from backend.config.settings import settings
from backend.deps import get_http_client
from backend.models.user import User

GOOGLE_AUTH_BASE = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_SCOPE = "https://www.googleapis.com/auth/photoslibrary.readonly"


def get_google_auth_url(state: str = "") -> str:
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": GOOGLE_SCOPE,
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "consent",
    }

    if state:
        params["state"] = state

    return f"{GOOGLE_AUTH_BASE}?{urlencode(params)}"


async def exchange_code_for_token(
    code: str, client: Annotated[httpx.AsyncClient, Depends(get_http_client)]
) -> dict:
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = await client.post(GOOGLE_TOKEN_URL, data=data)
    response.raise_for_status()
    return response.json()


def is_token_expired(user: User) -> bool:
    if not user.token_expiry:
        return True

    return user.token_expiry <= datetime.now(UTC)


async def get_fresh_access_token(
    user: User, session: Session, client: Annotated[httpx.AsyncClient, Depends(get_http_client)]
) -> str:
    if is_token_expired(user):
        await refresh_access_token(user, session, client)

    token: str | None = user.get_google_access_token()

    if token is None:
        raise ValueError(
            "Token refresh did not yield an access_token. User may require re-authentication."
        )

    if not token:
        raise ValueError("Access token is empty. User may require re-authentication.")

    return token


async def refresh_access_token(
    user: User, session: Session, client: Annotated[httpx.AsyncClient, Depends(get_http_client)]
) -> None:
    try:
        refresh_token = user.get_google_refresh_token()
        if not refresh_token:
            user.requires_reauth = True
            session.add(user)
            session.commit()
            raise ValueError("User does not have a refresh token. They must re-authenticate.")

        data: dict[str, Any] = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        response = await client.post(GOOGLE_TOKEN_URL, data=data)
        response.raise_for_status()

        token_data = response.json()
        # Google may omit refresh_token on refresh; keep the old one unless a new one is provided
        new_refresh: str | None = token_data.get("refresh_token") or user.get_google_refresh_token()
        expires_in = int(token_data.get("expires_in", 3600))

        user.set_google_tokens(
            access_token=token_data["access_token"],
            refresh_token=new_refresh,
            expires_in=expires_in,
        )
        user.requires_reauth = False
        session.add(user)
        session.commit()

    except (httpx.HTTPStatusError, ValueError) as e:
        user.requires_reauth = True
        session.add(user)
        session.commit()
        raise Exception("Google token refresh failed. User must re-authenticate.") from e
