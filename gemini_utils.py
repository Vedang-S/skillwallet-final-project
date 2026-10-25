"""
Multimodal Construction Intelligence Platform
=============================================
Gemini API wrapper — all LLM calls are centralized here.
Falls back gracefully to demo_data fixtures when no API key is provided.
"""

import json, re
from typing import Optional
import google.generativeai as genai
from PIL import Image
import io


def _clean_json(raw: str) -> str:
    """Strip markdown fences and extract pure JSON from model output."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)
    
    # Locate outermost JSON object {...} or array [...]
    obj_start = raw.find("{")
    obj_end = raw.rfind("}")
    arr_start = raw.find("[")
    arr_end = raw.rfind("]")

    if obj_start != -1 and obj_end != -1 and (arr_start == -1 or obj_start < arr_start):
        return raw[obj_start : obj_end + 1].strip()
    elif arr_start != -1 and arr_end != -1:
        return raw[arr_start : arr_end + 1].strip()
    
    return raw.strip()


def configure_gemini(api_key: str):
    """Initialize the Gemini SDK with the provided key."""
    genai.configure(api_key=api_key)


# ─────────────────────────────────────────────────────────────────────────────
# Tab 1 · PPE Safety Audit
# ─────────────────────────────────────────────────────────────────────────────

SAFETY_SYSTEM_PROMPT = """You are a certified Construction Safety Inspector AI with expertise in:
- OSHA 29 CFR Part 1926 (Construction Industry Standards)
- IS 456:2000 and NBC 2016 (Indian Standards)
- PPE compliance assessment
- Hazard identification and risk classification

Analyze the provided construction site image and return ONLY a valid JSON object with NO markdown, NO explanation text — pure JSON only.
"""

SAFETY_USER_PROMPT = """Analyze this construction site image for PPE compliance and site safety hazards.

Return ONLY this exact JSON structure (no markdown fences, no extra text):
{
  "safety_score": <integer 0-100>,
  "overall_status": "<Fully Compliant | High Compliance | Partial Compliance | Non-Compliant | Critical Non-Compliance>",
  "compliance_standards": ["OSHA 29 CFR 1926", "IS 456:2000"],
  "ppe_detection": {
    "hard_hat_helmet": {
      "status": "<Compliant | Non-Compliant | Partial | Not Visible | Not Applicable>",
      "compliance": <true|false>,
      "workers_detected": <int>,
      "workers_compliant": <int>,
      "note": "<specific observation>"
    },
    "high_visibility_vest": {
      "status": "<Compliant | Non-Compliant | Partial | Not Visible | Not Applicable>",
      "compliance": <true|false>,
      "workers_detected": <int>,
      "workers_compliant": <int>,
      "note": "<specific observation>"
    },
    "steel_toe_boots": {
      "status": "<Compliant | Non-Compliant | Partial | Not Visible | Not Applicable>",
      "compliance": <true|false>,
      "workers_detected": <int>,
      "workers_compliant": <int>,
      "note": "<specific observation>"
    },
    "safety_harness": {
      "status": "<Compliant | Non-Compliant | Partial | Not Visible | Not Applicable>",
      "compliance": <true|false>,
      "workers_detected": <int>,
      "workers_compliant": <int>,
      "note": "<specific observation>"
    },
    "safety_goggles": {
      "status": "<Compliant | Non-Compliant | Partial | Not Visible | Not Applicable>",
      "compliance": <true|false>,
      "workers_detected": <int>,
      "workers_compliant": <int>,
      "note": "<specific observation>"
    },
    "gloves": {
      "status": "<Compliant | Non-Compliant | Partial | Not Visible | Not Applicable>",
      "compliance": <true|false>,
      "workers_detected": <int>,
      "workers_compliant": <int>,
      "note": "<specific observation>"
    }
  },
  "site_hazards": [
    {
      "hazard": "<hazard name>",
      "severity": "<Low | Medium | High | Critical>",
      "location": "<location in frame>",
      "description": "<detailed description>",
      "corrective_remedy": "<specific corrective action>"
    }
  ],
  "regulatory_flags": ["<OSHA/IS standard violated>"],
  "audit_timestamp": "<ISO 8601 timestamp>",
  "recommendation_summary": "<2-3 sentence executive summary>"
}"""


def analyze_safety(image_bytes: bytes, api_key: str) -> dict:
    """Call Gemini Vision to analyze PPE and site safety."""
    configure_gemini(api_key)
    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash-lite",
        system_instruction=SAFETY_SYSTEM_PROMPT
    )
    img = Image.open(io.BytesIO(image_bytes))
    response = model.generate_content(
        [SAFETY_USER_PROMPT, img],
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            max_output_tokens=2048,
        )
    )
    raw = response.text
    return json.loads(_clean_json(raw))


# ─────────────────────────────────────────────────────────────────────────────
# Tab 2 · Crack Diagnostics
# ─────────────────────────────────────────────────────────────────────────────

CRACK_SYSTEM_PROMPT = """You are a licensed Structural Engineer AI specializing in:
- Concrete defect classification per IS 456:2000 and ACI 224.1R
- Crack morphology analysis and root-cause investigation
- Structural repair specification (epoxy injection, CFRP, grouting)
- Urgency triage for construction defects

