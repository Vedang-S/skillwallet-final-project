"""
Multimodal Construction Intelligence Platform
=============================================
Tab 4 · Daily Site Assistant & Weather-Aware Advisory
Epic 5 — Weather alerts + multi-turn construction engineering chatbot.
"""

import streamlit as st
from typing import Optional
from gemini_utils import chat_with_assistant
from demo_data import get_demo_chat_response
import datetime

# ──────────────────────────────────────────────────────────────────────────────
# Weather Alert Configurations
# ──────────────────────────────────────────────────────────────────────────────

WEATHER_CONFIGS = {
    "☀️ Normal / Clear": {
        "code": "normal",
        "icon": "☀️",
        "banner_class": "alert-normal",
        "banner_icon": "☀️",
        "banner_title": "Normal Operating Conditions",
        "banner_msg": "Standard site safety protocols apply. Maintain PPE compliance and regular toolbox talks.",
        "alerts": [
            {
                "icon": "✅",
                "title": "All Operations Permitted",
                "msg": "No weather-related restrictions. Ensure standard IS 456 curing protocols for concrete pours. Maintain hydration stations for workers.",
                "class": "alert-normal"
            },
            {
                "icon": "🌡️",
                "title": "Routine Heat Management",
                "msg": "Monitor ambient temperature. Avoid concrete pours during peak heat (12 PM–4 PM) if temp exceeds 35°C. Provide ORS sachets and water at work stations.",
                "class": "alert-normal"
            },
            {
                "icon": "📋",
                "title": "Daily Checklist Active",
                "msg": "Conduct morning toolbox talk. Inspect scaffolding, electrical connections, and PPE compliance. Log site diary as per IS 4656 requirements.",
                "class": "alert-normal"
            }
        ],
        "suspended_ops": [],
        "crane_permitted": True,
        "concrete_pour": "Permitted with standard protocols",
        "electrical_ops": "Permitted",
        "height_work": "Permitted with standard fall protection",
    },
    "💨 High Wind (>50 km/h)": {
        "code": "wind",
        "icon": "💨",
        "banner_class": "alert-wind",
        "banner_icon": "💨",
        "banner_title": "HIGH WIND ADVISORY ACTIVE",
        "banner_msg": "Wind speeds exceeding 50 km/h recorded. Multiple site operations must be suspended per OSHA 1926.502 and IS 3696.",
        "alerts": [
            {
                "icon": "🏗️",
                "title": "SUSPEND: All Crane & Lifting Operations",
                "msg": "Immediately cease all crane lifts, hoist operations, and material hoisting. Per OSHA 1926.1417 and IS 3938, crane operations must stop when wind exceeds 50 km/h (or manufacturer's rated limit, whichever is lower). Lower all suspended loads safely to ground. Lock crane slewing mechanism.",
                "class": "alert-critical"
            },
            {
                "icon": "🪟",
                "title": "SUSPEND: Facade Glazing & Cladding Work",
                "msg": "Halt all glass panel installations, curtain wall work, and large panel cladding. Wind forces can cause panel instability and catastrophic failure.",
                "class": "alert-critical"
            },
            {
                "icon": "🪜",
                "title": "RESTRICT: Scaffolding & Elevated Work",
                "msg": "Evacuate all workers from open scaffolding above 6 m. Inspect all scaffold tie-backs and bracing. Secure all loose material (formwork panels, debris nets, tool bags) with storm clips.",
                "class": "alert-wind"
            },
            {
                "icon": "🧱",
                "title": "SUSPEND: Masonry & Plastering",
                "msg": "Cease masonry work and external plastering. Wind will cause rapid moisture loss from fresh mortar, compromising bond strength. Cover completed masonry with polythene sheeting.",
                "class": "alert-wind"
            },
            {
                "icon": "⚡",
                "title": "CAUTION: Electrical Hazard — Flying Debris",
                "msg": "Secure temporary electrical cables and distribution boards. Flying debris can damage insulation and create electrocution risk. Inspect all GFCI units before resuming operations.",
                "class": "alert-wind"
            },
            {
                "icon": "🔄",
                "title": "Permitted Operations",
                "msg": "Interior structural work, underground works, MEP installation in enclosed areas, and finishing work inside completed floors may continue with enhanced fall protection.",
                "class": "alert-normal"
            }
        ],
        "suspended_ops": ["Crane lifts", "Hoist operations", "Facade glazing", "External scaffolding > 6m", "External masonry", "Formwork striking"],
        "crane_permitted": False,
        "concrete_pour": "Suspended — wind causes rapid evaporation and plastic shrinkage cracking",
        "electrical_ops": "Restricted — inspect GFCI; secure all temporary power cables",
        "height_work": "Suspended for open scaffolding above 6 m",
    },
    "🌧️ Heavy Rain / Monsoon": {
        "code": "rain",
        "icon": "🌧️",
        "banner_class": "alert-rain",
        "banner_icon": "🌧️",
        "banner_title": "HEAVY RAIN / MONSOON PROTOCOL",
        "banner_msg": "Heavy rainfall conditions active. Electrical hazard and foundation/slope stability are primary risks. Implement monsoon safety protocol per NBC 2016.",
        "alerts": [
            {
                "icon": "⚡",
                "title": "CRITICAL: Electrical Hazard Mitigation",
                "msg": "Immediately cover all temporary electrical panels, distribution boards, and extension boxes with waterproof enclosures. All site electrical circuits must route through GFCI/ELCB (30 mA trip). Shut down non-essential temporary power. No electrical work in waterlogged areas. Prohibition on using electrical tools near standing water.",
                "class": "alert-critical"
            },
            {
                "icon": "🚧",
                "title": "SUSPEND: Excavation & Foundation Work",
                "msg": "Halt open excavation, trenching, and pile boring in active rainfall. Risk of wall collapse, slurry failure, and equipment entrapment. Pump out accumulated water before resuming. Inspect existing shoring and sloping for stability after rain.",
                "class": "alert-rain"
            },
            {
                "icon": "🏗️",
                "title": "RESTRICT: Concrete Pouring Operations",
                "msg": "Avoid fresh concrete pours during active rainfall (rain dilutes water-cement ratio, causing strength loss). If pour is in progress, cover immediately with tarpaulins. Post-rain: test in-situ slump before resuming. Rainwater on fresh concrete surface to be removed before finishing.",
                "class": "alert-rain"
            },
            {
                "icon": "🪖",
                "title": "Enhanced PPE Requirement",
                "msg": "All workers must wear rubber-soled non-slip boots, waterproof rain suits, and insulated gloves for any electrical area proximity. High-vis vests must be waterproof Class 2 or above.",
                "class": "alert-rain"
            },
            {
                "icon": "🏚️",
                "title": "Structural Formwork Monitoring",
                "msg": "Inspect all formwork props and centering for settlement or displacement under wet soil conditions. Waterlogged soil reduces bearing capacity. Do NOT strike formwork during heavy rain period.",
                "class": "alert-rain"
            },
            {
                "icon": "🛡️",
                "title": "Monsoon Concrete Curing Protocol",
                "msg": "Rain acts as curing water — monitor for excessive water on surface. Use HRWR admixtures for rain-season pours. Ensure drainage slopes on slabs. Test cubes at 3, 7, and 28 days per IS 516.",
                "class": "alert-normal"
            }
        ],
        "suspended_ops": ["Open excavation", "Foundation boring in rain", "Exposed electrical work", "Surface blasting", "External painting"],
        "crane_permitted": True,
        "concrete_pour": "Restricted — cover in-progress pours; avoid fresh pours in downpour",
        "electrical_ops": "CRITICAL RESTRICTION — GFCI/ELCB mandatory; waterproof all panels",
        "height_work": "Restricted — non-slip surfaces required; inspect scaffolding for stability",
    },
    "🌡️ Extreme Heat (>42°C)": {
        "code": "heat",
        "icon": "🌡️",
        "banner_class": "alert-heat",
        "banner_icon": "🌡️",
        "banner_title": "EXTREME HEAT ADVISORY — >42°C",
        "banner_msg": "Ambient temperature exceeding 42°C. Worker heat stress risk is CRITICAL. Mandatory heat protection protocol per OSHA Heat Illness Prevention Standard.",
        "alerts": [
            {
                "icon": "🚑",
                "title": "MANDATORY: Worker Heat Stress Protocol",
                "msg": "Implement mandatory water-rest-shade schedule: 1 cup water every 20 minutes; 10-minute shade break every 2 hours. Designate shaded rest zones. Assign heat illness observer on each crew. At 44°C, consider complete work stoppage per OSHA Heat Illness Prevention guidelines.",
                "class": "alert-critical"
            },
            {
                "icon": "🧱",
                "title": "RESTRICT: Concrete Curing Protocol",
                "msg": "Extreme heat accelerates concrete hydration — risk of plastic shrinkage cracking and reduced 28-day strength. Apply wet burlap + polythene curing within 30 minutes of finishing. Increase curing frequency to 4× per day. Consider night pours for critical structural elements. Pre-cool aggregates and mix water (target mix temp <30°C per ACI 305R).",
                "class": "alert-heat"
            },
            {
                "icon": "⚡",
                "title": "CAUTION: Electrical Equipment Overheating",
                "msg": "Check all temporary generator sets, transformers, and distribution panels for overheating. Ensure ventilation clearances. Reduce load on temporary panels by 20%. Do not run cables in direct sunlight without UV-resistant conduit.",
                "class": "alert-heat"
            },
            {
                "icon": "🪜",
                "title": "RESTRICT: Height & Confined Space Work",
                "msg": "Elevated platform work increases heat exposure 3–5°C above ambient. Limit height work to before 10 AM and after 5 PM. Mandatory 30-min shade breaks every 45 minutes for elevated workers. Check for heat exhaustion symptoms (dizziness, nausea, confusion).",
                "class": "alert-heat"
            },
            {
                "icon": "🔩",
                "title": "Steel & Formwork Thermal Expansion",
                "msg": "Steel members expand significantly at 42°C+. Account for thermal movement in expansion joints. Do not fix formwork props with reduced clearance — allow 2–3mm thermal gap. Check pre-stressed elements for increased prestress losses.",
                "class": "alert-heat"
            },
            {
                "icon": "💧",
                "title": "Site Hydration & Medical Preparedness",
                "msg": "Ensure minimum 4 L of cold water per worker per shift. Stock ORS (Oral Rehydration Salts) at all hydration points. First aid kit with ice packs at site office. Emergency contact for nearest hospital on site noticeboard. Assign 1 trained first-aider per 25 workers.",
                "class": "alert-heat"
            }
        ],
        "suspended_ops": ["Mid-day concrete pours (11 AM–4 PM)", "Confined space hot work", "Roofing in full sun", "Asphalt laying in peak heat"],
        "crane_permitted": True,
        "concrete_pour": "Restricted — night/early morning pours recommended; pre-cool mix",
        "electrical_ops": "Caution — check for overheating; derate panel loads by 20%",
        "height_work": "Restricted — time-limited sessions with mandatory breaks",
    },
    "⛈️ Thunderstorm / Lightning": {
        "code": "thunder",
        "icon": "⛈️",
        "banner_class": "alert-critical",
        "banner_icon": "⛈️",
        "banner_title": "THUNDERSTORM ALERT — EVACUATE ELEVATED POSITIONS",
        "banner_msg": "Active lightning risk detected. ALL elevated work must be suspended immediately. Ground all personnel to shelter.",
        "alerts": [
            {
                "icon": "⚡",
                "title": "IMMEDIATE: Evacuate All Elevated Workers",
                "msg": "Lightning strike risk is CRITICAL for workers on scaffolding, cranes, rooftops, and steel frames. Immediately evacuate all workers above 3 m to ground level. This is a life-safety emergency — no exceptions.",
                "class": "alert-critical"
            },
            {
                "icon": "🏗️",
                "title": "SUSPEND: All Crane Operations — Ground Immediately",
                "msg": "Crane is the highest lightning conductor on site. Lower all loads, lower the jib to minimum height, and activate lightning protection ground connection. Operator to leave cab immediately after safe grounding.",
                "class": "alert-critical"
            },
            {
                "icon": "🔌",
                "title": "ISOLATE: All Site Electrical Power",
                "msg": "Shut down all temporary site power at main distribution board. Disconnect tower crane and hoist power. Risk of surge and ground fault from lightning strike. Do not reconnect until lightning risk has passed (30 minutes after last thunder clap).",
                "class": "alert-critical"
            },
            {
                "icon": "🏠",
                "title": "Sheltering Protocol",
                "msg": "All workers to shelter inside a solid building or hard-top vehicle. Avoid open canopies, tents, and lean-to shelters. Stay away from metal structures, rebars, and tall trees. Wait minimum 30 minutes after last thunder/lightning before resuming.",
                "class": "alert-heat"
            }
        ],
        "suspended_ops": ["ALL elevated work", "All crane operations", "All site electrical", "All outdoor operations"],
        "crane_permitted": False,
        "concrete_pour": "Suspended — personnel safety priority",
        "electrical_ops": "ISOLATED — shut down all site power at MDB",
        "height_work": "SUSPENDED — immediate evacuation required",
    },
}

