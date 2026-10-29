# SENTINEL-X pitch deck outline (12 slides maximum)

1. **Title — SENTINEL-X: Trust Interceptor**  
   A practical, explainable checkpoint for safer AI workflows.

2. **Problem**  
   Sensitive data can enter prompts; malicious instructions can manipulate AI workflows; outputs can be used in a way that can lead to the user information being used for the wrong reseon, scammed or any other malicious acts.

3. **Stakeholders and assets**  
   Employees, data owners, security/privacy teams, customers, and sensitive business information.

4. **Root causes**  
   Inconsistent checks at the point of use, permissions detached from AI workflows, weak output controls, unclear escalation, and limited testing.

5. **System map**  
   Identity/purpose → permission boundary → input scanner → prompt integrity → decision → simulated AI/output check → human review/release → minimal audit.

6. **Insight**  
   A prompt-only filter cannot establish whether a user is authorised or whether the output should be released.

7. **Intervention**  
   Four gates plus the Trust Decision Passport: decision, evidence, reasons, and review path.

8. **Demo**  
   Show one clean prompt, one sensitive-data indicator, one injection phrase, and one permission failure. Use synthetic data.

9. **Evidence**  
   Show actual automated test output and manual test log. Include false positives/false negatives from a labelled corpus; disclose the small test-set limitation.

10. **Feasibility**  
    Python + Streamlit, local execution, no paid API required, future identity-provider/model integration identified separately.

11. **Risks and limitations**  
    Rule-based misses, false positives, simulated identity/output, privacy of audit metadata, no production enforcement.

12. **Impact and next steps**  
    Expected benefit: more consistent, explainable checks. Next steps: larger test corpus, security review, trusted identity integration, policy configuration, and controlled pilot.

Speaker guidance: distinguish existing industry risks from your own measured results. Do not claim the idea has never existed or that the prototype prevents all attacks.
