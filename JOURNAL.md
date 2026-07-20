## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/50

**Issue title:** Test coverage detection logic

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The PathReview analyzer currently does not detect whether a repository contains tests. This issue requires adding logic to identify test directories (tests/ or test/), pytest.ini, or files matching test_*.py. The goal is to surface a boolean field `has_tests` in the analysis output. This affects the repo analyzer and GitHub tool modules.

**Branch name:** feat/50-test-detection

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
