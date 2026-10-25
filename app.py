"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          MULTIMODAL CONSTRUCTION INTELLIGENCE PLATFORM                     ║
║          Skill Wallet Capstone Project 1                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import os

# ── Page config must be the FIRST Streamlit call ──────────────────────────────
st.set_page_config(
    page_title="Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help":     None,
        "Report a bug": None,
        "About": (
            "**Multimodal Construction Intelligence Platform**\n\n"
            "Skill Wallet Capstone Project 1 · Built with Streamlit & Google Gemini\n\n"
            "Modules: PPE Audit · Crack Diagnostics · Real Estate Valuation · Site Assistant"
        ),
    }
)

# ── Imports (after page config) ───────────────────────────────────────────────
from styles       import APP_CSS
from tab_safety   import render_safety_tab
from tab_crack    import render_crack_tab
from tab_valuation import render_valuation_tab
from tab_assistant import render_assistant_tab

# ── Inject global CSS ─────────────────────────────────────────────────────────
st.markdown(APP_CSS, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════

with st.sidebar:

    # ── Brand Logo ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-logo-icon">🏗️</span>
        <div class="sidebar-logo-title">Construction AI</div>
        <div class="sidebar-logo-text">Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── API Key Input ────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">🔑 Gemini API Key</div>', unsafe_allow_html=True)

    env_key = os.environ.get("GEMINI_API_KEY", "")

    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        value=env_key,
        placeholder="AIza...  (blank = Demo Mode)",
        label_visibility="collapsed",
        help="Free key at https://aistudio.google.com/apikey"
    )

    api_key = api_key_input.strip() if api_key_input.strip() else None

    if api_key:
        if api_key.startswith("AIza") and len(api_key) > 30:
            st.markdown("""
            <div style="background:rgba(34,197,94,0.09); border:1px solid rgba(34,197,94,0.28);
                        border-radius:10px; padding:0.5rem 0.85rem; font-size:0.78rem; color:#22c55e; margin-top:0.4rem;">
                ✅ Connected — Live AI enabled
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(251,191,36,0.09); border:1px solid rgba(251,191,36,0.28);
                        border-radius:10px; padding:0.5rem 0.85rem; font-size:0.78rem; color:#fbbf24; margin-top:0.4rem;">
                ⚠️ Unusual key format — verify if errors occur
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(168,85,247,0.09); border:1px solid rgba(168,85,247,0.28);
                    border-radius:10px; padding:0.5rem 0.85rem; font-size:0.78rem; color:#c084fc; margin-top:0.4rem;">
            🔮 Demo Mode active — sample data shown
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.7rem; color:rgba(255,255,255,0.28); margin-top:0.4rem; line-height:1.5; padding-left:0.2rem;">
        Get a free key at
        <a href="https://aistudio.google.com/apikey" target="_blank"
           style="color:#FF6B35; text-decoration:none;">aistudio.google.com</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Module Navigation ────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">🧭 Modules</div>', unsafe_allow_html=True)

    nav_items = [
        ("🦺", "Site Safety & PPE Audit",       "Epic 2 · Vision AI"),
        ("🔬", "Crack Diagnostics",              "Epic 2 · Structural AI"),
        ("🏙️", "Planning & Valuation",           "Epic 3 · Financial Engine"),
        ("🤖", "Site Assistant & Weather",       "Epic 5 · Chat + Advisory"),
    ]
    for icon, name, sub in nav_items:
        st.markdown(f"""
        <div class="nav-item">
            <div class="nav-item-icon">{icon}</div>
            <div>
                <div style="font-size:0.8rem; color:rgba(255,255,255,0.78); font-weight:500; line-height:1.2;">{name}</div>
                <div style="font-size:0.68rem; color:rgba(255,255,255,0.32); margin-top:0.1rem;">{sub}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Tech Stack ────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">🏛️ Tech Stack</div>', unsafe_allow_html=True)

    arch_items = [
        ("🐍", "Streamlit",        "Web framework"),
        ("🔮", "Gemini 1.5 Flash", "Vision & Language"),
        ("🖼️", "Pillow",           "Image processing"),
        ("🎨", "Pollinations AI",  "3D rendering"),
        ("☁️", "Streamlit Cloud",  "1-click deployment"),
    ]
    for icon, name, desc in arch_items:
        st.markdown(f"""
        <div class="arch-item">
            <span class="arch-item-icon">{icon}</span>
            <div>
                <div style="color:rgba(255,255,255,0.72); font-weight:500;">{name}</div>
                <div style="color:rgba(255,255,255,0.32); font-size:0.68rem;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Standards ─────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">📋 Standards</div>', unsafe_allow_html=True)

    standards_left  = ["IS 456:2000", "IS 13920", "IS 1786", "IS 1904", "IS 3696"]
    standards_right = ["OSHA 29 CFR", "NBC 2016", "ACI 224.1R", "ASTM C881", "EN 1504"]

    for a, b in zip(standards_left, standards_right):
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; padding:0.18rem 0.2rem;
                    border-bottom:1px solid rgba(255,255,255,0.04); font-size:0.7rem; color:rgba(255,255,255,0.42);">
            <span>📌 {a}</span>
            <span>📌 {b}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; font-size:0.68rem; color:rgba(255,255,255,0.22); line-height:1.8; padding-top:0.2rem;">
        <span style="color:rgba(255,107,53,0.5); font-weight:600;">Capstone Project 1</span><br>
        Skill Wallet · 2026
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ════════════════════════════════════════════════════════════════════════════

# ── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Capstone Project 1 · Skill Wallet</div>
    <div class="hero-title">
        Multimodal <span>Construction</span><br>Intelligence Platform
    </div>
    <div class="hero-subtitle">
        AI-powered site safety auditing &nbsp;·&nbsp; Structural crack diagnostics &nbsp;·&nbsp;
        Real estate valuation &nbsp;·&nbsp; Weather-aware advisory &nbsp;·&nbsp; Engineering assistant
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stat Row (3 pills — AI Model box removed) ─────────────────────────────────
mode_color = "#22c55e" if api_key else "#a855f7"
mode_label = "⚡ Live AI Mode" if api_key else "🔮 Demo Mode"

st.markdown(f"""
<div class="stat-row">
    <div class="stat-pill">
        <div class="stat-pill-label">Status</div>
        <div class="stat-pill-value" style="color:{mode_color};">{mode_label}</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-label">Active Modules</div>
        <div class="stat-pill-value" style="color:#60a5fa;">4 Modules</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-label">Standards</div>
        <div class="stat-pill-value" style="color:#c084fc;">IS · OSHA · ACI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Main Tabs ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺  Site Safety & PPE",
    "🔬  Crack Diagnostics",
    "🏙️  Valuation & Planning",
    "🤖  Site Assistant",
])

with tab1:
    render_safety_tab(api_key=api_key)

with tab2:
    render_crack_tab(api_key=api_key)

with tab3:
    render_valuation_tab(api_key=api_key)

with tab4:
    render_assistant_tab(api_key=api_key)
