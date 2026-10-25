"""
Multimodal Construction Intelligence Platform
=============================================
Tab 2 · Crack Diagnostics & Structural Integrity
Epic 2 — Gemini Vision-powered crack classification and repair specification.
"""

import streamlit as st
import json
import datetime
from PIL import Image
import io
from typing import Optional
from gemini_utils import analyze_crack
from demo_data import get_demo_crack_report

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

URGENCY_CONFIG = {
    "Immediate": {"color": "#ef4444", "icon": "🚨", "class": "pill-danger"},
    "High":      {"color": "#f97316", "icon": "🔴", "class": "pill-danger"},
    "Medium":    {"color": "#fbbf24", "icon": "🟡", "class": "pill-warning"},
    "Low":       {"color": "#22c55e", "icon": "🟢", "class": "pill-safe"},
    "Critical":  {"color": "#a855f7", "icon": "💜", "class": "pill-critical"},
    "Monitor Only": {"color": "#3b82f6", "icon": "🔵", "class": "pill-info"},
}

RISK_COLORS = {
    "None":           "#22c55e",
    "Negligible":     "#22c55e",
    "Very Low":       "#22c55e",
    "Low":            "#86efac",
    "Low-Moderate":   "#fbbf24",
    "Moderate":       "#fbbf24",
    "Moderate-High":  "#f97316",
    "High":           "#f97316",
    "Severe":         "#ef4444",
    "Critical":       "#a855f7",
}

CRACK_TYPE_DESCRIPTIONS = {
    "HC-01": "Hairline Shrinkage Crack — Superficial surface cracks due to plastic shrinkage during curing.",
    "SC-02": "Settlement Crack — Vertical or diagonal cracks caused by differential foundation settlement.",
    "SC-03": "Structural Shear Crack — Diagonal cracks indicating shear force exceedance at structural members.",
    "TC-04": "Thermal Expansion Crack — Cracks due to thermal cycling and restrained movement.",
    "SP-05": "Spalling & Delamination — Concrete surface detachment, often with exposed reinforcement.",
    "ASR-06": "Alkali-Silica Reaction — Map/pattern cracking caused by chemical gel expansion.",
    "CI-07": "Corrosion-Induced Cracking — Cracks along rebar lines caused by reinforcement corrosion expansion.",
    "ND-00": "No Significant Defect — Surface is within acceptable limits per IS 456:2000.",
}


def _risk_badge(level: str) -> str:
    color = RISK_COLORS.get(level, "#fbbf24")
    return f'<span style="color:{color}; font-weight:600;">{level}</span>'


def _priority_pill(priority: str) -> str:
    config = {
        "Immediate": "pill-danger",
        "Urgent":    "pill-danger",
        "Routine":   "pill-warning",
        "Optional":  "pill-info",
        "Concurrent":"pill-warning",
        "Post-Repair": "pill-safe",
        "Recommended": "pill-info",
    }
    cls = config.get(priority, "pill-info")
    return f'<span class="pill {cls}">{priority}</span>'