Analyze the provided image and return ONLY a valid JSON object — no markdown, no explanations.
"""

CRACK_USER_PROMPT = """Analyze this image of a concrete/structural surface for cracks and defects.

Return ONLY this exact JSON structure (no markdown fences, no extra text):
{
  "defect_classification": "<Hairline Shrinkage Crack | Settlement Crack | Structural Shear Crack | Thermal Expansion Crack | Spalling & Delamination | Alkali-Silica Reaction | Corrosion-Induced Cracking | No Significant Defect>",
  "crack_type_code": "<HC-01 | SC-02 | SC-03 | TC-04 | SP-05 | ASR-06 | CI-07 | ND-00>",
  "estimated_crack_width_mm": <float>,
  "estimated_crack_length_mm": <float>,
  "crack_depth": "<Superficial | Moderate | Deep | Full Penetration | Unknown>",
  "crack_orientation": "<Horizontal | Vertical | Diagonal | Irregular | Map Cracking>",
  "affected_area_m2": <float>,
  "urgency": "<Immediate | High | Medium | Low | Monitor Only>",
  "urgency_score": <integer 0-100>,
  "root_causes": ["<cause 1>", "<cause 2>"],
  "structural_risk_assessment": {
    "load_bearing_impact": "<None | Negligible | Moderate | High | Severe>",
    "collapse_risk": "<Very Low | Low | Moderate | High | Critical>",
    "water_ingress_risk": "<None | Low | Moderate | High | Critical>",
    "reinforcement_corrosion_risk": "<None | Low | Moderate | High | Critical>"
  },
  "recommended_repairs": [
    {
      "repair_method": "<method name>",
      "description": "<detailed repair procedure>",
      "priority": "<Immediate | Urgent | Routine | Optional | Post-Repair>",
      "estimated_cost_inr": "<cost range>"
    }
  ],
  "compliance_references": ["<IS/ACI/ASTM reference>"],
  "immediate_actions": ["<action 1>", "<action 2>"],
  "monitoring_recommendation": "<monitoring protocol>"
}"""


def analyze_crack(image_bytes: bytes, api_key: str) -> dict:
    """Call Gemini Vision to classify crack defects."""
    configure_gemini(api_key)
    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash-lite",
        system_instruction=CRACK_SYSTEM_PROMPT
    )
    img = Image.open(io.BytesIO(image_bytes))
    response = model.generate_content(
        [CRACK_USER_PROMPT, img],
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            max_output_tokens=2048,
        )
    )
    return json.loads(_clean_json(response.text))


# ─────────────────────────────────────────────────────────────────────────────
# Tab 4 · Chatbot
# ─────────────────────────────────────────────────────────────────────────────

CHAT_SYSTEM_PROMPT = """You are an expert Construction Engineering AI Assistant with deep knowledge of:
- Structural engineering (IS 456, IS 800, IS 1786, IS 1904, IS 2911, IS 13920, IS 1893)
- Construction management and project planning
- Safety standards (OSHA 29 CFR 1926, NBC 2016, IS 3696)
- Material science (concrete, steel, masonry, composites)
- Building codes (NBC 2016, local municipal bylaws)
- Cost estimation, BOQ preparation, and valuation
- Geotechnical engineering fundamentals
- Indian construction industry practices and market rates

Provide accurate, practical, and regulation-compliant answers. Use bullet points and structured formatting.
Always cite relevant IS/OSHA standards. Keep responses concise but comprehensive.
When uncertain, recommend consulting a licensed structural engineer.
"""


def chat_with_assistant(messages: list, api_key: str) -> str:
    """Multi-turn chat with the construction engineering assistant."""
    configure_gemini(api_key)
    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash-lite",
        system_instruction=CHAT_SYSTEM_PROMPT
    )
    # Convert messages to Gemini format
    history = []
    for msg in messages[:-1]:
        history.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [msg["content"]]
        })
    chat = model.start_chat(history=history)
    response = chat.send_message(
        messages[-1]["content"],
        generation_config=genai.types.GenerationConfig(
            temperature=0.4,
            max_output_tokens=1024,
        )
    )
    return response.text

