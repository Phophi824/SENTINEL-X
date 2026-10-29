
# SENTINEL-X Test Results

**Status:** Automated unit tests passed locally.

## Automated Unit Tests

The automated test suite completed successfully in the local test environment.

- **Date:** 29 October 2026
- **Operating system:** Windows
- **Python version:** Not recorded
- **Number of tests:** 9
- **Passed:** 9
- **Failed:** 0
- **Errors:** 0
- **Reported runtime:** 0.017 seconds
- **Test command:** `python -m unittest discover -s tests -v`

- **Test output evidence:** `docs/INITIAL_TEST_RUN.txt`
- **Screenshot evidence:** `screenshots/test-results.png`

All nine automated tests passed. The tests cover selected behaviours, including permission boundaries, prompt-injection detection, sensitive-data screening, output checks, and protection of raw prompts in the audit record and Trust Decision Passport.

### Startup Warning

The captured output included a spreadsheet-runtime warmup warning during Python startup. The unit tests nevertheless completed successfully, reporting nine tests and `OK`. The cause of the warning has not been established.

## Automated Test Cases

| Test | Purpose |
|---|---|
| `test_audit_excludes_raw_prompt` | Checks that the audit record excludes the raw prompt. |
| `test_clean_request_allowed` | Checks that a clean request can be allowed. |
| `test_email_requires_review` | Checks that a prompt containing an email pattern requires review. |
| `test_injection_blocked` | Checks that a known prompt-injection example is blocked. |
| `test_missing_purpose_requires_review` | Checks that a request without a purpose requires review. |
| `test_passport_does_not_contain_raw_prompt` | Checks that the Trust Decision Passport excludes the raw prompt. |
| `test_role_boundary_blocks` | Checks that a role-boundary violation is blocked. |
| `test_script_output_requires_review` | Checks that simulated output containing a script tag requires review. |
| `test_sensitive_output_requires_review` | Checks that simulated output containing a sensitive pattern requires review. |

## Manual Test Log

The following manual demonstration cases are planned. Record the actual outcome after running each case in the application.

| Case | Input or setting | Expected result | Actual result | Pass/fail |
|---|---|---|---|---|
| T01 | Clean prompt, employee/internal, purpose supplied | ALLOW | Not recorded | Not run |
| T02 | Prompt includes `demo.person@example.com` | HUMAN REVIEW | Not recorded | Not run |
| T03 | Prompt contains a known injection phrase | BLOCK | Not recorded | Not run |
| T04 | Employee requests restricted data | BLOCK | Not recorded | Not run |
| T05 | Purpose is missing | HUMAN REVIEW | Not recorded | Not run |
| T06 | Simulated output includes an email pattern | HUMAN REVIEW | Not recorded | Not run |
| T07 | Simulated output includes a script tag | HUMAN REVIEW | Not recorded | Not run |

## Metrics

Detection rates, false-positive rates, and other security-performance metrics have not been measured.

To calculate meaningful metrics, a labelled test corpus must be created and evaluated to record true positives (TP), false positives (FP), true negatives (TN), and false negatives (FN).

This initial unit-test suite is a functional check of known examples. It is not a comprehensive benchmark of general AI security, and passing these tests does not prove that SENTINEL-X detects all security threats.

## Limitations

- The prototype uses rule-based checks and known example patterns.
- Identity and AI output are simulated; the prototype is not connected to a live AI model.
- New, obfuscated, or previously unknown attacks may not be detected.
- Legitimate content may be flagged for review.
- The script-tag check is not a complete output sanitisation solution.
- The prototype has not been independently security-audited and is not ready for production use.

## Conclusion

The reported automated run passed all nine unit tests with no failures or errors. This provides initial evidence that selected implemented behaviours work as expected. Further manual testing, broader security testing, and evaluation using a labelled test corpus are needed before drawing wider conclusions about security effectiveness.