def _render_crack_report(report: dict):
    defect = report.get("defect_classification", "Unknown")
    code = report.get("crack_type_code", "")
    urgency = report.get("urgency", "Medium")
    urgency_cfg = URGENCY_CONFIG.get(urgency, URGENCY_CONFIG["Medium"])
    urgency_score = report.get("urgency_score", 50)
    width_mm = report.get("estimated_crack_width_mm", 0)
    length_mm = report.get("estimated_crack_length_mm", 0)
    depth = report.get("crack_depth", "Unknown")
    orientation = report.get("crack_orientation", "Unknown")
    area = report.get("affected_area_m2", 0)

    # ── Defect Header ──
    st.markdown(f"""
    <div class="crack-result-card">
        <span class="crack-type-badge">{code} · {defect}</span>
        <div style="font-size:0.85rem; color:rgba(255,255,255,0.5); margin-bottom:1rem;">
            {CRACK_TYPE_DESCRIPTIONS.get(code, "")}
        </div>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{width_mm}</div>
                <div class="metric-label">Width (mm)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{length_mm}</div>
                <div class="metric-label">Length (mm)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{area}</div>
                <div class="metric-label">Area (m²)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="font-size:1.4rem; color:{urgency_cfg['color']};">{urgency_cfg['icon']} {urgency}</div>
                <div class="metric-label">Urgency</div>
            </div>
        </div>
        <div style="display:flex; gap:2rem; margin-top:0.5rem; font-size:0.85rem; color:rgba(255,255,255,0.6);">
            <span>📐 <strong>Orientation:</strong> {orientation}</span>
            <span>🔩 <strong>Depth:</strong> {depth}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Urgency Score Bar ──
    st.markdown(f"""
    <div style="margin:1rem 0 0.3rem; font-size:0.85rem; color:rgba(255,255,255,0.6);">
        Urgency Score: <strong style="color:{urgency_cfg['color']};">{urgency_score}/100</strong>
    </div>
    <div class="milestone-bar-wrapper">
        <div class="milestone-bar-fill" style="width:{urgency_score}%; background:linear-gradient(90deg,{urgency_cfg['color']},{urgency_cfg['color']}88);">
            {urgency_score}%
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Root Causes ──
    causes = report.get("root_causes", [])
    if causes:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🔍</div>
            <h3>Root Cause Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        for i, cause in enumerate(causes, 1):
            st.markdown(f"""
            <div style="display:flex; gap:0.8rem; align-items:flex-start; padding:0.6rem 0.9rem;
                        background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:0.4rem;
                        border-left:3px solid rgba(255,107,53,0.5);">
                <span style="color:#FF6B35; font-weight:700; flex-shrink:0;">{i:02d}</span>
                <span style="color:rgba(255,255,255,0.75); font-size:0.87rem;">{cause}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Structural Risk Assessment ──
    risk = report.get("structural_risk_assessment", {})
    if risk:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🏗️</div>
            <h3>Structural Risk Assessment</h3>
        </div>
        """, unsafe_allow_html=True)

        risk_items = [
            ("⚖️ Load Bearing Impact",         risk.get("load_bearing_impact", "Unknown")),
            ("💥 Collapse Risk",                risk.get("collapse_risk", "Unknown")),
            ("💧 Water Ingress Risk",            risk.get("water_ingress_risk", "Unknown")),
            ("🔩 Reinforcement Corrosion Risk", risk.get("reinforcement_corrosion_risk", "Unknown")),
        ]
        cols = st.columns(2)
        for i, (label, level) in enumerate(risk_items):
            with cols[i % 2]:
                color = RISK_COLORS.get(level, "#fbbf24")
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
                            border-radius:14px; padding:1rem 1.2rem; margin-bottom:0.7rem;">
                    <div style="font-size:0.75rem; color:rgba(255,255,255,0.4); margin-bottom:0.25rem;">{label}</div>
                    <div style="font-size:1rem; font-weight:700; color:{color};">{level}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── Recommended Repairs ──
    repairs = report.get("recommended_repairs", [])
    if repairs:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🔧</div>
            <h3>Engineering Repair Specifications</h3>
        </div>
        """, unsafe_allow_html=True)
        for r in repairs:
            priority_pill = _priority_pill(r.get("priority", "Routine"))
            st.markdown(f"""
            <div class="hazard-card">
                <div class="hazard-header">
                    <span class="hazard-title">🔨 {r.get("repair_method","")}</span>
                    <span style="display:flex; align-items:center; gap:0.5rem;">
                        {priority_pill}
                    </span>
                </div>
                <div class="hazard-desc">{r.get("description","")}</div>
                <div class="hazard-remedy" style="margin-top:0.6rem;">
                    💰 <strong>Estimated Cost:</strong> {r.get("estimated_cost_inr","TBD")}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Immediate Actions ──
    actions = report.get("immediate_actions", [])
    if actions:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🚨</div>
            <h3>Immediate Actions Required</h3>
        </div>
        """, unsafe_allow_html=True)
        for action in actions:
            st.markdown(f'<div class="danger-box">⚡ {action}</div>', unsafe_allow_html=True)

    # ── Monitoring ──
    monitoring = report.get("monitoring_recommendation", "")
    if monitoring:
        st.markdown(f"""
        <div class="section-header">
            <div class="section-icon">📡</div>
            <h3>Monitoring Protocol</h3>
        </div>
        <div class="info-box">📡 {monitoring}</div>
        """, unsafe_allow_html=True)

    # ── References ──
    refs = report.get("compliance_references", [])
    if refs:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📚</div>
            <h3>Compliance References</h3>
        </div>
        """, unsafe_allow_html=True)
        ref_html = " &nbsp;|&nbsp; ".join([f'<code style="background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);padding:2px 8px;border-radius:4px;font-size:0.78rem;color:#93c5fd;">{r}</code>' for r in refs])
        st.markdown(f"<div style='margin:0.5rem 0; line-height:2;'>{ref_html}</div>", unsafe_allow_html=True)

    # ── Download ──
    st.markdown("---")
    json_str = json.dumps(report, indent=2, ensure_ascii=False)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="⬇️  Download Crack Diagnostic Report (JSON)",
        data=json_str,
        file_name=f"crack_diagnosis_{timestamp}.json",
        mime="application/json",
        use_container_width=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Main render
