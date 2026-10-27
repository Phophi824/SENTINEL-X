# SENTINEL-X test results

**Status:** Not yet measured. Run the tests on your machine and replace this statement with actual results.

## Automated unit tests

Run from the repository root:

```bash
python -m unittest discover -s tests -v
```

- Date/time:
- Python version:
- Operating system:
- Number of tests:
- Passed:
- Failed:
- Full output or link to saved output:

## Manual test log

| Case | Input/setting | Expected result | Actual result | Pass/fail |
|---|---|---|---|---|
| T01 | Clean prompt, employee/internal, purpose supplied | ALLOW | Not run | Not run |
| T02 | Prompt includes demo.person@example.com | HUMAN REVIEW | Not run | Not run |
| T03 | Known injection phrase | BLOCK | Not run | Not run |
| T04 | Employee requests restricted data | BLOCK | Not run | Not run |
| T05 | Missing purpose | HUMAN REVIEW | Not run | Not run |
| T06 | Simulated output includes email | HUMAN REVIEW | Not run | Not run |
| T07 | Simulated output includes script tag | HUMAN REVIEW | Not run | Not run |

## Metrics
Do not fill in invented results. Use a labelled test corpus and record TP, FP, TN, and FN before calculating rates. This initial unit-test suite is a functional check of known examples, not a benchmark of general AI security.
