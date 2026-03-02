"""ERCOT API client.

API reference: https://developer.ercot.com/
Authentication: OAuth2 client-credentials flow.
"""

import httpx
from api.config import settings


class ERCOTClient:
    """Thin async wrapper around the ERCOT public-reports API."""

    TOKEN_URL = "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v1.0/token"

    def __init__(self) -> None:
        self._access_token: str | None = None
        self._client = httpx.AsyncClient(base_url=settings.ercot_base_url, timeout=30)

    async def _get_token(self) -> str:
        """Fetch/refresh OAuth2 bearer token."""
        resp = await self._client.post(
            self.TOKEN_URL,
            data={
                "grant_type": "password",
                "client_id": settings.ercot_client_id,
                "client_secret": settings.ercot_client_secret,
                "scope": f"openid {settings.ercot_client_id} offline_access",
                # ERCOT ROPC flow also needs username/password but we use client-creds here
            },
        )
        resp.raise_for_status()
        self._access_token = resp.json()["access_token"]
        return self._access_token

    @property
    def _auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self._access_token}"}

    async def get_real_time_prices(self) -> dict:
        """Fetch Real-Time Settlement Point Prices (SPPs)."""
        if not self._access_token:
            await self._get_token()
        resp = await self._client.get(
            "/np6-905-cd/spp_node_zone_hub",
            headers=self._auth_headers,
        )
        resp.raise_for_status()
        return resp.json()

    async def get_load_forecast(self) -> dict:
        """Fetch ERCOT system load forecast."""
        if not self._access_token:
            await self._get_token()
        resp = await self._client.get(
            "/np3-566-cd/lf_by_model_study_area",
            headers=self._auth_headers,
        )
        resp.raise_for_status()
        return resp.json()

    async def close(self) -> None:
        await self._client.aclose()
