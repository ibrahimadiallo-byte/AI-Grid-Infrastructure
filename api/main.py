"""FastAPI main application.

Run with:
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.ercot_client import ERCOTClient
from api.isone_client import ISONeClient

ercot = ERCOTClient()
isone = ISONeClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await ercot.close()
    await isone.close()


app = FastAPI(
    title="Energy Grid Dashboard API",
    description="Real-time data from ERCOT (Texas) and ISO-NE (New England) grid operators.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ─── Health ──────────────────────────────────────────────────────────────────

@app.get("/health", tags=["meta"])
async def health_check():
    return {"status": "ok", "env": settings.app_env}


# ─── ERCOT ───────────────────────────────────────────────────────────────────

@app.get("/ercot/prices", tags=["ERCOT"])
async def ercot_prices():
    """Real-time settlement-point prices from ERCOT."""
    try:
        return await ercot.get_real_time_prices()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.get("/ercot/load-forecast", tags=["ERCOT"])
async def ercot_load_forecast():
    """ERCOT system load forecast."""
    try:
        return await ercot.get_load_forecast()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


# ─── ISO-NE ──────────────────────────────────────────────────────────────────

@app.get("/isone/lmp/realtime", tags=["ISO-NE"])
async def isone_realtime_lmp():
    """ISO-NE real-time locational marginal prices."""
    try:
        return await isone.get_real_time_lmp()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.get("/isone/lmp/dayahead", tags=["ISO-NE"])
async def isone_dayahead_lmp():
    """ISO-NE day-ahead locational marginal prices."""
    try:
        return await isone.get_day_ahead_lmp()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.get("/isone/demand", tags=["ISO-NE"])
async def isone_demand():
    """ISO-NE current hourly system demand."""
    try:
        return await isone.get_hourly_demand()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
