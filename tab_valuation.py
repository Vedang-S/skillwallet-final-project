"""
Multimodal Construction Intelligence Platform
=============================================
Tab 3 · Planning & Real Estate Valuation
Epic 3 — Budget estimation, material take-off, and 3D render generation.
"""

import streamlit as st
import math
import urllib.parse
from typing import Optional

# ──────────────────────────────────────────────────────────────────────────────
# Configuration Tables
# ──────────────────────────────────────────────────────────────────────────────

STRUCTURE_CONFIGS = {
    "Residential Villa / Bungalow": {
        "base_cost_per_sqft": 2200,
        "steel_kg_per_sqft":  4.5,
        "cement_bags_per_sqft": 0.55,
        "sand_cft_per_sqft": 1.4,
        "aggregate_cft_per_sqft": 2.1,
        "floors_typical": 2,
        "description": "Load-bearing / RCC frame structure with premium finishes.",
    },
    "Apartment / Multi-Storey RCC": {
        "base_cost_per_sqft": 1950,
        "steel_kg_per_sqft":  5.2,
        "cement_bags_per_sqft": 0.65,
        "sand_cft_per_sqft": 1.6,
        "aggregate_cft_per_sqft": 2.4,
        "floors_typical": 10,
        "description": "High-rise RCC frame with IS 456 ductile detailing.",
    },
    "Commercial Office / IT Park": {
        "base_cost_per_sqft": 2800,
        "steel_kg_per_sqft":  6.0,
        "cement_bags_per_sqft": 0.70,
        "sand_cft_per_sqft": 1.8,
        "aggregate_cft_per_sqft": 2.7,
        "floors_typical": 5,
        "description": "Steel / composite frame with HVAC, raised flooring.",
    },
    "Industrial Warehouse / Factory": {
        "base_cost_per_sqft": 1400,
        "steel_kg_per_sqft":  7.5,
        "cement_bags_per_sqft": 0.45,
        "sand_cft_per_sqft": 1.1,
        "aggregate_cft_per_sqft": 1.8,
        "floors_typical": 1,
        "description": "Pre-engineered building or structural steel portal frame.",
    },
    "Hospital / Healthcare Facility": {
        "base_cost_per_sqft": 3500,
        "steel_kg_per_sqft":  5.8,
        "cement_bags_per_sqft": 0.72,
        "sand_cft_per_sqft": 1.7,
        "aggregate_cft_per_sqft": 2.6,
        "floors_typical": 4,
        "description": "Seismic Zone IV compliant, MEP-intensive medical facility.",
    },
    "School / Educational Building": {
        "base_cost_per_sqft": 1800,
        "steel_kg_per_sqft":  4.8,
        "cement_bags_per_sqft": 0.60,
        "sand_cft_per_sqft": 1.5,
        "aggregate_cft_per_sqft": 2.2,
        "floors_typical": 3,
        "description": "NBC 2016 compliant institutional building with fire exits.",
    },
    "Luxury Hotel / Resort": {
        "base_cost_per_sqft": 4200,
        "steel_kg_per_sqft":  5.5,
        "cement_bags_per_sqft": 0.68,
        "sand_cft_per_sqft": 1.6,
        "aggregate_cft_per_sqft": 2.5,
        "floors_typical": 8,
        "description": "High-end hospitality with premium MEP, façade, and interiors.",
    },
    "Affordable Housing / EWS-LIG": {
        "base_cost_per_sqft": 1100,
        "steel_kg_per_sqft":  3.8,
        "cement_bags_per_sqft": 0.48,
        "sand_cft_per_sqft": 1.2,
        "aggregate_cft_per_sqft": 1.9,
        "floors_typical": 4,
        "description": "PMAY / EWS compliant load-bearing masonry with RCC slabs.",
    },
}

LOCATION_TIERS = {
    "Tier 1 (Mumbai, Delhi NCR, Bengaluru, Chennai, Hyderabad, Pune)": {
        "market_multiplier": 1.65,
        "land_cost_lakh_per_sqft": 1.8,
        "rental_yield_pct": 3.2,
        "appreciation_pct": 8.5,
        "cities": "Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune",
    },
    "Tier 2 (Ahmedabad, Surat, Jaipur, Lucknow, Kochi, Chandigarh)": {
        "market_multiplier": 1.25,
        "land_cost_lakh_per_sqft": 0.65,
        "rental_yield_pct": 4.1,
        "appreciation_pct": 7.0,
        "cities": "Ahmedabad, Surat, Jaipur, Lucknow, Kochi, Chandigarh",
    },
    "Tier 3 (Nashik, Coimbatore, Vizag, Bhopal, Indore, Udaipur)": {
        "market_multiplier": 0.90,
        "land_cost_lakh_per_sqft": 0.25,
        "rental_yield_pct": 5.5,
        "appreciation_pct": 5.5,
        "cities": "Nashik, Coimbatore, Vizag, Bhopal, Indore, Udaipur",
    },
}

