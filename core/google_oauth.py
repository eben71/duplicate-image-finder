import httpx
from datetime import datetime, timezone
from sqlmodel import Session
from urllib.parse import urlencode
from backend.config.settings import settings
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
        "prompt": "consent",
        "state": state,
    }

    return f"{GOOGLE_AUTH_BASE}?{urlencode(params)}"


async def exchange_code_for_token(code: str) -> dict:
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()


def is_token_expired(user: User) -> bool:
    if not user.token_expiry:
        return True

    return user.token_expiry <= datetime.now(timezone.utc)


async def get_fresh_access_token(user: User, session: Session) -> str:
    if is_token_expired(user):
        await refresh_access_token(user, session)

    token = user.get_google_access_token()
    if not token:
        raise ValueError("Missing access token. User may require re-authentication.")

    return token


async def refresh_access_token(user: User, session: Session) -> None:
    try:
        refresh_token = user.get_google_refresh_token()
        if not refresh_token:
            raise ValueError(
                "User does not have a refresh token. They must re-authenticate."
            )

        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GOOGLE_TOKEN_URL, data=data)
            response.raise_for_status()

        token_data = await response.json()

        user.set_google_tokens(
            access_token=token_data["access_token"],
            refresh_token=None,
            expires_in=token_data["expires_in"],
        )
        session.add(user)
        session.commit()

    except (httpx.HTTPStatusError, ValueError) as e:
        user.requires_reauth = True
        session.add(user)
        session.commit()
        raise Exception(
            "Google token refresh failed. User must re-authenticate."
        ) from e
