"""
panels/maine.py — Maine (ISO-NE) Dashboard Panel
===================================================
Gary's module. Renders all Maine-specific content.
Ibrahima: you don't need to touch this file.
"""

import streamlit as st
from datetime import datetime

from maine_ingestion import (
    fetch_maine_snapshot,
    GAS_THRESHOLD_PCT,
    PRICE_THRESHOLD_MWH,
)
from panels.shared import render_metric_card, render_fuel_bar, render_data_center_mock


# Fuel colors
FUEL_COLORS = {
    "Natural Gas": "#ef4444",
    "Nuclear": "#8b5cf6",
    "Hydro": "#3b82f6",
    "Renewables": "#22c55e",
    "Coal": "#6b7280",
    "Other": "#a1a1aa",
}


def get_sidebar_info() -> dict:
    """Return sidebar content specific to Maine's Green Mode rules."""
    return {
        "thresholds_title": "Green Mode Thresholds",
        "rules": [
            f"Gas > **{GAS_THRESHOLD_PCT}%** of fuel mix",
            f"Price > **${PRICE_THRESHOLD_MWH:.0f}**/MWh",
            "Action: **Reduce load 25%**",
        ],
    }


def render():
    """Main render function — called by dashboard.py when Maine is selected."""

    # Fetch live data
    with st.spinner("Fetching live ISO-NE data..."):
        snap = fetch_maine_snapshot()

    if not snap or not snap.get("fuel_mix"):
        st.error("❌ Could not fetch data from ISO-NE. Check your .env credentials.")
        st.stop()

    fm = snap["fuel_mix"]
    lmp = snap["lmp"]
    load = snap["system_load"]
    green_mode = snap["green_mode_triggered"]
    reasons = snap["trigger_reasons"]

    # ── Green Mode Banner ──
    if green_mode:
        reason_text = " | ".join(reasons)
        st.markdown(
            f'<div class="green-mode-on">'
            f'🔴 GREEN MODE ACTIVE — Load reduced 25% — {reason_text}'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="green-mode-off">'
            '🟢 GRID NORMAL — No throttling needed'
            '</div>',
            unsafe_allow_html=True,
        )

    # ── Header ──
    st.markdown("## 🏔️ Maine Grid — ISO New England")
    ts = snap.get("fetched_at", "")
    if ts:
        try:
            dt = datetime.fromisoformat(ts)
            st.caption(f"Last updated: {dt.strftime('%B %d, %Y at %I:%M:%S %p UTC')}")
        except Exception:
            st.caption(f"Last updated: {ts}")

    # ── Key Metrics ──
    col1, col2, col3, col4 = st.columns(4)

    gas_pct = fm.get("gas_pct", 0)
    price = lmp.get("lmp_total", 0)

    with col1:
        gas_status = "🔴 ABOVE" if fm.get("gas_above_threshold") else "🟢 Below"
        render_metric_card(
            f"{gas_pct:.1f}%",
            "Natural Gas Share",
            f"{gas_status} {GAS_THRESHOLD_PCT}% threshold",
        )
    with col2:
        price_status = "🔴 ABOVE" if lmp.get("price_above_threshold") else "🟢 Below"
        render_metric_card(
            f"${price:.2f}",
            "Maine LMP ($/MWh)",
            f"{price_status} ${PRICE_THRESHOLD_MWH:.0f} threshold",
        )
    with col3:
        render_metric_card(
            f"{load.get('load_mw', 0):,.0f}",
            "System Load (MW)",
            "New England total demand",
        )
    with col4:
        render_metric_card(
            f"{fm.get('total_mw', 0):,.0f}",
            "Total Generation (MW)",
            "All fuel sources combined",
        )

    st.markdown("")

    # ── Two-column: Fuel Mix + Price Detail ──
    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.markdown("### ⛽ Generation Fuel Mix")
        fuels = fm.get("fuels", {})
        sorted_fuels = sorted(fuels.items(), key=lambda x: -x[1]["mw"])
        for fuel_name, fuel_info in sorted_fuels:
            color = FUEL_COLORS.get(fuel_name, "#64748b")
            render_fuel_bar(
                fuel_name,
                fuel_info["pct"],
                fuel_info["mw"],
                color,
                fuel_info.get("marginal", False),
            )

        renew = fuels.get("Renewables", {})
        subs = renew.get("subcategories", {})
        if subs:
            with st.expander("🌿 Renewables Breakdown"):
                for sub_name, sub_mw in sorted(subs.items(), key=lambda x: -x[1]):
                    st.markdown(f"- **{sub_name}**: {sub_mw:,} MW")

    with right_col:
        st.markdown("### 💰 Price Components")
        energy = lmp.get("energy_component", 0)
        congestion = lmp.get("congestion_component", 0)
        loss = lmp.get("loss_component", 0)

        st.markdown(f"""
        <div class="metric-card" style="text-align: left;">
            <div style="font-size: 0.9rem; margin-bottom: 0.8rem;">
                <strong>LMP Breakdown for Maine (.Z.MAINE)</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid #334155;">
                <span>⚡ Energy</span>
                <span style="font-weight: 700;">${energy:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid #334155;">
                <span>🚧 Congestion</span>
                <span style="font-weight: 700;">${congestion:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid #334155;">
                <span>📉 Loss</span>
                <span style="font-weight: 700;">${loss:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.6rem 0 0.2rem; font-size: 1.1rem;">
                <span style="font-weight: 700;">Total LMP</span>
                <span style="font-weight: 800; color: {'#ef4444' if lmp.get('price_above_threshold') else '#22c55e'};">
                    ${price:.2f}/MWh
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### 🎯 Green Mode Rules")
        st.markdown(f"""
        <div class="metric-card" style="text-align: left; font-size: 0.9rem;">
            <div style="padding: 0.3rem 0;">
                {"🔴" if fm.get("gas_above_threshold") else "⚪"} Gas > {GAS_THRESHOLD_PCT}% →
                currently <strong>{gas_pct:.1f}%</strong>
            </div>
            <div style="padding: 0.3rem 0;">
                {"🔴" if lmp.get("price_above_threshold") else "⚪"} Price > ${PRICE_THRESHOLD_MWH:.0f} →
                currently <strong>${price:.2f}</strong>
            </div>
            <div style="padding: 0.5rem 0 0.2rem; border-top: 1px solid #334155; margin-top: 0.3rem;">
                Either trigger = <strong>Reduce data center load 25%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Data Center Response ──
    st.markdown("---")
    st.markdown("### 🖥️ Data Center Response")
    render_data_center_mock("Maine", green_mode, reduction_pct=25)

    # ── Raw data ──
    st.markdown("---")
    with st.expander("📋 Raw Snapshot Data (for debugging)"):
        st.json(snap)
