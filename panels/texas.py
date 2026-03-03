"""
panels/texas.py — Texas (ERCOT) Dashboard Panel
==================================================
🚧 PLACEHOLDER — Ibrahima, this is YOUR file to build out.

Instructions:
  1. Create a texas_ingestion.py (same pattern as maine_ingestion.py)
     with a fetch_texas_snapshot() function that returns:
     {
         "state": "texas",
         "fetched_at": "...",
         "frequency": { "hz": 59.98, "below_threshold": False },
         "fuel_mix": { ... },
         "system_load": { ... },
         "reliability_mode_triggered": True/False,
         "trigger_reasons": [...]
     }

  2. Fill in the render() function below using shared components
     from panels.shared (render_metric_card, render_fuel_bar, etc.)

  3. Optionally add get_sidebar_info() to show Texas-specific
     thresholds in the sidebar.

You do NOT need to touch dashboard.py or panels/maine.py.
"""

import streamlit as st
from panels.shared import render_metric_card, render_data_center_mock


def get_sidebar_info() -> dict:
    """Return sidebar content specific to Texas Reliability Mode rules."""
    return {
        "thresholds_title": "Reliability Mode Thresholds",
        "rules": [
            "Frequency < **59.97 Hz**",
            "Action: **Reduce load 40%**",
        ],
    }


def render():
    """
    Main render function — called by dashboard.py when Texas is selected.
    Replace this placeholder with real ERCOT data once texas_ingestion.py is ready.
    """
    st.markdown("## 🤠 Texas Grid (ERCOT)")

    st.info(
        "🔧 **Texas data ingestion is being built by Ibrahima.**\n\n"
        "Once `texas_ingestion.py` is created with a `fetch_texas_snapshot()` function, "
        "this panel will show live ERCOT frequency, reserves, fuel mix, "
        "and Reliability Mode status.\n\n"
        "**To get started:**\n"
        "1. Create `texas_ingestion.py` (follow `maine_ingestion.py` as a template)\n"
        "2. Edit this file (`panels/texas.py`) to call your ingestion and render the data\n"
        "3. Use shared components from `panels/shared.py` for consistent styling",
        icon="🚧",
    )

    # ── Preview of what it will look like ──
    st.markdown("### 📐 Preview (Mock Data)")
    st.caption("This is a preview using fake values so you can see the layout.")

    st.markdown(
        '<div class="reliability-mode-off">'
        '🟢 GRID NORMAL — No throttling needed'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("60.00 Hz", "Grid Frequency", "🟢 Normal range")
    with col2:
        render_metric_card("$42.50", "ERCOT LMP ($/MWh)", "Real-time price")
    with col3:
        render_metric_card("45,200", "System Load (MW)", "ERCOT total demand")

    st.markdown("---")
    st.markdown("### 🖥️ Data Center Response")
    render_data_center_mock("Texas", throttled=False, reduction_pct=40)
