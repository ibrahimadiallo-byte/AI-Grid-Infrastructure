"""
ingestion_worker.py — Background Polling Worker
=================================================
Runs Maine (and later Texas) ingestion in a background thread.
Can be started by the FastAPI app on startup.
"""

import time
import threading
import logging

from maine_ingestion import fetch_maine_snapshot
from snapshot_store import save_snapshot

log = logging.getLogger("ingestion_worker")

_running = False
_thread = None


def _poll_loop(interval: int = 60):
    """Internal polling loop — runs in a background thread."""
    global _running
    cycle = 0
    while _running:
        cycle += 1
        try:
            # ── Maine ──
            snap = fetch_maine_snapshot()
            save_snapshot(snap)
            log.info(
                f"[Maine] Cycle {cycle} | "
                f"Gas={snap['fuel_mix'].get('gas_pct', '?')}% | "
                f"Price=${snap['lmp'].get('lmp_total', '?')}/MWh | "
                f"GreenMode={'ON' if snap['green_mode_triggered'] else 'OFF'}"
            )

            # ── Texas ── (placeholder for Ibrahima's module)
            # from texas_ingestion import fetch_texas_snapshot
            # tx_snap = fetch_texas_snapshot()
            # save_snapshot(tx_snap)

        except Exception as e:
            log.error(f"Ingestion cycle {cycle} failed: {e}")

        time.sleep(interval)


def start(interval: int = 60):
    """Start the background ingestion worker."""
    global _running, _thread
    if _running:
        log.warning("Worker already running.")
        return
    _running = True
    _thread = threading.Thread(target=_poll_loop, args=(interval,), daemon=True)
    _thread.start()
    log.info(f"Ingestion worker started (every {interval}s)")


def stop():
    """Stop the background ingestion worker."""
    global _running, _thread
    _running = False
    if _thread:
        _thread.join(timeout=5)
        _thread = None
    log.info("Ingestion worker stopped.")
