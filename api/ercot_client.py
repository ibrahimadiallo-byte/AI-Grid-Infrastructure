"""ERCOT API client.

API reference: https://developer.ercot.com/
Authentication: OAuth2 client-credentials flow.
"""

import httpx
from api.config import settings


class ERCOTClient:
    """Thin async wrapper around the ERCOT public-reports API."""

    def __init__(self) -> None:
        self._access_token: str | None = None
        self._client = httpx.AsyncClient(base_url=settings.ercot_base_url, timeout=30)

    async def _get_token(self) -> str:
        """Fetch/refresh OAuth2 bearer token."""
        if not settings.ercot_username or not settings.ercot_password:
            raise ValueError("ERCOT_USERNAME and ERCOT_PASSWORD must be set in .env")
        if not settings.ercot_client_id:
            raise ValueError("ERCOT_CLIENT_ID must be set in .env")
        resp = await self._client.post(
            settings.ercot_token_url,
            data={
                "grant_type": "password",
                "client_id": settings.ercot_client_id,
                "username": settings.ercot_username,
                "password": settings.ercot_password,
                "scope": f"openid {settings.ercot_client_id} offline_access",
            },
        )
        resp.raise_for_status()
        self._access_token = resp.json()["access_token"]
        return self._access_token

    @property
    def _auth_headers(self) -> dict:
        headers = {"Authorization": f"Bearer {self._access_token}"}
        if settings.ercot_subscription_key:
            headers["Ocp-Apim-Subscription-Key"] = settings.ercot_subscription_key
        return headers

    async def _get(self, path: str) -> dict:
        """GET helper with token refresh on 401."""
        if not self._access_token:
            await self._get_token()
        resp = await self._client.get(path, headers=self._auth_headers)
        if resp.status_code == 401:
            await self._get_token()
            resp = await self._client.get(path, headers=self._auth_headers)
        resp.raise_for_status()
        return resp.json()

    async def get_real_time_prices(self) -> dict:
        """Fetch Real-Time Settlement Point Prices (SPPs)."""
        return await self._get("/np6-905-cd/spp_node_zone_hub")

    async def get_load_forecast(self) -> dict:
        """Fetch ERCOT system load forecast."""
        return await self._get("/np3-566-cd/lf_by_model_study_area")

    async def get_system_frequency(self) -> dict:
        """Fetch ERCOT system frequency payload from a configured endpoint."""
        if not settings.ercot_frequency_endpoint:
            raise ValueError(
                "ERCOT_FREQUENCY_ENDPOINT must be set in .env "
                "(e.g., a public-reports path that returns system frequency)."
            )
        return await self._get(settings.ercot_frequency_endpoint)

    async def close(self) -> None:
        await self._client.aclose()
