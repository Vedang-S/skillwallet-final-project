"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
============================================
Modular styles and CSS constants.
"""

APP_CSS = """
<style>
/* ─── Global Reset & Base ─── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ─── Hide Streamlit Branding ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ─── App Background ─── */
.stApp {
    background: linear-gradient(135deg, #0a0d14 0%, #0e1117 50%, #111622 100%);
    min-height: 100vh;
}

/* ─── Main content padding ─── */
.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px;
}

/* ─── Hero Banner ─── */
.hero-banner {
    background: linear-gradient(135deg, #1a1d2e 0%, #16213e 40%, #0f3460 100%);
    border: 1px solid rgba(255, 107, 53, 0.3);
    border-radius: 20px;
    padding: 2.4rem 3rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255,107,53,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -60%; left: -5%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.hero-title span { color: #FF6B35; }
.hero-subtitle {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.5);
    font-weight: 400;
    letter-spacing: 0.02em;
    line-height: 1.6;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,107,53,0.15);
    border: 1px solid rgba(255,107,53,0.4);
    color: #FF6B35;
    padding: 0.25rem 0.85rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.9rem;
}

/* ─── Metric Cards ─── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 1.4rem 0;
}
.metric-card {
    background: linear-gradient(135deg, #1e2130 0%, #252840 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.metric-card:hover {
    transform: translateY(-3px);
    border-color: rgba(255,107,53,0.35);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #FF6B35, #ff9a6c);
    border-radius: 0 0 16px 16px;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #FF6B35;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.metric-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.45);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* ─── Status Pills ─── */
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.pill-safe    { background: rgba(34,197,94,0.15);  border: 1px solid rgba(34,197,94,0.4);  color: #22c55e; }
.pill-warning { background: rgba(251,191,36,0.15); border: 1px solid rgba(251,191,36,0.4); color: #fbbf24; }
.pill-danger  { background: rgba(239,68,68,0.15);  border: 1px solid rgba(239,68,68,0.4);  color: #ef4444; }
.pill-info    { background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.4); color: #3b82f6; }
.pill-critical{ background: rgba(168,85,247,0.15); border: 1px solid rgba(168,85,247,0.4); color: #a855f7; }

/* ─── Section Headers ─── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.8rem 0 1.1rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.section-header h3 {
    font-size: 1.05rem;
    font-weight: 600;
    color: #ffffff;
}
.section-icon {
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg, #FF6B35, #ff9a6c);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(255,107,53,0.25);
}

/* ─── Info / Alert Boxes ─── */
.info-box {
    background: rgba(59,130,246,0.07);
    border: 1px solid rgba(59,130,246,0.22);
    border-left: 4px solid #3b82f6;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.9rem 0;
    font-size: 0.875rem;
    color: rgba(255,255,255,0.8);
    line-height: 1.6;
}
.warning-box {
    background: rgba(251,191,36,0.07);
    border: 1px solid rgba(251,191,36,0.22);
    border-left: 4px solid #fbbf24;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.9rem 0;
    font-size: 0.875rem;
    color: rgba(255,255,255,0.8);
    line-height: 1.6;
}
.danger-box {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.22);
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.9rem 0;
    font-size: 0.875rem;
    color: rgba(255,255,255,0.8);
    line-height: 1.6;
}
.success-box {
    background: rgba(34,197,94,0.07);
    border: 1px solid rgba(34,197,94,0.22);
    border-left: 4px solid #22c55e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.9rem 0;
    font-size: 0.875rem;
    color: rgba(255,255,255,0.8);
    line-height: 1.6;
}

/* ─── PPE Checklist Items ─── */
.ppe-item {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding: 0.8rem 1.1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    margin-bottom: 0.5rem;
    font-size: 0.88rem;
    transition: background 0.15s;
}
.ppe-item:hover { background: rgba(255,255,255,0.05); }
.ppe-item .ppe-icon { font-size: 1.2rem; }
.ppe-item .ppe-label { flex: 1; color: rgba(255,255,255,0.8); font-weight: 500; }
.ppe-compliant { border-left: 3px solid #22c55e; }
.ppe-violation { border-left: 3px solid #ef4444; }
.ppe-partial   { border-left: 3px solid #fbbf24; }

/* ─── Hazard Cards ─── */
.hazard-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.hazard-card:hover {
    border-color: rgba(255,107,53,0.3);
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}
.hazard-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}
.hazard-title { font-size: 0.92rem; font-weight: 600; color: #ffffff; }
.hazard-desc  { font-size: 0.83rem; color: rgba(255,255,255,0.55); line-height: 1.5; }
.hazard-remedy {
    margin-top: 0.6rem;
    padding: 0.45rem 0.8rem;
    background: rgba(255,107,53,0.08);
    border-radius: 8px;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.65);
}

/* ─── Severity Badges ─── */
.sev-low      { background: rgba(34,197,94,0.15);  color: #22c55e;  padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.sev-medium   { background: rgba(251,191,36,0.15); color: #fbbf24; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.sev-high     { background: rgba(249,115,22,0.15); color: #f97316; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.sev-critical { background: rgba(239,68,68,0.15);  color: #ef4444; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }

/* ─── Crack Diagnosis ─── */
.crack-result-card {
    background: linear-gradient(135deg, #1a1d2e 0%, #16213e 100%);
    border: 1px solid rgba(255,107,53,0.2);
    border-radius: 18px;
    padding: 1.8rem;
    margin: 1rem 0;
}
.crack-type-badge {
    display: inline-block;
    background: linear-gradient(135deg, #FF6B35, #ff9a6c);
    color: white;
    padding: 0.4rem 1.2rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: 0.04em;
}

/* ─── Valuation Cards ─── */
.valuation-card {
    background: linear-gradient(135deg, #1a2744, #0f1e3c);
    border: 1px solid rgba(59,130,246,0.22);
    border-radius: 18px;
    padding: 1.6rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s;
}
.valuation-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
.valuation-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #60a5fa);
}
.valuation-amount {
    font-size: 2rem;
    font-weight: 700;
    color: #60a5fa;
    line-height: 1;
}
.valuation-unit {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.45);
    margin-top: 0.3rem;
}

/* ─── Weather Alert Banners ─── */
.weather-alert {
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin: 0.8rem 0;
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    font-size: 0.875rem;
    line-height: 1.55;
}
.weather-alert-icon { font-size: 1.5rem; flex-shrink: 0; padding-top: 0.1rem; }
.weather-alert-content { flex: 1; }
.weather-alert-title { font-weight: 700; margin-bottom: 0.3rem; }
.alert-wind     { background: rgba(59,130,246,0.1);  border: 1px solid rgba(59,130,246,0.28);  color: #93c5fd; }
.alert-rain     { background: rgba(34,211,238,0.09);  border: 1px solid rgba(34,211,238,0.28);  color: #67e8f9; }
.alert-heat     { background: rgba(251,191,36,0.09);  border: 1px solid rgba(251,191,36,0.28);  color: #fde68a; }
.alert-normal   { background: rgba(34,197,94,0.09);   border: 1px solid rgba(34,197,94,0.28);   color: #86efac; }
.alert-critical { background: rgba(239,68,68,0.1);    border: 1px solid rgba(239,68,68,0.28);   color: #fca5a5; }

/* ─── Chat Interface ─── */
.chat-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.4rem;
    max-height: 500px;
    overflow-y: auto;
    margin-bottom: 1rem;
}
.chat-msg {
    display: flex;
    gap: 0.85rem;
    margin-bottom: 1.1rem;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.chat-avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.avatar-user { background: linear-gradient(135deg, #FF6B35, #ff9a6c); }
.avatar-bot  { background: linear-gradient(135deg, #3b82f6, #60a5fa); }
.chat-bubble {
    flex: 1;
    padding: 0.8rem 1.1rem;
    border-radius: 14px;
    font-size: 0.875rem;
    line-height: 1.6;
    max-width: 85%;
}
.bubble-user {
    background: rgba(255,107,53,0.1);
    border: 1px solid rgba(255,107,53,0.2);
    color: rgba(255,255,255,0.85);
    align-self: flex-end;
    margin-left: auto;
    border-bottom-right-radius: 4px;
}
.bubble-bot {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.18);
    color: rgba(255,255,255,0.85);
    border-bottom-left-radius: 4px;
}

/* ─── Progress / Milestone Bar ─── */
.milestone-bar-wrapper {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    overflow: hidden;
    height: 16px;
    margin: 0.4rem 0 0.2rem;
}
.milestone-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #FF6B35, #ff9a6c);
    border-radius: 10px;
    transition: width 0.8s ease;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 8px;
    font-size: 0.7rem;
    font-weight: 700;
    color: white;
}

/* ─── Rendering Card ─── */
.render-card {
    background: linear-gradient(135deg, #1a1d2e, #111622);
    border: 1px solid rgba(168,85,247,0.22);
    border-radius: 18px;
    padding: 1.6rem;
    text-align: center;
}
.render-placeholder {
    background: rgba(168,85,247,0.05);
    border: 2px dashed rgba(168,85,247,0.28);
    border-radius: 12px;
    padding: 2.5rem;
    color: rgba(255,255,255,0.4);
    font-size: 0.88rem;
    line-height: 1.6;
}

/* ─── Sidebar Styles ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #111622 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.2rem 2rem;
}
.sidebar-logo {
    text-align: center;
    padding: 0.5rem 0 1.2rem;
}
.sidebar-logo-icon {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 0.4rem;
    filter: drop-shadow(0 2px 8px rgba(255,107,53,0.3));
}
.sidebar-logo-title {
    font-size: 1rem;
    font-weight: 700;
    color: #FF6B35;
    margin-bottom: 0.1rem;
    letter-spacing: -0.01em;
}
.sidebar-logo-text {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
.sidebar-section-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.6rem;
    margin-top: 0.2rem;
    padding-left: 0.3rem;
}
.nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.65rem 0.9rem;
    border-radius: 10px;
    margin-bottom: 0.25rem;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.6);
    background: transparent;
    cursor: default;
    transition: background 0.2s, color 0.2s;
}
.nav-item:hover { background: rgba(255,107,53,0.09); color: rgba(255,255,255,0.9); }
.nav-item-icon {
    width: 28px; height: 28px;
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem;
    flex-shrink: 0;
}
.arch-item {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.45rem 0.3rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.78rem;
}
.arch-item-icon {
    font-size: 1.1rem;
    flex-shrink: 0;
    width: 24px;
    text-align: center;
}

/* ─── Tab Overrides ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;
    background: rgba(255,255,255,0.03);
    border-radius: 14px;
    padding: 0.45rem;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: rgba(255,255,255,0.5);
    background: transparent;
    border: none;
    transition: all 0.2s;
}
.stTabs [data-baseweb="tab"]:hover {
    color: rgba(255,255,255,0.8);
    background: rgba(255,255,255,0.04);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B35, #ff9a6c) !important;
    color: white !important;
    font-weight: 600;
    box-shadow: 0 2px 10px rgba(255,107,53,0.3);
}

/* ─── Streamlit Widget Tweaks ─── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #fafafa !important;
    border-radius: 10px !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(255,107,53,0.5) !important;
    box-shadow: 0 0 0 2px rgba(255,107,53,0.1) !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #FF6B35, #ff9a6c) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #FF6B35, #ff9a6c);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 1.5rem;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(255,107,53,0.2);
}
.stButton > button:hover {
    opacity: 0.92;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(255,107,53,0.3);
}
.stButton > button:active { transform: translateY(0); }
.stFileUploader {
    background: rgba(255,255,255,0.02);
    border: 2px dashed rgba(255,107,53,0.3);
    border-radius: 14px;
    padding: 0.5rem;
    transition: border-color 0.2s;
}
.stFileUploader:hover { border-color: rgba(255,107,53,0.55); }
.stDownloadButton > button {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.38);
    color: #22c55e;
    border-radius: 10px;
    font-weight: 600;
}
.stDownloadButton > button:hover {
    background: rgba(34,197,94,0.2);
    box-shadow: 0 4px 12px rgba(34,197,94,0.2);
}
.element-container { animation: fadeIn 0.25s ease; }

/* ─── Dividers ─── */
hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.2rem 0 !important; }

/* ─── JSON Code Block ─── */
.json-block {
    background: #0d1117;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #e2e8f0;
    overflow-x: auto;
    line-height: 1.6;
    max-height: 350px;
    overflow-y: auto;
}

/* ─── Demo Mode Banner ─── */
.demo-banner {
    background: linear-gradient(135deg, rgba(168,85,247,0.1), rgba(139,92,246,0.07));
    border: 1px solid rgba(168,85,247,0.28);
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.7);
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

/* ─── Stat Indicator Row ─── */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.stat-pill {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 0.75rem 1rem;
    text-align: center;
    transition: border-color 0.2s;
}
.stat-pill:hover { border-color: rgba(255,107,53,0.2); }
.stat-pill-label {
    font-size: 0.68rem;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 0.2rem;
}
.stat-pill-value {
    font-size: 0.88rem;
    font-weight: 700;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,107,53,0.28); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,107,53,0.5); }

/* ─── Expander tweaks ─── */
.streamlit-expanderHeader {
    border-radius: 10px !important;
    background: rgba(255,255,255,0.03) !important;
}
details > summary { border-radius: 10px !important; }
</style>
"""
