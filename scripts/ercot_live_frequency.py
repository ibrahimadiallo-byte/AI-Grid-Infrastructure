import asyncio
import json
import os
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Optional, Tuple

import httpx

from api.ercot_client import ERCOTClient


class _TableTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._capture = False
        self.cells: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"td", "th"}:
            self._capture = True

    def handle_endtag(self, tag):
        if tag in {"td", "th"}:
            self._capture = False

    def handle_data(self, data):
        if self._capture:
            text = data.strip()
            if text:
                self.cells.append(text)


def _extract_frequency(payload: dict) -> Tuple[Optional[float], Optional[dict]]:
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


def _extract_frequency_from_html(html: str) -> Tuple[Optional[float], Optional[str]]:
    parser = _TableTextParser()
    parser.feed(html)
    cells = parser.cells

    for idx, cell in enumerate(cells):
        if "frequency" in cell.lower() and "current" in cell.lower():
            if idx + 1 < len(cells):
                try:
                    return float(cells[idx + 1]), cell
                except ValueError:
                    continue
    return None, None


async def run(poll_seconds: int = 60) -> None:
    client = ERCOTClient()
    try:
        while True:
            ts = datetime.now(timezone.utc).isoformat()
            frequency_endpoint = os.getenv("ERCOT_FREQUENCY_ENDPOINT", "").strip()
            frequency_url = os.getenv(
                "ERCOT_FREQUENCY_URL",
                "https://www.ercot.com/content/cdr/html/real_time_system_conditions.html",
            ).strip()

            if frequency_endpoint:
                payload = await client.get_system_frequency()
                frequency, record = _extract_frequency(payload)
                if frequency is not None:
                    print(f"[{ts}] ERCOT system frequency: {frequency:.4f} Hz")
                else:
                    sample = record or payload
                    print(f"[{ts}] Frequency not found in API payload. Sample:")
                    print(json.dumps(sample, indent=2)[:2000])
            else:
                async with httpx.AsyncClient(timeout=30) as http_client:
                    resp = await http_client.get(frequency_url)
                    resp.raise_for_status()
                    frequency, label = _extract_frequency_from_html(resp.text)
                    if frequency is not None:
                        print(f"[{ts}] ERCOT system frequency: {frequency:.4f} Hz")
                    else:
                        print(f"[{ts}] Frequency not found in HTML payload ({label}).")
            await asyncio.sleep(poll_seconds)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(run())
