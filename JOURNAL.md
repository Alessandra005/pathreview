## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/50

**Issue title:** Test coverage detection logic

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The PathReview analyzer currently does not detect whether a repository contains tests. This issue requires adding logic to identify test directories (tests/ or test/), pytest.ini, or files matching test_*.py. The goal is to surface a boolean field `has_tests` in the analysis output. This affects the repo analyzer and GitHub tool modules.

**Branch name:** feat/50-test-detection

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/Alessandra005/pathreview/commit/3cfb305

**Reproduction summary:**
Created a mocked unit test (`tests/unit/test_github_tool.py`) that runs `GitHubTool.execute()` and checks that `"has_tests"` appears in the returned metadata. The test fails, showing that the field is completely missing even though the sample repo includes a `tests/` directory. The test uses mocked `httpx.get` and `httpx.head` calls so it stays offline and avoids GitHub rate limits, following the same mocking style already used in other tests under `tests/unit/`.

**PLAN.md link:** https://github.com/Alessandra005/pathreview/blob/feat/50-test-detection/PLAN.md

**Blockers or open questions:**
The original issue pointed to `agent/tools/repo_analyzer.py`, but that file doesn’t exist in this project. The correct place for the fix is `GitHubTool._fetch_repo_metadata`, next to where `has_readme` is already computed. While writing the test, a separate mypy error surfaced in the `_has_readme` helper. This issue isn’t related to #50, so I’m not fixing it here, but I’m noting it in the plan for future cleanup.

## Week 9 — Solution building & PR submission

### Check-in 1

**Current progress:**
Implemented the fix in `GitHubTool`. Added a `_has_tests(username, repo_name)` helper (modeled on `_has_readme`) that lists the repo root via the GitHub contents API and detects a `tests/` or `test/` directory, a `pytest.ini` file, or a root-level `test_*.py` file, then wired its result into `_fetch_repo_metadata` as a new `has_tests` boolean. The Week 8 reproduction test now passes. Sub-tasks 1–3 from PLAN.md are done.

**Next steps:**
Expand `tests/unit/test_github_tool.py` from the single reproduction test into a full suite covering every detection branch and the graceful-failure paths (non-200, non-list payload, network error). Run `make check` and `make test-unit`, confirm my changes add no new failures on top of the codebase's documented pre-existing ones, then open a draft PR for peer feedback.

**Blockers:**
The codebase has a large number of pre-existing `make check`/`make test-unit` failures unrelated to #50. I recorded a baseline (54 failing unit tests, 182 ruff errors, 5 mypy errors) before starting so I can prove my change doesn't make things worse.

---

### Check-in 2 

**PR link:** https://github.com/ascherj/pathreview/pull/644

**Branch:** `feat/50-test-detection`

**What you built:**
A `has_tests` boolean was added to the GitHub repo analysis output. `GitHubTool._has_tests` queries the GitHub contents API for the repository root and returns `True` when it finds a `tests/`/`test/` directory, a `pytest.ini`, or a root-level `test_*.py` file, mirroring the existing `has_readme` signal. It returns explicit booleans and swallows non-200/malformed/network errors as `False`, so it adds no new failure mode to metadata fetching.

**Tests added or updated:**
`tests/unit/test_github_tool.py` — replaced the single reproduction test with 10 unit tests: each detection branch (`tests/`, `test/`, `pytest.ini`, `test_*.py`), the no-indicator case, a negative case for non-test files that merely contain "test", the non-200 / non-list / exception fallbacks, and an end-to-end check that `execute()` surfaces `has_tests` as a boolean. All 10 pass.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes

_Interpreted per the course guidance on pre-existing failures — "passes" means my changes introduce no new failures. Baseline before my change: 54 failing unit tests, 182 ruff errors, 5 mypy errors. After: 53 failing unit tests (my reproduction test now passes; +10 new tests all pass), 181 ruff errors (I fixed the one import-sort error in the file I edited), 5 mypy errors (unchanged). The two files I touched (`agent/tools/github_tool.py`, `tests/unit/test_github_tool.py`) pass `ruff`, `black`, and `mypy` cleanly. To let the touched file pass the mypy pre-commit hook I also wrapped the pre-existing `_has_readme` return in `bool()` (the `no-any-return` error noted in Week 8) — a one-line, behavior-preserving change._

**Draft PR feedback received from:** none
