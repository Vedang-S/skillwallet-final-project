"""
Multimodal Construction Intelligence Platform
=============================================
Demo / fallback data module — used when no Gemini API key is provided.
All fixtures mirror the exact JSON schemas that the real Gemini responses produce.
"""

import json, random

# ─────────────────────────────────────────────────────────────────────────────
# Tab 1 · Safety & PPE Audit
# ─────────────────────────────────────────────────────────────────────────────

DEMO_SAFETY_REPORTS = [
    {
        "safety_score": 72,
        "overall_status": "Partial Compliance",
        "compliance_standards": ["OSHA 29 CFR 1926", "IS 456:2000"],
        "ppe_detection": {
            "hard_hat_helmet": {"status": "Compliant", "compliance": True, "workers_detected": 4, "workers_compliant": 4, "note": "All workers wearing IS 4151 certified hard hats"},
            "high_visibility_vest": {"status": "Partial", "compliance": False, "workers_detected": 4, "workers_compliant": 2, "note": "2 of 4 workers lack high-vis vests — OSHA 1926.67 violation"},
            "steel_toe_boots": {"status": "Compliant", "compliance": True, "workers_detected": 4, "workers_compliant": 3, "note": "3 workers confirmed; 1 worker footwear obscured"},
            "safety_harness": {"status": "Non-Compliant", "compliance": False, "workers_detected": 1, "workers_compliant": 0, "note": "Worker at elevation >6 ft not wearing fall-arrest harness — Critical OSHA 1926.502 violation"},
            "safety_goggles": {"status": "Not Applicable", "compliance": True, "workers_detected": 0, "workers_compliant": 0, "note": "No grinding / cutting operations visible in frame"},
            "gloves": {"status": "Partial", "compliance": False, "workers_detected": 4, "workers_compliant": 2, "note": "Rebar handling workers should wear cut-resistant gloves"}
        },
        "site_hazards": [
            {"hazard": "Fall Risk at Elevated Platform", "severity": "Critical", "location": "North scaffolding structure", "description": "Worker operating without fall-arrest harness at ~3.2 m elevation. Immediate stoppage required.", "corrective_remedy": "Stop work immediately. Issue full-body harness + lanyard. Inspect anchor points before resuming. Tag unsafe area."},
            {"hazard": "Inadequate High-Vis PPE", "severity": "High", "location": "General site perimeter", "description": "50% of visible workers lack ANSI/ISEA 107 Class 2 or higher high-visibility vests near active vehicle paths.", "corrective_remedy": "Issue Type R Class 2 vests. Conduct 5-min toolbox talk on PPE compliance. Record in daily safety log."},
            {"hazard": "Unsecured Material Stack", "severity": "Medium", "location": "Material lay-down zone", "description": "Steel rebars stacked informally without end caps or barriers. Trip and impalement hazard.", "corrective_remedy": "Stack horizontally with timber dunnage. Install rebar end caps. Mark exclusion zone with barrier tape."},
            {"hazard": "Electrical Cable on Ground", "severity": "High", "location": "Eastern walkway", "description": "Temporary power cable running across pedestrian walkway without protective cover or overhead routing.", "corrective_remedy": "Route cable overhead at >2.5 m clearance or install OSHA-compliant cable protectors/ramps. Ground-fault protection required."},
            {"hazard": "Inadequate Signage", "severity": "Low", "location": "Site entrance", "description": "PPE mandatory signage partially obscured by equipment. IS 9457 compliant signs required.", "corrective_remedy": "Reposition or replace damaged safety signage. Ensure bilingual (English/local language) compliance boards are visible."}
        ],
        "regulatory_flags": ["OSHA 1926.502 — Fall Protection", "OSHA 1926.651 — Struck-by Hazard", "IS 456:2000 Cl.5.3 — Material Handling"],
        "audit_timestamp": "2026-10-25T21:00:00+05:30",
        "recommendation_summary": "Immediate corrective action required for fall-protection violation. Schedule follow-up inspection within 24 hours. Partial PPE compliance noted — conduct mandatory site-wide PPE briefing."
    },
    {
        "safety_score": 91,
        "overall_status": "High Compliance",
        "compliance_standards": ["OSHA 29 CFR 1926", "IS 456:2000"],
        "ppe_detection": {
            "hard_hat_helmet": {"status": "Compliant", "compliance": True, "workers_detected": 6, "workers_compliant": 6, "note": "All workers wearing approved hard hats"},
            "high_visibility_vest": {"status": "Compliant", "compliance": True, "workers_detected": 6, "workers_compliant": 6, "note": "All workers equipped with Class 2 high-vis vests"},
            "steel_toe_boots": {"status": "Compliant", "compliance": True, "workers_detected": 6, "workers_compliant": 5, "note": "Minor: 1 worker footwear unverifiable"},
            "safety_harness": {"status": "Compliant", "compliance": True, "workers_detected": 2, "workers_compliant": 2, "note": "Both elevated workers using full-body fall-arrest harnesses"},
            "safety_goggles": {"status": "Compliant", "compliance": True, "workers_detected": 3, "workers_compliant": 3, "note": "Grinding station workers using approved eye protection"},
            "gloves": {"status": "Compliant", "compliance": True, "workers_detected": 6, "workers_compliant": 5, "note": "Cut-resistant gloves visible on rebar handlers"}
        },
        "site_hazards": [
            {"hazard": "Minor Housekeeping Debris", "severity": "Low", "location": "South work zone", "description": "Small accumulation of formwork timber off-cuts near walkway.", "corrective_remedy": "Clear debris to designated waste zone. Conduct end-of-shift housekeeping."},
            {"hazard": "Partially Open Excavation", "severity": "Medium", "location": "Foundation trench — Grid C4", "description": "Trench edge lacking full OSHA-compliant barricade on one side.", "corrective_remedy": "Install rigid barricades + warning lights. Install shoring if trench exceeds 1.5 m depth."}
        ],
        "regulatory_flags": ["IS 456:2000 Cl.5.3 — Minor Housekeeping"],
        "audit_timestamp": "2026-10-25T21:00:00+05:30",
        "recommendation_summary": "Site demonstrates strong PPE compliance. Address minor housekeeping and excavation barricade gaps within 8 hours. Continue daily safety inspections."
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# Tab 2 · Crack Diagnostics
# ─────────────────────────────────────────────────────────────────────────────

DEMO_CRACK_REPORTS = [
    {
        "defect_classification": "Structural Shear Crack",
        "crack_type_code": "SC-03",
        "estimated_crack_width_mm": 3.8,
        "estimated_crack_length_mm": 420,
        "crack_depth": "Deep — likely full section penetration",
        "crack_orientation": "Diagonal (45° to horizontal)",
        "affected_area_m2": 0.6,
        "urgency": "Critical",
        "urgency_score": 95,
        "root_causes": [
            "Differential settlement of foundation exceeding IS 456:2000 permissible limits (>25 mm for isolated footings)",
            "Shear force exceeding design capacity at beam-column junction",
            "Inadequate shear reinforcement (stirrup spacing non-compliant with IS 13920)",
            "Construction deficiency — suspected inadequate concrete cover to reinforcement",
            "Possible seismic demand exceedance in Zone III/IV region"
        ],
        "structural_risk_assessment": {
            "load_bearing_impact": "High — structural integrity compromised",
            "collapse_risk": "Moderate-High without immediate intervention",
            "water_ingress_risk": "High — crack width >0.3 mm per IS 456 limit",
            "reinforcement_corrosion_risk": "High"
        },
        "recommended_repairs": [
            {
                "repair_method": "Structural Epoxy Injection",
                "description": "High-strength low-viscosity epoxy resin (ASTM C881 Type IV) injection under controlled pressure (0.3–0.6 MPa). Restore structural continuity and monolithic behavior.",
                "priority": "Immediate",
                "estimated_cost_inr": "₹45,000 – ₹80,000"
            },
            {
                "repair_method": "Carbon Fibre Reinforced Polymer (CFRP) Wrapping",
                "description": "Apply uni-directional CFRP fabric bonded with epoxy laminate to provide shear confinement and prevent further crack propagation.",
                "priority": "Urgent",
                "estimated_cost_inr": "₹1,20,000 – ₹2,50,000"
            },
            {
                "repair_method": "Structural Re-Grouting & Patch Repair",
                "description": "Remove loose concrete, clean reinforcement, apply corrosion inhibitor, and re-grout with non-shrink cementitious grout (IS 9103 compliant).",
                "priority": "Concurrent",
                "estimated_cost_inr": "₹15,000 – ₹35,000"
            }
        ],
        "compliance_references": ["IS 456:2000 Clause 6.2 — Durability", "IS 13920:2016 — Seismic Detailing", "ASTM C881 — Epoxy Resin Structural Bonding", "ACI 224.1R-07 — Causes, Evaluation, and Repair of Cracks"],
        "immediate_actions": ["Place structural supports / shores under affected beam immediately", "Restrict access to affected zone", "Commission licensed Structural Engineer for urgent assessment within 24 hours", "Do not apply any additional loads to structure"],
        "monitoring_recommendation": "Install crack width monitoring gauges at 3 reference points. Record measurements every 24 hours. If crack width increases >0.5 mm/day, evacuate immediately."
    },
    {
        "defect_classification": "Hairline Settlement Crack",
        "crack_type_code": "HC-01",
        "estimated_crack_width_mm": 0.15,
        "estimated_crack_length_mm": 180,
        "crack_depth": "Superficial — surface mortar only",
        "crack_orientation": "Vertical / Sub-vertical",
        "affected_area_m2": 0.05,
        "urgency": "Low",
        "urgency_score": 22,
        "root_causes": [
            "Normal plastic shrinkage during initial concrete / mortar curing",
            "Thermal expansion/contraction cycles typical of Indian climate",
            "Minor differential settlement within IS 456 permissible range",
            "Inadequate curing duration (minimum 7-day wet curing not maintained)"
        ],
        "structural_risk_assessment": {
            "load_bearing_impact": "Negligible — cosmetic defect only",
            "collapse_risk": "Very Low",
            "water_ingress_risk": "Low — crack width <0.2 mm IS 456 limit",
            "reinforcement_corrosion_risk": "Low"
        },
        "recommended_repairs": [
            {
                "repair_method": "Acrylic / Elastomeric Crack Filler",
                "description": "Surface preparation by wire brushing. Apply acrylic polymer-modified mortar or elastomeric sealant to seal hairline crack. Finish with texture coat.",
                "priority": "Routine",
                "estimated_cost_inr": "₹800 – ₹2,500"
            },
            {
                "repair_method": "Epoxy Paste Surface Seal",
                "description": "For exposed locations, apply epoxy paste sealant to prevent moisture ingress and carbonation.",
                "priority": "Optional",
                "estimated_cost_inr": "₹1,500 – ₹4,000"
            }
        ],
        "compliance_references": ["IS 456:2000 Table 16 — Nominal cover", "IS 3370 — Crack width limits for water-retaining structures"],
        "immediate_actions": ["Monitor crack for progression over 30-day period", "Document with photographic record and date stamp", "Apply temporary waterproof membrane if exposed to rain"],
        "monitoring_recommendation": "Visual inspection monthly for 6 months. No immediate intervention required. Repair during next scheduled maintenance cycle."
    },
    {
        "defect_classification": "Spalling & Delamination",
        "crack_type_code": "SP-05",
        "estimated_crack_width_mm": 8.5,
        "estimated_crack_length_mm": 650,
        "crack_depth": "Moderate — concrete cover delaminated, reinforcement exposed in 2 zones",
        "crack_orientation": "Irregular / Circumferential around rebar",
        "affected_area_m2": 1.2,
        "urgency": "High",
        "urgency_score": 78,
        "root_causes": [
            "Reinforcement corrosion causing expansive rust buildup (chloride or carbonation-induced)",
            "Inadequate concrete cover (<25 mm actual vs IS 456 minimum requirement)",
            "Water infiltration and freeze-thaw cycling",
            "Alkali-Silica Reaction (ASR) — gel expansion causing internal pressure",
            "Construction deficiency — honeycombing visible in spalled zone"
        ],
        "structural_risk_assessment": {
            "load_bearing_impact": "Moderate — section loss reducing effective structural capacity",
            "collapse_risk": "Low-Moderate with active monitoring",
            "water_ingress_risk": "Critical — direct water contact with reinforcement",
            "reinforcement_corrosion_risk": "Critical — active corrosion confirmed"
        },
        "recommended_repairs": [
            {
                "repair_method": "Concrete Repair Mortar + Anti-Corrosion Treatment",
                "description": "Remove all delaminated concrete (hammer tap test). Clean reinforcement with wire brushing to Sa 2.5 standard. Apply corrosion inhibiting primer. Reinstate concrete section with polymer-modified repair mortar (IS 9103 / EN 1504).",
                "priority": "Urgent",
                "estimated_cost_inr": "₹35,000 – ₹75,000"
            },
            {
                "repair_method": "Cathodic Protection System",
                "description": "Install impressed current cathodic protection (ICCP) system to arrest ongoing electrochemical corrosion of embedded reinforcement.",
                "priority": "Recommended",
                "estimated_cost_inr": "₹1,50,000 – ₹4,00,000"
            },
            {
                "repair_method": "Carbonation / Chloride Barrier Coating",
                "description": "Apply silane/siloxane penetrating sealer + elastomeric waterproof membrane coat over repaired and adjacent surfaces to prevent future ingress.",
                "priority": "Post-Repair",
                "estimated_cost_inr": "₹12,000 – ₹28,000"
            }
        ],
        "compliance_references": ["IS 456:2000 Clause 26.4 — Nominal Cover", "IS 9103:1999 — Admixtures", "EN 1504 — Concrete Repair Products", "CPWD Maintenance Manual"],
        "immediate_actions": ["Prop / shore any beams/slabs showing active spalling from soffit", "Seal exposed reinforcement with temporary epoxy paste", "Engage structural consultant within 72 hours", "Restrict vehicle / pedestrian loading in affected bay"],
        "monitoring_recommendation": "Conduct half-cell potential survey to map corrosion activity extent. Chloride content and carbonation depth testing required. Repair within 30 days."
    },
    {
        "defect_classification": "Thermal Expansion Crack",
        "crack_type_code": "TC-04",
        "estimated_crack_width_mm": 1.4,
        "estimated_crack_length_mm": 310,
        "crack_depth": "Moderate — through plaster and partial brickwork/concrete",
        "crack_orientation": "Horizontal / Step pattern",
        "affected_area_m2": 0.35,
        "urgency": "Medium",
        "urgency_score": 55,
        "root_causes": [
            "Restrained thermal movement at junction of dissimilar materials (RCC frame and masonry infill)",
            "Absence of flexible expansion joint at roof slab parapet junction",
            "Diurnal temperature fluctuations exceeding 20°C in semi-arid climate",
            "Inadequate thermal insulation on exposed roof terrace"
        ],
        "structural_risk_assessment": {
            "load_bearing_impact": "Negligible — primarily non-structural thermal strain relief",
            "collapse_risk": "Very Low",
            "water_ingress_risk": "Moderate — rainwater penetration potential",
            "reinforcement_corrosion_risk": "Low"
        },
        "recommended_repairs": [
            {
                "repair_method": "Polyurethane Flexible Joint Sealant",
                "description": "V-groove crack to 10x10 mm. Clean and prime surface. Insert closed-cell polyethylene foam backer rod and tool high-performance moisture-curing polyurethane sealant.",
                "priority": "Routine",
                "estimated_cost_inr": "₹4,500 – ₹10,000"
            },
            {
                "repair_method": "Structural Re-Grouting & Thermal Movement Joint",
                "description": "Retrofit 20 mm vertical expansion control joint with compressible filler board and polysulphide sealant to accommodate future thermal cycles.",
                "priority": "Concurrent",
                "estimated_cost_inr": "₹18,000 – ₹35,000"
            }
        ],
        "compliance_references": ["IS 3414:1968 — Code of Practice for Design of Joints in Buildings", "IS 456:2000 Cl.27 — Expansion Joints"],
        "immediate_actions": ["Rake out loose mortar and seal with temporary weatherproofing", "Inspect adjacent roof waterproof membrane for tears", "Schedule permanent movement joint installation"],
        "monitoring_recommendation": "Install tell-tale crack width monitor to track seasonal movement (summer vs winter). Record at peak temperature and minimum night temperature."
    },
    {
        "defect_classification": "Settlement Crack",
        "crack_type_code": "SC-02",
        "estimated_crack_width_mm": 2.6,
        "estimated_crack_length_mm": 510,
        "crack_depth": "Deep — extending through structural masonry and foundation plinth",
        "crack_orientation": "Diagonal stepped pattern from foundation upwards",
        "affected_area_m2": 0.85,
        "urgency": "High",
        "urgency_score": 82,
        "root_causes": [
            "Differential settlement of corner footing due to uneven subsoil bearing capacity or localized moisture saturation",
            "Inadequate consolidation of backfill beneath plinth beam",
            "Plumbing leak or broken stormwater drain softening foundation soil",
            "Bearing pressure exceeding safe bearing capacity (SBC) under sustained structural dead load"
        ],
        "structural_risk_assessment": {
            "load_bearing_impact": "Moderate-High — load path redistribution occurring",
            "collapse_risk": "Moderate if soil settlement continues active",
            "water_ingress_risk": "High — subsoil moisture seepage into plinth",
            "reinforcement_corrosion_risk": "Moderate"
        },
        "recommended_repairs": [
            {
                "repair_method": "Structural Re-Grouting & Micro-Piling Underpinning",
                "description": "Pressure grout subsoil void beneath footing with micro-fine cementitious grout. If settlement continues, install 150 mm diameter bored cast-in-situ micropiles to competent stratum.",
                "priority": "Immediate",
                "estimated_cost_inr": "₹85,000 – ₹2,20,000"
            },
            {
                "repair_method": "Low-Viscosity Structural Epoxy Injection",
                "description": "Once foundation is stabilized, inject structural epoxy resin under 0.4 MPa pressure along entire crack profile to restore shear capacity.",
                "priority": "Post-Repair",
                "estimated_cost_inr": "₹25,000 – ₹55,000"
            }
        ],
        "compliance_references": ["IS 1904:1986 — Design and Construction of Foundations in Soils", "IS 13094:1992 — Ground Improvement", "IS 456:2000 Cl.6.2"],
        "immediate_actions": ["Fix optical crack monitoring target across crack line", "Identify and repair any subterranean water or drainage leakages within 5m", "Shoring of distressed corner column/wall bay", "Restrict dynamic loads on overlying slab"],
        "monitoring_recommendation": "Daily levelling survey of plinth and bi-weekly crack gauge measurements for 60 days to confirm cessation of settlement before stitching crack."
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# Tab 4 · Chatbot fallback responses
# ─────────────────────────────────────────────────────────────────────────────

DEMO_CHAT_RESPONSES = {
    "concrete": (
        "**Concrete Quality & Mix Design (IS 456:2000)**\n\n"
        "For M25 grade concrete (fck = 25 MPa), the nominal mix ratio is **1:1:2** (Cement:FA:CA). "
        "However, IS 456 mandates design mix for all structural concrete in Exposure Condition 'Moderate' and above.\n\n"
        "**Key water-cement ratio limits:**\n"
        "- Mild exposure: ≤ 0.55\n- Moderate: ≤ 0.50\n- Severe: ≤ 0.45\n- Very Severe: ≤ 0.40\n\n"
        "Minimum 7-day wet curing is mandatory. For OPC cement, strength development at 28 days should reach ≥ fck. "
        "Slump test every 50 m³ of pour is recommended."
    ),
    "foundation": (
        "**Foundation Design Principles (IS 1904)**\n\n"
        "Foundation selection depends on safe bearing capacity (SBC) of soil:\n"
        "- SBC > 200 kN/m²: Isolated footings\n"
        "- SBC 100–200 kN/m²: Raft / Combined footings\n"
        "- SBC < 100 kN/m²: Pile foundation\n\n"
        "**Settlement limits per IS 456:**\n"
        "- Max total settlement: 65 mm (isolated), 40 mm (raft on sand)\n"
        "- Max differential settlement: L/500 between adjacent columns\n\n"
        "Always conduct soil investigation (BIS/ASTM bore log) before finalizing foundation type."
    ),
    "safety": (
        "**Construction Site Safety — OSHA & IS Standards**\n\n"
        "Critical safety protocols for active construction sites:\n\n"
        "1. **Fall Protection** (OSHA 1926.502): Mandatory for work at ≥ 1.8 m (6 ft) height\n"
        "2. **Scaffolding** (IS 3696): Max load 270 kg/m², toe boards mandatory\n"
        "3. **Excavation** (OSHA 1926.651): Shoring required for trenches > 1.5 m deep\n"
        "4. **Electrical Safety**: GFCI required on all temporary power\n"
        "5. **PPE**: Hard hat + high-vis vest + steel-toe boots mandatory site-wide\n\n"
        "Daily toolbox talks and weekly HSE inspections are best practice."
    ),
    "steel": (
        "**Reinforcement Steel — IS 1786 & IS 456**\n\n"
        "**Common grades used in India:**\n"
        "- Fe 415 — fy = 415 MPa (most common)\n"
        "- Fe 500 — fy = 500 MPa (high-strength structures)\n"
        "- Fe 550D — fy = 550 MPa (seismic zones)\n\n"
        "**Thumb rules for estimation:**\n"
        "- RCC Slab: 80–120 kg per m³ concrete\n"
        "- Beam: 120–200 kg per m³ concrete\n"
        "- Column: 150–250 kg per m³ concrete\n"
        "- Foundation: 60–100 kg per m³ concrete\n\n"
        "Lapping length = 50d (tension zone), 45d (compression). Minimum cover 25–40 mm per IS 456 Cl.26.4."
    ),
    "default": (
        "**Construction Engineering Assistant** 🏗️\n\n"
        "I'm your AI-powered construction engineering consultant. I can help with:\n\n"
        "- **Structural design** guidance (IS 456, IS 800, IS 1786)\n"
        "- **Safety protocols** (OSHA, IS 3696, NBC 2016)\n"
        "- **Material specifications** (concrete mix, steel grades)\n"
        "- **Quality control** procedures and testing\n"
        "- **Cost estimation** and BOQ preparation\n"
        "- **Foundation design** (IS 1904, IS 2911)\n"
        "- **Earthquake-resistant design** (IS 1893, IS 13920)\n\n"
        "Please ask me a specific question about your construction project!"
    )
}

def get_demo_safety_report():
    return random.choice(DEMO_SAFETY_REPORTS)

def get_demo_crack_report():
    return random.choice(DEMO_CRACK_REPORTS)

def get_demo_chat_response(message: str) -> str:
    msg_lower = message.lower()
    for keyword, response in DEMO_CHAT_RESPONSES.items():
        if keyword in msg_lower:
            return response
    return DEMO_CHAT_RESPONSES["default"]

