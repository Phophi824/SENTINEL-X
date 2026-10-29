"""SENTINEL-X Trust Interceptor prototype.

This is a demonstrator, not a production security gateway.
It uses deterministic rules and simulated identities/outputs.
"""
from __future__ import annotations
import hashlib
import re
import uuid
from datetime import datetime, timezone

SENSITIVE_PATTERNS = {
    "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "possible_sa_id_number": re.compile(r"(?<!\d)\d{13}(?!\d)"),
    "possible_api_key": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{12,}|AKIA[A-Z0-9]{16})\b"),
}
INJECTION_MARKERS = (
    "ignore all previous instructions",
    "ignore previous instructions",
    "reveal the system prompt",
    "reveal confidential information",
    "bypass security controls",
    "ignore your safety rules",
    "disregard the developer message",
)
ROLE_CLEARANCE = {
    "employee": {"public", "internal"},
    "analyst": {"public", "internal", "confidential"},
    "admin": {"public", "internal", "confidential", "restricted"},
}
OUTPUT_SENSITIVE_PATTERNS = {
    "email_address": SENSITIVE_PATTERNS["email_address"],
    "possible_api_key": SENSITIVE_PATTERNS["possible_api_key"],
}

def _fingerprint(text: str) -> str:
    """One-way digest for correlation; does not store the original prompt."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def inspect_prompt(prompt: str) -> list[str]:
    findings = []
    for label, pattern in SENSITIVE_PATTERNS.items():
        if pattern.search(prompt):
            findings.append(label)
    normalized = " ".join(prompt.lower().split())
    if any(marker in normalized for marker in INJECTION_MARKERS):
        findings.append("possible_prompt_injection")
    if len(prompt) > 5000:
        findings.append("prompt_length_over_5000")
    return findings

def inspect_output(output: str) -> list[str]:
    findings = []
    for label, pattern in OUTPUT_SENSITIVE_PATTERNS.items():
        if pattern.search(output):
            findings.append(f"output_{label}")
    unsafe_html = re.search(r"<\s*script\b", output, re.I)
    if unsafe_html:
        findings.append("output_contains_script_tag")
    return findings

def evaluate_request(*, user_role: str, data_classification: str,
                     purpose: str, prompt: str, simulated_output: str = "") -> dict:
    """Evaluate a request and return an explainable Trust Decision Passport."""
    role = user_role.strip().lower()
    classification = data_classification.strip().lower()
    purpose_clean = purpose.strip()
    prompt = prompt or ""
    simulated_output = simulated_output or ""
    findings = []
    reasons = []

    if role not in ROLE_CLEARANCE:
        findings.append("unknown_role")
        reasons.append("The supplied role is not recognised by the prototype policy.")
    elif classification not in ROLE_CLEARANCE[role]:
        findings.append("role_not_authorised_for_classification")
        reasons.append(f"The {role} role is not authorised for {classification} data.")

    if not purpose_clean:
        findings.append("missing_business_purpose")
        reasons.append("A business purpose is required for accountability.")

    input_findings = inspect_prompt(prompt)
    findings.extend(input_findings)
    if input_findings:
        reasons.append("The input scanner found one or more configured risk indicators.")

    output_findings = inspect_output(simulated_output)
    findings.extend(output_findings)
    if output_findings:
        reasons.append("The simulated output failed one or more configured release checks.")

    # Conservative precedence: block known injection indicators and unauthorised access;
    # otherwise hold for review when data/output indicators or missing purpose exist.
    if "possible_prompt_injection" in findings:
        action = "BLOCK"
        reasons.append("A configured prompt-injection marker was detected.")
    elif "unknown_role" in findings or "role_not_authorised_for_classification" in findings:
        action = "BLOCK"
    elif output_findings:
        action = "HUMAN REVIEW"
    elif any(f in findings for f in (
        "email_address", "possible_sa_id_number", "possible_api_key",
        "prompt_length_over_5000", "missing_business_purpose"
    )):
        action = "HUMAN REVIEW"
    else:
        action = "ALLOW"

    passport = {
        "passport_id": f"SX-{uuid.uuid4().hex[:10].upper()}",
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "user_role": role if role else "missing",
        "data_classification": classification if classification else "missing",
        "purpose_provided": bool(purpose_clean),
        "prompt_fingerprint": _fingerprint(prompt),
        "input_findings": input_findings,
        "output_findings": output_findings,
        "all_findings": findings,
        "decision": action,
        "reasons": reasons or ["No configured risk indicators were detected by this prototype."],
        "processing_mode": "SIMULATED_NO_EXTERNAL_AI_CALL",
        "limitations": [
            "Rule-based detection can miss novel or obfuscated attacks.",
            "ALLOW means no configured indicator was detected; it is not a safety guarantee.",
        ],
    }
    return passport

def append_audit_event(passport: dict, path: str = "audit.jsonl") -> None:
    """Append minimal passport data; never write raw prompt or output text."""
    import json
    event = {
        "passport_id": passport["passport_id"],
        "created_at_utc": passport["created_at_utc"],
        "user_role": passport["user_role"],
        "data_classification": passport["data_classification"],
        "prompt_fingerprint": passport["prompt_fingerprint"],
        "decision": passport["decision"],
        "all_findings": passport["all_findings"],
    }
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
