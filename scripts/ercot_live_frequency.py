import asyncio
import json
from datetime import datetime, timezone

from api.ercot_client import ERCOTClient


def _extract_frequency(payload: dict) -> tuple[float | None, dict | None]:
    if not isinstance(payload, dict):
        return None, None

    records = payload.get("data") or payload.get("items") or payload.get("results")
    if isinstance(records, list) and records:
        for record in records:
            if not isinstance(record, dict):
                continue
            for key, value in record.items():
                if "frequency" in key.lower():
                    try:
                        return float(value), record
                    except (TypeError, ValueError):
                        continue

    for key, value in payload.items():
        if "frequency" in key.lower():
            try:
                return float(value), payload
            except (TypeError, ValueError):
                continue

    return None, None


async def run(poll_seconds: int = 60) -> None:
    client = ERCOTClient()
    try:
        while True:
            ts = datetime.now(timezone.utc).isoformat()
            payload = await client.get_system_frequency()
            frequency, record = _extract_frequency(payload)
            if frequency is not None:
                print(f"[{ts}] ERCOT system frequency: {frequency:.4f} Hz")
            else:
                sample = record or payload
                print(f"[{ts}] Frequency not found. Sample payload:")
                print(json.dumps(sample, indent=2)[:2000])
            await asyncio.sleep(poll_seconds)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(run())