# ──────────────────────────────────────────────────────────────────────────────

def render_crack_tab(api_key: Optional[str] = None):
    demo_mode = not api_key

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🔬</div>
        <h3>Crack Diagnostics & Structural Integrity Analysis — Epic 2</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        Upload an image of a cracked concrete or masonry surface. The AI will classify the defect type,
        estimate crack dimensions, identify root causes, and prescribe engineering repair methods
        per <strong>IS 456:2000</strong>, <strong>ACI 224.1R</strong>, and <strong>ASTM C881</strong> standards.
    </div>
    """, unsafe_allow_html=True)

    if demo_mode:
        st.markdown("""
        <div class="demo-banner">
            🔮 <strong>Demo Mode Active</strong> — Showing sample crack diagnostic report.
            Connect your Gemini API key for real image analysis.
        </div>
        """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📸 Upload Crack / Surface Defect Image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a clear photo of the cracked surface. Better lighting = higher accuracy.",
        key="crack_uploader"
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        analyze_btn = st.button(
            "🔬 Diagnose Structural Defect",
            use_container_width=True,
            key="crack_btn",
            type="primary"
        )
    with col2:
        demo_btn = st.button(
            "📋 Load Demo Report",
            use_container_width=True,
            key="crack_demo_btn"
        )

    if uploaded_file:
        img = Image.open(uploaded_file)
        col_img, col_info = st.columns([3, 2])
        with col_img:
            st.image(img, caption="Uploaded Surface Image", use_container_width=True)
        with col_info:
            st.markdown("""
            <div style="padding:1rem; background:rgba(255,255,255,0.03); border-radius:10px; border:1px solid rgba(255,255,255,0.07);">
                <div style="font-size:0.85rem; font-weight:600; color:#fff; margin-bottom:0.8rem;">Analysis Scope</div>
                <div style="font-size:0.8rem; color:rgba(255,255,255,0.55); line-height:2;">
                    ✅ Crack type classification<br>
                    ✅ Dimensional estimation (width/length)<br>
                    ✅ Root cause identification<br>
                    ✅ Structural risk assessment<br>
                    ✅ Repair specification with costs<br>
                    ✅ IS 456 / ACI compliance check
                </div>
            </div>
            """, unsafe_allow_html=True)

    if analyze_btn:
        if not uploaded_file:
            st.markdown('<div class="warning-box">⚠️ Please upload a crack/surface image before running diagnostics.</div>', unsafe_allow_html=True)
            return

        if demo_mode:
            st.markdown('<div class="warning-box">⚠️ Demo Mode: Showing sample crack report. Add Gemini API key for real analysis.</div>', unsafe_allow_html=True)
            report = get_demo_crack_report()
        else:
            with st.spinner("🔬 Analyzing structural defects with Gemini Vision..."):
                try:
                    uploaded_file.seek(0)
                    image_bytes = uploaded_file.read()
                    report = analyze_crack(image_bytes, api_key)
                except json.JSONDecodeError as e:
                    st.markdown(f'<div class="danger-box">⚠️ JSON parsing error: {e}. Please retry — the model may have returned non-JSON text.</div>', unsafe_allow_html=True)
                    return
                except Exception as e:
                    st.markdown(f'<div class="danger-box">⚠️ Analysis error: {e}</div>', unsafe_allow_html=True)
                    return

        st.markdown("---")
        st.markdown("### 🔬 Crack Diagnostic Report")
        _render_crack_report(report)

    elif demo_btn:
        report = get_demo_crack_report()
        st.markdown("---")
        st.markdown("### 🔬 Demo Crack Diagnostic Report")
        _render_crack_report(report)

