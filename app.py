import json
from pathlib import Path
import streamlit as st
from sentinelx.engine import evaluate_request, append_audit_event

st.set_page_config(page_title="SENTINEL-X | Trust Interceptor", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 2rem;}
.hero {padding: 1.4rem 1.6rem; border: 1px solid #d9e2ef; border-radius: 16px; background: linear-gradient(120deg,#ffffff,#f4f8fc);}
.eyebrow {color:#4263eb; font-size:.78rem; font-weight:750; letter-spacing:.14em;}
.muted {color:#667085;}
.passport {border:1px solid #d9e2ef; border-radius:14px; padding:1rem 1.2rem; background:#fff;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="eyebrow">AI SECURITY CONTROL PLANE</div><h1>SENTINEL-X</h1><p>Trust Interceptor · Explainable request decisions</p><p class="muted">A local prototype using synthetic inputs and simulated outputs. No external AI call is made.</p></div>', unsafe_allow_html=True)
st.write("")
left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Request context")
    role = st.selectbox("Simulated user role", ["employee", "analyst", "admin"])
    classification = st.selectbox("Requested data classification", ["public", "internal", "confidential", "restricted"])
    purpose = st.text_input("Business purpose", placeholder="e.g., Summarise an approved internal report")
    prompt = st.text_area("Prompt to inspect", height=150, placeholder="Enter synthetic sample text only")
    output = st.text_area("Simulated AI output to verify (optional)", height=100, placeholder="e.g., A safe summary with no sensitive details")
    run = st.button("Generate Trust Decision Passport", type="primary", use_container_width=True)

with right:
    st.subheader("Policy at a glance")
    st.markdown("""
    - **Gate 1 — Permission boundary:** role versus requested classification.
    - **Gate 2 — Data exposure:** configured patterns for emails, possible SA ID numbers and API-key-like strings.
    - **Gate 3 — Prompt integrity:** known prompt-injection phrases.
    - **Gate 4 — Output verification:** checks simulated output for selected sensitive patterns and script tags.
    """)
    st.info("The role selector is a demonstration input, not real authentication. A production deployment must derive identity and permissions from a trusted identity provider and server-side policy.")

if run:
    if not prompt.strip():
        st.warning("Enter a synthetic prompt before generating a passport.")
    else:
        passport = evaluate_request(
            user_role=role, data_classification=classification,
            purpose=purpose, prompt=prompt, simulated_output=output
        )
        append_audit_event(passport, "audit.jsonl")
        st.session_state["last_passport"] = passport

passport = st.session_state.get("last_passport")
if passport:
    st.divider()
    st.subheader("Trust Decision Passport")
    decision = passport["decision"]
    if decision == "ALLOW":
        st.success(f"Decision: {decision}")
    elif decision == "BLOCK":
        st.error(f"Decision: {decision}")
    else:
        st.warning(f"Decision: {decision}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Passport ID", passport["passport_id"])
    c2.metric("Input findings", len(passport["input_findings"]))
    c3.metric("Output findings", len(passport["output_findings"]))

    with st.container(border=True):
        st.markdown("**Decision explanation**")
        for reason in passport["reasons"]:
            st.write(f"- {reason}")
        st.markdown("**Findings**")
        if passport["all_findings"]:
            for finding in passport["all_findings"]:
                st.code(finding)
        else:
            st.write("No configured risk indicators detected.")
        st.markdown("**Accountability metadata**")
        st.write(f"Role: `{passport['user_role']}` · Classification: `{passport['data_classification']}` · Purpose provided: `{passport['purpose_provided']}`")
        st.write(f"Created (UTC): {passport['created_at_utc']}")
        st.write(f"Prompt fingerprint (SHA-256 prefix): `{passport['prompt_fingerprint']}`")
        st.caption("The raw prompt and simulated output are not written to the audit log. A hash is a correlation aid, not anonymisation or proof that the input was safe.")

    st.download_button("Download passport JSON", data=json.dumps(passport, indent=2), file_name=f"{passport['passport_id']}.json", mime="application/json")
    st.caption("Prototype limitation: a passport explains configured rule outcomes; it does not prove a real AI model behaved safely.")