QUICK_PROMPTS = [
    "What is the minimum curing period for M25 concrete as per IS 456?",
    "How do I calculate safe bearing capacity of soil on site?",
    "What is the stirrup spacing formula for a shear-critical beam?",
    "Explain the OSHA requirements for scaffold safety in construction.",
    "What are the IS 1786 requirements for Fe 500D rebar?",
    "How to estimate project cost for a 5-storey RCC building in Bangalore?",
    "What are the BIS standards for concrete mix design?",
    "Explain the difference between M20, M25, and M30 concrete grades.",
]


def render_assistant_tab(api_key: Optional[str] = None):
    demo_mode = not api_key

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🤖</div>
        <h3>Daily Site Assistant & Weather-Aware Advisory — Epic 5</h3>
    </div>
    """, unsafe_allow_html=True)

    # ── WEATHER ADVISORY SECTION ──────────────────────────────────────────────
    st.markdown("### 🌤️ Weather Condition & Site Advisory")

    weather_choice = st.selectbox(
        "📡 Current Weather Condition at Site",
        list(WEATHER_CONFIGS.keys()),
        key="weather_select"
    )

    cfg = WEATHER_CONFIGS[weather_choice]

    # Banner
    banner_cls = cfg["banner_class"]
    st.markdown(f"""
    <div class="weather-alert {banner_cls}" style="margin-bottom:1rem;">
        <div class="weather-alert-icon">{cfg['banner_icon']}</div>
        <div class="weather-alert-content">
            <div class="weather-alert-title">{cfg['banner_title']}</div>
            {cfg['banner_msg']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Status Row
    col1, col2, col3, col4 = st.columns(4)
    statuses = [
        (col1, "🏗️ Crane Ops",     "Permitted ✓" if cfg["crane_permitted"] else "SUSPENDED ✗",
         "#22c55e" if cfg["crane_permitted"] else "#ef4444"),
        (col2, "🪨 Concrete Pour", cfg["concrete_pour"][:25] + "...",
         "#22c55e" if "Permitted" in cfg["concrete_pour"] else "#fbbf24" if "Restricted" in cfg["concrete_pour"] else "#ef4444"),
        (col3, "⚡ Electrical",    cfg["electrical_ops"][:25] + "...",
         "#22c55e" if "Permitted" in cfg["electrical_ops"] else "#fbbf24" if "Restricted" in cfg["electrical_ops"] or "Caution" in cfg["electrical_ops"] else "#ef4444"),
        (col4, "🪜 Height Work",   cfg["height_work"][:25] + "...",
         "#22c55e" if "Permitted" in cfg["height_work"] else "#fbbf24" if "Restricted" in cfg["height_work"] else "#ef4444"),
    ]
    for col, label, value, color in statuses:
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
                        border-radius:10px; padding:0.7rem; text-align:center; margin-bottom:0.5rem;">
                <div style="font-size:0.72rem; color:rgba(255,255,255,0.4); margin-bottom:0.2rem;">{label}</div>
                <div style="font-size:0.78rem; font-weight:700; color:{color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    # Suspended Operations
    if cfg["suspended_ops"]:
        susp_items = " &nbsp;·&nbsp; ".join([f"<strong>{op}</strong>" for op in cfg["suspended_ops"]])
        st.markdown(f"""
        <div class="danger-box">
            🚫 <strong>Suspended Operations:</strong> {susp_items}
        </div>
        """, unsafe_allow_html=True)

    # Detailed Alerts
    with st.expander("📋 View Detailed Weather Safety Protocols", expanded=True):
        for alert in cfg["alerts"]:
            st.markdown(f"""
            <div class="weather-alert {alert['class']}" style="margin-bottom:0.7rem;">
                <div class="weather-alert-icon">{alert['icon']}</div>
                <div class="weather-alert-content">
                    <div class="weather-alert-title">{alert['title']}</div>
                    {alert['msg']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── CHATBOT SECTION ───────────────────────────────────────────────────────
    st.markdown("### 🤖 Construction Engineering Assistant")

    if demo_mode:
        st.markdown("""
        <div class="demo-banner">
            🔮 <strong>Demo Mode Active</strong> — Showing pre-programmed responses.
            Add your Gemini API key in the sidebar to enable full AI chat capabilities.
        </div>
        """, unsafe_allow_html=True)

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello! I'm your **Construction Engineering AI Assistant** — powered by Gemini.\n\n"
                    "I specialize in:\n"
                    "- **Structural design** (IS 456, IS 800, IS 13920)\n"
                    "- **Safety protocols** (OSHA, NBC 2016)\n"
                    "- **Material specifications** & quality control\n"
                    "- **Cost estimation** & BOQ preparation\n"
                    "- **Foundation design** & soil mechanics\n\n"
                    "Ask me anything about your construction project! 🏗️"
                )
            }
        ]

    # Quick Prompt Buttons
    st.markdown("<div style='font-size:0.8rem; color:rgba(255,255,255,0.4); margin-bottom:0.5rem;'>💡 Quick prompts:</div>", unsafe_allow_html=True)
    qp_cols = st.columns(4)
    for i, qp in enumerate(QUICK_PROMPTS[:4]):
        with qp_cols[i]:
            if st.button(f"💬 {qp[:35]}...", key=f"qp_{i}", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": qp})
                with st.spinner("🤔 Thinking..."):
                    try:
                        if demo_mode:
                            reply = get_demo_chat_response(qp)
                        else:
                            reply = chat_with_assistant(st.session_state.chat_messages, api_key)
                    except Exception as e:
                        reply = f"⚠️ Error: {e}. Please check your API key and retry."
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()

    # Chat Display
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div class="chat-msg" style="flex-direction:row-reverse;">
                <div class="chat-avatar avatar-user">👤</div>
                <div class="chat-bubble bubble-user">{msg['content'].replace(chr(10), '<br>')}</div>
            </div>"""
        else:
            content = msg['content'].replace("**", "<strong>", 1)
            # Simple bold replacement (pairs of **)
            import re
            content_rendered = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', msg['content'])
            content_rendered = content_rendered.replace("\n", "<br>")
            chat_html += f"""
            <div class="chat-msg">
                <div class="chat-avatar avatar-bot">🤖</div>
                <div class="chat-bubble bubble-bot">{content_rendered}</div>
            </div>"""
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input Form (supports Enter key and button click)
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "Message",
                placeholder="Ask about concrete design, safety protocols, cost estimates... (Press Enter to send)",
                key="chat_input_text",
                label_visibility="collapsed"
            )
        with col_send:
            send_btn = st.form_submit_button("Send ➤", use_container_width=True, type="primary")

    col_dummy, col_clear = st.columns([5, 1])
    with col_clear:
        clear_btn = st.button("🗑️ Clear Chat", use_container_width=True, key="chat_clear")

    if clear_btn:
        st.session_state.chat_messages = [st.session_state.chat_messages[0]]  # Keep system greeting
        st.rerun()

    if send_btn and user_input.strip():
        st.session_state.chat_messages.append({"role": "user", "content": user_input.strip()})
        with st.spinner("🤔 Generating response..."):
            try:
                if demo_mode:
                    reply = get_demo_chat_response(user_input)
                else:
                    reply = chat_with_assistant(st.session_state.chat_messages, api_key)
            except Exception as e:
                reply = f"⚠️ Error communicating with Gemini: {e}. Please verify your API key."
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    # Status info
    st.markdown(f"""
    <div style="font-size:0.75rem; color:rgba(255,255,255,0.3); text-align:center; margin-top:0.5rem;">
        💬 {len(st.session_state.chat_messages)} messages &nbsp;·&nbsp;
        Model: {'Gemini 1.5 Flash' if not demo_mode else 'Demo Mode'} &nbsp;·&nbsp;
        Session: {datetime.datetime.now().strftime('%H:%M IST')}
    </div>
    """, unsafe_allow_html=True)

