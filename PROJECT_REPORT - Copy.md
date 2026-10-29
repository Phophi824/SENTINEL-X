# SENTINEL-X: Trust Interceptor
## Project documentation (working draft)

### 1. Executive summary
SENTINEL-X is a local prototype that demonstrates an explainable security checkpoint for AI requests. It combines a simulated role/data-classification check, pattern-based input screening, prompt-injection phrase detection, simulated-output checks, and a Trust Decision Passport. The prototype makes no external AI calls and uses synthetic examples.

### 2. Problem and context
Organisations may use generative AI to summarise documents, draft communications, and assist analysis. Risks include sensitive information disclosure, prompt injection, and unsafe handling of model output. Written guidance alone may not ensure that every request is checked consistently at the point of use.

The project question is: **How can an organisation add a practical, explainable checkpoint between employees, sensitive information, and AI workflows without making unsupported claims that AI can be made completely safe?**

### 3. Stakeholders
- Employees using approved AI tools.
- Data owners and business-unit managers.
- Security, privacy, and compliance teams.
- IT administrators responsible for identity and access control.
- Customers or staff whose information may be processed.
- Reviewers who need traceable reasons for a decision.

### 4. Root-cause analysis
The underlying problem is not simply that employees make mistakes. Contributing system causes may include:
- AI workflows that accept prompts without a consistent data-classification check.
- Permissions that are not carried through to the AI workflow.
- Dependence on prompts or policy documents instead of enforceable controls.
- Missing checks on model output before it is displayed or used downstream.
- Insufficient logging of decisions or unclear human escalation paths.
- Limited security testing against both expected and adversarial inputs.

These are hypotheses to validate for a real organisation; this prototype does not claim to have surveyed a company.

### 5. System relationships
The intended data flow is: user identity and purpose → permission check → input data scanner → prompt-integrity checks → policy decision → (in a future integration, approved AI request) → output verification → human review or release → minimal audit record.

In the current prototype, identity is selected from a simulated role list and output is supplied manually. No real identity provider, document repository, or AI model is connected.

### 6. Proposed intervention
The intervention is a four-gate Trust Interceptor with a Trust Decision Passport:
1. Permission boundary checks a simulated role against a data classification.
2. Data exposure screening detects a small set of configured patterns.
3. Prompt integrity flags known suspicious phrases.
4. Output verification checks a simulated response for selected patterns and a script tag.

The passport includes a unique ID, UTC timestamp, simulated role, classification, purpose-presence indicator, prompt fingerprint, findings, decision, and reasons. Audit JSONL stores minimal metadata and excludes the raw prompt and output.

### 7. Alternatives considered
**A. Awareness and written policy only:** inexpensive and important, but depends on user compliance and does not technically inspect every request.

**B. Prompt screening only:** quick to implement, but cannot enforce role permissions or inspect the output.

**C. SENTINEL-X multi-gate prototype:** demonstrates layered controls and explainable decisions. Its main trade-off is complexity and the risk of false positives/false negatives. It remains a prototype until integrated with trusted identity, real policy enforcement, and an actual AI workflow.

### 8. Feasibility
A small local implementation is feasible using Python and Streamlit. It runs without an API key and is testable on a standard laptop. A production version would require threat modelling, privacy/legal review, identity integration, robust policy management, security logging controls, monitoring, accessibility testing, and evaluation on representative data.

### 9. Security, privacy and operational risks
- **False negatives:** simple rules can miss new, obfuscated, or indirect attacks.
- **False positives:** ordinary content may be held for review.
- **Simulated identity:** role selection is not authentication and must not be treated as an access-control mechanism in production.
- **Output checks:** a script-tag pattern is not a complete HTML sanitizer or browser security control.
- **Audit privacy:** fingerprints can still leak information in some contexts; logs need access control, retention limits, and a documented purpose.
- **Human review:** reviewers need guidance, escalation routes, and response-time expectations.
- **Over-reliance:** a green result could be misinterpreted as a guarantee; the interface explicitly warns against this.
- **Scope:** no real model, retrieval system, tools, or external data source is connected.

### 10. Assumptions
- The first demonstrator can use synthetic examples.
- A small, deterministic prototype is acceptable as evidence of an intervention, subject to challenge rules.
- The organisation would define data classifications and access policies before deployment.
- Human reviewers can be identified for uncertain or high-risk requests.

### 11. Evaluation plan and evidence
Run the included unit tests and a separate labelled test set containing benign prompts, sensitive-data indicators, injection phrases, permission violations, missing purpose, and risky simulated outputs. Report:
- Test count and date.
- Correctly identified positive cases (true positives).
- Missed positive cases (false negatives).
- Benign cases incorrectly flagged (false positives).
- Detection rate/recall = TP / (TP + FN), where denominator is non-zero.
- False-positive rate = FP / (FP + TN), where denominator is non-zero.
- Test failures and examples that bypass the rules.

Do not report hypothetical figures as measured results. Enter actual outputs in `TEST_RESULTS.md`.

### 12. Expected impact
The expected benefit is a more consistent and explainable checkpoint for the narrow risks covered by the prototype. The project may help teams discuss policy, permissions, escalation, and auditability. No claim of enterprise risk reduction should be made until tested against a representative workflow and a suitable baseline.

### 13. Originality and contribution
The name, composition, and Trust Decision Passport are the proposed design framing for this submission. Similar concepts such as AI guardrails, policy engines, audit trails, and prompt-injection detection already exist. Do not claim global novelty. The individual contribution should be documented honestly, including implementation choices, test design, modifications, and any AI assistance.

### 14. References
1. NIST. (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile* (NIST AI 600-1). https://doi.org/10.6028/NIST.AI.600-1
2. OWASP GenAI Security Project. (2025). *Top 10 for Large Language Model Applications*. https://genai.owasp.org/llm-top-10/
3. OWASP DevSecOps Guideline. *AI/LLM Application Security Testing and Red Teaming*. https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-6-AI-LLM-Application-Security-Testing/
