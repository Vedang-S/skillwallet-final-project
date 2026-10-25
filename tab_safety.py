"""
Multimodal Construction Intelligence Platform
=============================================
Tab 1 · Site Safety & PPE Audit
Epic 2 — Multimodal PPE compliance analysis powered by Gemini Vision.
"""

import streamlit as st
import json
import datetime
from PIL import Image
import io
from gemini_utils import analyze_safety
from demo_data import get_demo_safety_report

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

PPE_ICONS = {
    "hard_hat_helmet":      "⛑️",
    "high_visibility_vest": "🦺",
    "steel_toe_boots":      "👢",
    "safety_harness":       "🪝",
    "safety_goggles":       "🥽",
    "gloves":               "🧤",
}

PPE_LABELS = {
    "hard_hat_helmet":      "Hard Hat / Helmet",
    "high_visibility_vest": "High-Visibility Vest",
    "steel_toe_boots":      "Steel-Toe Boots",
    "safety_harness":       "Safety Harness",
    "safety_goggles":       "Safety Goggles",
    "gloves":               "Protective Gloves",
}

SEV_COLOR = {
    "Low":      "#22c55e",
    "Medium":   "#fbbf24",
    "High":     "#f97316",
    "Critical": "#ef4444",
}

SEV_ICON = {
    "Low":      "🟢",
    "Medium":   "🟡",
    "High":     "🟠",
    "Critical": "🔴",
}


def _score_color(score: int) -> str:
    if score >= 85:
        return "#22c55e"
    elif score >= 65:
        return "#fbbf24"
    elif score >= 40:
        return "#f97316"
    return "#ef4444"


def _status_pill_class(status: str) -> str:
    s = status.lower()
    if "fully" in s or "high" in s:
        return "pill-safe"
    elif "partial" in s:
        return "pill-warning"
    elif "critical" in s:
        return "pill-critical"
    return "pill-danger"


def _ppe_item_class(ppe: dict) -> str:
    status = ppe.get("status", "").lower()
    if ppe.get("compliance"):
        return "ppe-compliant"
    elif "partial" in status:
        return "ppe-partial"
    return "ppe-violation"


def _ppe_status_pill(ppe: dict) -> str:
    status = ppe.get("status", "Unknown")
    if ppe.get("compliance"):
        return f'<span class="pill pill-safe">✓ {status}</span>'
    elif "partial" in status.lower():
        return f'<span class="pill pill-warning">⚠ {status}</span>'
    elif "not applicable" in status.lower():
        return f'<span class="pill pill-info">— {status}</span>'
    return f'<span class="pill pill-danger">✗ {status}</span>'


