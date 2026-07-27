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