MILESTONES = [
    ("Foundation & Excavation",     15),
    ("Structural Frame (Floors)",   40),
    ("Masonry & Infill Walls",      55),
    ("MEP Roughing-in",             70),
    ("Plastering & Finishes",       85),
    ("Fit-out & Handover",         100),
]


def _format_inr(amount_lakh: float) -> tuple[str, str]:
    """Return (formatted_value, unit) for INR in Lakh/Crore."""
    if amount_lakh >= 100:
        crore = amount_lakh / 100
        return f"₹{crore:.2f}", "Crores"
    return f"₹{amount_lakh:.2f}", "Lakhs"


def _generate_pollinations_url(prompt: str, width: int = 800, height: int = 500) -> str:
    """Build a Pollinations AI image URL for architectural rendering."""
    encoded = urllib.parse.quote(prompt)
    seed = hash(prompt) % 999999
    return f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true&enhance=true"


def _get_milestone_label(completion: int) -> str:
    for label, threshold in MILESTONES:
        if completion <= threshold:
            return label
    return "Handover Complete"


def render_valuation_tab(api_key: Optional[str] = None):
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🏙️</div>
        <h3>Planning & Real Estate Valuation Engine — Epic 3</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        Configure your project parameters below to generate a comprehensive financial model —
        total budget, capital expenditure, market asset valuation in INR, material take-off (steel/cement),
        and a milestone progress dashboard. Includes AI-powered 3D architectural render generation.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── INPUT PANEL ──────────────────────────────────────────────────────────
    st.markdown("### ⚙️ Project Configuration")

    col1, col2 = st.columns(2)

    with col1:
        structure_type = st.selectbox(
            "🏗️ Structure Type",
            list(STRUCTURE_CONFIGS.keys()),
            help="Select the primary occupancy/use of the building"
        )
        builtup_sqft = st.number_input(
            "📐 Built-up Area (sq ft)",
            min_value=500,
            max_value=5_000_000,
            value=3500,
            step=100,
            help="Total built-up / plinth area of the project"
        )
        project_name = st.text_input(
            "🏷️ Project Name",
            value="Skyline Heights Phase 1",
            placeholder="Enter project name"
        )

    with col2:
        location_tier = st.selectbox(
            "📍 Location Tier",
            list(LOCATION_TIERS.keys()),
            help="City tier determines market valuation multiplier"
        )
        completion_pct = st.slider(
            "🚧 Construction Completion (%)",
            min_value=0, max_value=100, value=45, step=5,
            help="Current stage of construction completion"
        )
        num_floors = st.number_input(
            "🏢 Number of Floors",
            min_value=1, max_value=60, value=5
        )

    col3, col4 = st.columns(2)
    with col3:
        land_area_sqft = st.number_input(
            "🌍 Land Area (sq ft)",
            min_value=0, max_value=1_000_000, value=8000, step=100
        )
        contingency_pct = st.slider(
            "📊 Contingency (%)",
            min_value=0, max_value=30, value=10,
            help="Contingency allowance over base construction cost"
        )
    with col4:
        gst_rate = st.selectbox(
            "🧾 GST Rate",
            ["5% (Affordable Housing)", "12% (Other Residential)", "18% (Commercial)"],
            index=1
        )
        profit_margin_pct = st.slider(
            "💹 Developer Profit Margin (%)",
            min_value=0, max_value=40, value=18,
            help="Expected developer profit / markup"
        )

    calculate_btn = st.button(
        "📊 Calculate Project Financials & Generate 3D Render",
        use_container_width=True,
        type="primary",
        key="valuation_btn"
    )

    if not calculate_btn:
        return

    # ── CALCULATIONS ─────────────────────────────────────────────────────────
    config = STRUCTURE_CONFIGS[structure_type]
    loc = LOCATION_TIERS[location_tier]

    gst_pct = {"5%": 0.05, "12%": 0.12, "18%": 0.18}
    gst_val = gst_pct.get(gst_rate.split("%")[0].strip(), 0.12)

    # Base construction
    base_cost = config["base_cost_per_sqft"] * builtup_sqft  # INR
    contingency_cost = base_cost * (contingency_pct / 100)
    gst_amount = base_cost * gst_val
    total_construction_cost = base_cost + contingency_cost + gst_amount  # INR

    # Land cost
    land_cost_inr = land_area_sqft * loc["land_cost_lakh_per_sqft"] * 100_000  # INR

    # Total project budget
    total_budget_inr = total_construction_cost + land_cost_inr
    total_budget_lakh = total_budget_inr / 100_000

    # Capital expenditure incurred
    capex_incurred_lakh = total_budget_lakh * (completion_pct / 100)

    # Market valuation
    market_value_per_sqft = config["base_cost_per_sqft"] * loc["market_multiplier"] * (1 + profit_margin_pct / 100)
    market_value_inr = market_value_per_sqft * builtup_sqft
    market_value_lakh = market_value_inr / 100_000
    market_value_completed_lakh = market_value_lakh + (land_cost_inr / 100_000)

    # Land appreciation
    land_value_lakh = land_cost_inr / 100_000

    # Material take-off
    steel_kg = config["steel_kg_per_sqft"] * builtup_sqft
    cement_bags = config["cement_bags_per_sqft"] * builtup_sqft
    sand_cft = config["sand_cft_per_sqft"] * builtup_sqft
    aggregate_cft = config["aggregate_cft_per_sqft"] * builtup_sqft

    # Current asset value (completion-weighted)
    current_asset_lakh = (market_value_completed_lakh * completion_pct / 100) + (land_value_lakh * 0.5)

    # ROI
    roi_pct = ((market_value_completed_lakh - total_budget_lakh) / total_budget_lakh) * 100 if total_budget_lakh > 0 else 0

    # ── RESULTS DISPLAY ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"### 📊 Financial Model — *{project_name}*")

    # Top KPI Metrics
    bv, bu = _format_inr(total_budget_lakh)
    cv, cu = _format_inr(capex_incurred_lakh)
    mv, mu = _format_inr(market_value_completed_lakh)
    av, au = _format_inr(current_asset_lakh)

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.6rem;">{bv}</div>
            <div class="metric-label">{bu} · Total Budget</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.6rem; color:#fbbf24;">{cv}</div>
            <div class="metric-label">{cu} · CAPEX Incurred ({completion_pct}%)</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.6rem; color:#22c55e;">{mv}</div>
            <div class="metric-label">{mu} · Market Valuation (On Completion)</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.6rem; color:#60a5fa;">{av}</div>
            <div class="metric-label">{au} · Current Asset Value</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Secondary metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        lv, lu = _format_inr(land_value_lakh)
        st.markdown(f"""
        <div class="valuation-card">
            <div style="font-size:0.78rem; color:rgba(255,255,255,0.4); margin-bottom:0.3rem;">LAND VALUE</div>
            <div class="valuation-amount">{lv}</div>
            <div class="valuation-unit">{lu}</div>
            <div style="font-size:0.75rem; color:rgba(255,255,255,0.35); margin-top:0.5rem;">
                @ ₹{loc['land_cost_lakh_per_sqft']:.2f}L/sqft
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="valuation-card">
            <div style="font-size:0.78rem; color:rgba(255,255,255,0.4); margin-bottom:0.3rem;">DEVELOPER ROI</div>
            <div class="valuation-amount" style="color:{'#22c55e' if roi_pct >= 0 else '#ef4444'};">{roi_pct:.1f}%</div>
            <div class="valuation-unit">Return on Investment</div>
            <div style="font-size:0.75rem; color:rgba(255,255,255,0.35); margin-top:0.5rem;">
                Profit Margin: {profit_margin_pct}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="valuation-card">
            <div style="font-size:0.78rem; color:rgba(255,255,255,0.4); margin-bottom:0.3rem;">MARKET RATE / SQFT</div>
            <div class="valuation-amount" style="font-size:1.5rem;">₹{market_value_per_sqft:,.0f}</div>
            <div class="valuation-unit">Per sq ft · {loc['cities'].split(',')[0].strip()}</div>
            <div style="font-size:0.75rem; color:rgba(255,255,255,0.35); margin-top:0.5rem;">
                Appreciation: ~{loc['appreciation_pct']}% p.a.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Milestone Progress ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🚧</div>
        <h3>Construction Milestone Progress</h3>
    </div>
    """, unsafe_allow_html=True)

    current_milestone = _get_milestone_label(completion_pct)

    for label, threshold in MILESTONES:
        if completion_pct >= threshold:
            fill = 100
            color = "#22c55e"
            status_icon = "✅"
        elif completion_pct > (threshold - 15):
            fill = int((completion_pct - (threshold - 15)) / 15 * 100)
            color = "#FF6B35"
            status_icon = "🔄"
        else:
            fill = 0
            color = "rgba(255,255,255,0.15)"
            status_icon = "⏳"

        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.7rem;">
            <span style="width:24px; text-align:center;">{status_icon}</span>
            <span style="font-size:0.82rem; color:rgba(255,255,255,0.7); width:220px; flex-shrink:0;">{label}</span>
            <div style="flex:1; background:rgba(255,255,255,0.06); border-radius:6px; height:12px; overflow:hidden;">
                <div style="width:{fill}%; height:100%; background:linear-gradient(90deg, {color}, {color}aa);
                            border-radius:6px; transition:width 0.8s ease;"></div>
            </div>
            <span style="font-size:0.78rem; color:rgba(255,255,255,0.4); width:40px; text-align:right;">{threshold}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="success-box" style="margin-top:0.5rem;">
        📍 <strong>Current Stage:</strong> {current_milestone} &nbsp;|&nbsp;
        🏗️ <strong>Overall Completion:</strong> {completion_pct}% &nbsp;|&nbsp;
        📐 <strong>Built-up Area:</strong> {builtup_sqft:,} sq ft across {num_floors} floors
    </div>
    """, unsafe_allow_html=True)

    # ── Material Take-Off ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🏗️</div>
        <h3>Material Take-Off (MTO)</h3>
    </div>
    """, unsafe_allow_html=True)

    col_mat1, col_mat2, col_mat3, col_mat4 = st.columns(4)
    materials = [
        (col_mat1, "⚙️", f"{steel_kg:,.0f}",      "kg",          "Steel (Fe 415/500)"),
        (col_mat2, "🏭", f"{cement_bags:,.0f}",   "bags (50kg)", "OPC/PPC Cement"),
        (col_mat3, "🏜️", f"{sand_cft:,.0f}",     "cft",         "Fine Aggregate (Sand)"),
        (col_mat4, "🪨", f"{aggregate_cft:,.0f}", "cft",         "Coarse Aggregate"),
    ]

    for col, icon, value, unit, label in materials:
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
                        border-radius:16px; padding:1.2rem 1rem; text-align:center; border-top:3px solid #FF6B35;
                        transition: box-shadow 0.2s;">
                <div style="font-size:1.8rem; margin-bottom:0.4rem;">{icon}</div>
                <div style="font-size:1.4rem; font-weight:700; color:#FF6B35;">{value}</div>
                <div style="font-size:0.72rem; color:rgba(255,255,255,0.4);">{unit}</div>
                <div style="font-size:0.78rem; color:rgba(255,255,255,0.65); margin-top:0.35rem; font-weight:500;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # Steel per incurred work
    steel_incurred = steel_kg * (completion_pct / 100)
    cement_incurred = cement_bags * (completion_pct / 100)
    st.markdown(f"""
    <div class="info-box" style="margin-top:0.8rem;">
        📊 <strong>Material Consumed to Date ({completion_pct}% completion):</strong>
        &nbsp; Steel: <strong>{steel_incurred:,.0f} kg</strong>
        &nbsp;|&nbsp; Cement: <strong>{cement_incurred:,.0f} bags</strong>
        &nbsp;|&nbsp; Remaining Steel: <strong>{steel_kg - steel_incurred:,.0f} kg</strong>
    </div>
    """, unsafe_allow_html=True)

    # ── Cost Breakdown ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">💰</div>
        <h3>Cost Breakdown</h3>
    </div>
    """, unsafe_allow_html=True)

    breakdown_items = [
        ("Base Construction Cost",  base_cost / 100_000,           "#FF6B35"),
        ("Contingency",             contingency_cost / 100_000,    "#fbbf24"),
        ("GST",                     gst_amount / 100_000,          "#f97316"),
        ("Land Cost",               land_cost_inr / 100_000,       "#60a5fa"),
    ]

    for label, lakh_val, color in breakdown_items:
        pct_of_total = (lakh_val / total_budget_lakh) * 100 if total_budget_lakh > 0 else 0
        fv, fu = _format_inr(lakh_val)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.9rem; margin-bottom:0.6rem;
                    padding:0.6rem 0.9rem; background:rgba(255,255,255,0.02);
                    border-radius:10px; border:1px solid rgba(255,255,255,0.05);">
            <span style="font-size:0.82rem; color:rgba(255,255,255,0.6); width:200px; flex-shrink:0;">{label}</span>
            <div style="flex:1; background:rgba(255,255,255,0.06); border-radius:8px; height:10px; overflow:hidden;">
                <div style="width:{pct_of_total:.1f}%; height:100%; background:{color}; border-radius:8px; transition:width 0.8s;"></div>
            </div>
            <span style="font-size:0.82rem; color:rgba(255,255,255,0.75); width:100px; text-align:right; font-weight:600;">{fv} {fu}</span>
            <span style="font-size:0.73rem; color:rgba(255,255,255,0.35); width:36px;">{pct_of_total:.0f}%</span>
        </div>
        """, unsafe_allow_html=True)

    # ── 3D Architectural Render ──────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🎨</div>
        <h3>Conceptual 3D Architectural Rendering</h3>
    </div>
    """, unsafe_allow_html=True)

    # Build a rich prompt
    tier_city = loc["cities"].split(",")[0].strip()
    render_prompt = (
        f"photorealistic architectural 3D rendering of a {structure_type.lower()} building, "
        f"modern Indian architecture, {num_floors} floors, {tier_city} urban setting, "
        f"construction phase {completion_pct}% complete, golden hour lighting, "
        f"ultra-realistic 8K, architectural visualization, Unreal Engine 5 style"
    )

    pollinations_url = _generate_pollinations_url(render_prompt, 900, 500)

    st.markdown(f"""
    <div class="render-card">
        <div style="font-size:0.82rem; color:rgba(255,255,255,0.45); margin-bottom:0.8rem; font-style:italic;">
            🎨 AI-Generated Conceptual Render via Pollinations AI · Prompt: <em>"{render_prompt[:80]}..."</em>
        </div>
    """, unsafe_allow_html=True)

    # Try to load the image (requires network — graceful fallback for sandbox)
    try:
        st.image(
            pollinations_url,
            caption=f"Conceptual Render — {project_name} · {structure_type}",
            use_container_width=True
        )
    except Exception:
        st.markdown(f"""
        <div class="render-placeholder">
            🎨 3D Architectural Rendering<br><br>
            <strong>{project_name}</strong><br>
            <em>{structure_type} · {num_floors} Floors · {tier_city}</em><br><br>
            <code style="font-size:0.72rem; word-break:break-all;">{pollinations_url}</code><br><br>
            Open the URL above in your browser to view the AI-generated render.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Prompt display + copy ──
    with st.expander("🎨 View / Customize 3D Render Prompt"):
        render_prompt_custom = st.text_area(
            "Architectural render prompt (editable)",
            value=render_prompt,
            height=100,
            key="render_prompt_txt"
        )
        if st.button("🔄 Regenerate Render", key="regen_render"):
            new_url = _generate_pollinations_url(render_prompt_custom, 900, 500)
            try:
                st.image(new_url, caption="Regenerated Render", use_container_width=True)
            except Exception:
                st.code(new_url, language="")

    # ── Investment Summary ──
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">📈</div>
        <h3>Investment Summary</h3>
    </div>
    <div class="success-box">
        <strong>📊 {project_name} — Financial Snapshot</strong><br><br>
        • Total Project Budget: <strong>{bv} {bu}</strong> (incl. land + construction + taxes)<br>
        • CAPEX Incurred ({completion_pct}%): <strong>{cv} {cu}</strong><br>
        • Completed Market Value: <strong>{mv} {mu}</strong> &nbsp;|&nbsp; ROI: <strong>{roi_pct:.1f}%</strong><br>
        • Annual Capital Appreciation: ~<strong>{loc['appreciation_pct']}%</strong> in {loc['cities'].split(',')[0].strip()}<br>
        • Rental Yield Potential: ~<strong>{loc['rental_yield_pct']}%</strong> gross yield<br>
        • Steel Requirement: <strong>{steel_kg:,.0f} kg</strong> (Fe 415/500) &nbsp;|&nbsp;
          Cement: <strong>{cement_bags:,.0f} bags</strong>
    </div>
    """, unsafe_allow_html=True)