def _render_report(report: dict):
    score = report.get("safety_score", 0)
    status = report.get("overall_status", "Unknown")
    sc = _score_color(score)

    # ── Score + Status Banner ──
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:2rem; background:rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.08); border-radius:18px; padding:1.8rem 2.2rem; margin:1rem 0;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
        <div style="text-align:center; min-width:90px;">
            <div style="font-size:3.5rem; font-weight:800; color:{sc}; line-height:1;">{score}</div>
            <div style="font-size:0.72rem; color:rgba(255,255,255,0.4); text-transform:uppercase; letter-spacing:0.09em; margin-top:0.2rem;">Safety Score</div>
        </div>
        <div style="flex:1; padding:0 0.5rem;">
            <div style="font-size:1.25rem; font-weight:700; color:#fff; margin-bottom:0.5rem; line-height:1.2;">
                {status}
            </div>
            <div class="{_status_pill_class(status)}" style="display:inline-flex; align-items:center; padding:0.28rem 0.9rem; border-radius:20px; font-size:0.78rem; font-weight:600; margin-bottom:0.5rem;">
                Overall Compliance Status
            </div>
            <div style="font-size:0.78rem; color:rgba(255,255,255,0.4);">
                📋 Standards: {", ".join(report.get("compliance_standards", []))}
            </div>
        </div>
        <div style="text-align:right; flex-shrink:0;">
            <div style="width:88px; height:88px; border-radius:50%; border:5px solid {sc};
                        display:flex; align-items:center; justify-content:center;
                        background:rgba(0,0,0,0.35);">
                <div style="font-size:1.35rem; font-weight:800; color:{sc};">{score}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric Cards ──
    ppe_data = report.get("ppe_detection", {})
    hazards = report.get("site_hazards", [])
    total_ppe_items = len(ppe_data)
    compliant_ppe_items = sum(1 for p in ppe_data.values() if p.get("compliance") is True)
    critical_hazards = sum(1 for h in hazards if h.get("severity", "").lower() == "critical")
    high_hazards = sum(1 for h in hazards if h.get("severity", "").lower() == "high")

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-value" style="color:{sc};">{score}/100</div>
            <div class="metric-label">Safety Index</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color:#22c55e;">{compliant_ppe_items}/{total_ppe_items}</div>
            <div class="metric-label">Compliant PPE Categories</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color:#fbbf24;">{len(hazards)}</div>
            <div class="metric-label">Identified Hazards</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color:{'#ef4444' if critical_hazards > 0 else '#22c55e'};">{critical_hazards}</div>
            <div class="metric-label">Critical Red Flags</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PPE Detection Checklist ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🦺</div>
        <h3>PPE Detection Checklist</h3>
    </div>
    """, unsafe_allow_html=True)

    ppe_data = report.get("ppe_detection", {})
    for key, ppe in ppe_data.items():
        icon = PPE_ICONS.get(key, "🔧")
        label = PPE_LABELS.get(key, key.replace("_", " ").title())
        item_class = _ppe_item_class(ppe)
        status_pill = _ppe_status_pill(ppe)
        detected = ppe.get("workers_detected", 0)
        compliant = ppe.get("workers_compliant", 0)
        note = ppe.get("note", "")
        st.markdown(f"""
        <div class="ppe-item {item_class}">
            <span class="ppe-icon">{icon}</span>
            <span class="ppe-label">{label}</span>
            <span style="font-size:0.78rem; color:rgba(255,255,255,0.4); margin-right:0.5rem;">
                {compliant}/{detected} workers
            </span>
            {status_pill}
        </div>
        <div style="font-size:0.78rem; color:rgba(255,255,255,0.4); margin: -0.2rem 0 0.6rem 2.2rem; padding-left:0.5rem;">
            {note}
        </div>
        """, unsafe_allow_html=True)

    # ── Site Hazards ──
    hazards = report.get("site_hazards", [])
    if hazards:
        st.markdown(f"""
        <div class="section-header">
            <div class="section-icon">⚠️</div>
            <h3>Identified Site Hazards ({len(hazards)})</h3>
        </div>
        """, unsafe_allow_html=True)

        for h in hazards:
            sev = h.get("severity", "Medium")
            sev_icon = SEV_ICON.get(sev, "🟡")
            sev_color = SEV_COLOR.get(sev, "#fbbf24")
            st.markdown(f"""
            <div class="hazard-card" style="border-left:3px solid {sev_color};">
                <div class="hazard-header">
                    <span class="hazard-title">{sev_icon} {h.get("hazard","")}</span>
                    <span class="sev-{sev.lower()}">{sev}</span>
                </div>
                <div style="font-size:0.78rem; color:rgba(255,255,255,0.4); margin-bottom:0.3rem;">
                    📍 {h.get("location","")}
                </div>
                <div class="hazard-desc">{h.get("description","")}</div>
                <div class="hazard-remedy">
                    🔧 <strong>Remedy:</strong> {h.get("corrective_remedy","")}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Regulatory Flags ──
    flags = report.get("regulatory_flags", [])
    if flags:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📋</div>
            <h3>Regulatory Flags</h3>
        </div>
        """, unsafe_allow_html=True)
        for flag in flags:
            st.markdown(f'<div class="info-box">⚖️ {flag}</div>', unsafe_allow_html=True)

    # ── Executive Summary ──
    summary = report.get("recommendation_summary", "")
    if summary:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📝</div>
            <h3>Executive Recommendation</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="success-box">{summary}</div>', unsafe_allow_html=True)

    # ── Download ──
    st.markdown("---")
    json_str = json.dumps(report, indent=2, ensure_ascii=False)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="⬇️  Download Full JSON Report",
        data=json_str,
        file_name=f"safety_audit_{timestamp}.json",
        mime="application/json",
        use_container_width=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Main render function
# ──────────────────────────────────────────────────────────────────────────────

def render_safety_tab(api_key: Optional[str] = None):
    demo_mode = not api_key

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🦺</div>
        <h3>Site Safety & PPE Compliance Audit — Epic 2</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        Upload a construction site photograph to receive an AI-powered PPE compliance audit
        against <strong>OSHA 29 CFR 1926</strong> and <strong>IS 456:2000</strong> standards.
        Outputs include a structured safety score, PPE checklist, hazard registry, and downloadable JSON report.
    </div>
    """, unsafe_allow_html=True)

    if demo_mode:
        st.markdown("""
        <div class="demo-banner">
            🔮 <strong>Demo Mode Active</strong> — Displaying sample audit data.
            Add your Gemini API key in the sidebar to analyze real site photographs.
        </div>
        """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📸 Upload Construction Site Photo",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supports JPG, PNG, WebP up to 50 MB",
        key="safety_uploader"
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        analyze_btn = st.button(
            "🔍 Run Safety Audit",
            use_container_width=True,
            key="safety_btn",
            type="primary"
        )
    with col2:
        demo_btn = st.button(
            "📋 Load Demo Report",
            use_container_width=True,
            key="safety_demo_btn"
        )

    # Show uploaded image preview
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Site Photo — Ready for Analysis", use_container_width=True)

    # ── Analysis ──
    if analyze_btn:
        if not uploaded_file:
            st.markdown('<div class="warning-box">⚠️ Please upload a construction site photo before running the audit.</div>', unsafe_allow_html=True)
            return

        if demo_mode:
            st.markdown('<div class="warning-box">⚠️ Demo Mode: Connect your Gemini API key to analyze real images. Showing sample report instead.</div>', unsafe_allow_html=True)
            report = get_demo_safety_report()
        else:
            with st.spinner("🔍 Analyzing PPE compliance and site hazards with Gemini Vision..."):
                try:
                    uploaded_file.seek(0)
                    image_bytes = uploaded_file.read()
                    report = analyze_safety(image_bytes, api_key)
                except json.JSONDecodeError as e:
                    st.markdown(f'<div class="danger-box">⚠️ JSON parsing error: {e}. The model returned an unexpected format. Please retry.</div>', unsafe_allow_html=True)
                    return
                except Exception as e:
                    st.markdown(f'<div class="danger-box">⚠️ Analysis error: {e}</div>', unsafe_allow_html=True)
                    return

        st.markdown("---")
        st.markdown("### 📊 Audit Results")
        _render_report(report)

    elif demo_btn:
        report = get_demo_safety_report()
        st.markdown("---")
        st.markdown("### 📊 Demo Audit Report")
        _render_report(report)

