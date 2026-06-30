# E2E Test Skill Templates

## Dedicated Test File

Use one dedicated Markdown file for the whole test lifecycle. Prefer a filename like:

`e2e-test-plan-{feature}-{run_id}.md`

If the user does not specify a path, place the file under `e2e-test-plans/` and store evidence under `e2e-test-evidence/{run_id}/`.

Before execution, the file is an E2E test plan. After the user explicitly authorizes execution and the run starts, append execution results, bugs, and cleanup status to the same file.

## Test Suite Overview

```markdown
# E2E Test Plan: {feature/integration}

Scope:
- In scope:
- Out of scope:

Assumptions:
-

Environment:
- Product URL:
- Database:
- External systems:
- Test accounts:
- Test data run ID:
- Plan file location:
- Evidence directory:

Review Status:
- Current status: Draft / Waiting for user case review / Approved for E2E execution / Changes requested / Executed
- Review decision scope: Case quality and completeness only; not final release acceptance and not proof of execution readiness
- Reviewer:
- Review notes:
- Last updated:

Execution Authorization:
- Current status: Not requested / Requested by user / Verification refresh required / Approved to run / Executed
- Authorized by:
- Authorization notes:
- Authorized at:

PM Review Packet:
- User decision needed: Approve for E2E execution / Request changes / Mark execution blocked
- One-page summary only: Yes / No

Decision Digest:
- Recommendation: Approve / Revise / Blocked
- What this plan covers:
- Coverage gaps:
- What is intentionally not covered:
- Top blockers:
- Top high-risk items:
- Decision needed now: {1-3 decisions only}

Automated Quality Gate:
- Validator: Not run / Passed / Failed
- Blocking structural issues:
- Main-agent fixes made before review:

Second Review:
- Reviewer verdict: Passed / Needs changes / Blocked / Manual review required when sub-agent is unavailable
- Reviewer input scope: PM Review Packet / decision digest / coverage audit / mock-data plan / blocker list / 3-5 top high-risk cases
- Must-fix issues: {up to 5, or none}
- User decisions: {up to 3, or none}
- Reviewer rationale: {one short paragraph}
- Main-agent response: Fixed / Deferred with reason / Moved to user decision / Marked manual review required because sub-agent was unavailable

Execution-Time Verification Refresh:
- Current status: Not started; fill only after the user requests execution / Updated after execution request / Blocked by missing access
- Product URL checked:
- Account/role matrix checked:
- Database/API/log/external-system access checked:
- Cleanup permission checked:
- Plan updated before run: Yes / No

Coverage Summary:
| ID | Priority | Risk | Title | Actor | Main UI Path | Independent Verification | Status |
|---|---|---|---|---|---|---|---|
```


## PRD Coverage Audit

Use this section for every PRD-backed full acceptance plan. For focused-slice plans, include a shortened version that states what is intentionally uncovered.

```markdown
## PRD Coverage Audit

Coverage Position:
- Plan type: Full release acceptance / Focused slice / Prototype-only / Formal environment E2E
- Coverage claim: Full PRD coverage / P0-P1 only / Selected workflow only
- Not covered by this E2E plan:
- Specialty tests required:
- Blocked by product decisions or environment:

Coverage Summary:
| Status | Count | Meaning |
|---|---:|---|
| Covered | 0 | Has executable UI path and independent verification |
| Partially covered | 0 | Missing a branch, role, state, or verification source |
| Blocked | 0 | Cannot honestly plan or run until a dependency is resolved |
| Out of E2E / specialty | 0 | Requires performance, security, load, accessibility, or other test type |
| Out of release scope | 0 | PRD explicitly excludes or defers it |

Requirement Coverage Matrix:
| PRD Item | Acceptance Point | Risk | Coverage Status | Case IDs | Gap / Decision |
|---|---|---|---|---|---|
| PRD-001 | {requirement or checklist item} | High / Medium / Low | Covered / Partially covered / Blocked / Out of E2E / Out of release scope | {CASE-ID} | {missing branch, dependency, specialty test, or none} |

Coverage Gate Notes:
- Every Covered row must reference an existing executable case ID.
- Every row must use exactly one coverage status; put high-risk and blocker details in Risk or Gap / Decision, not in the status cell.
- Every high-risk Partially covered row must name the missing branch or verification source and either add a case or name the execution-time decision needed.
- Every Blocked row must name the missing decision, account, environment, system, or permission.
- Do not ask for review while an explicit P0/P1 PRD item is unmapped unless it is marked Blocked or Out of E2E with a concrete reason.
```
## Dependency Discovery Result

```markdown
## Dependency Discovery

Found:
| Category | Source | Detail | Confidence |
|---|---|---|---|

Missing:
| Category | Required Item | Needed For | User Input Required |
|---|---|---|---|

Execution Impact:
- {what can run now}
- {what is blocked until user provides data}
- Plain-language explanation for non-technical reviewers:
  - {what this means and what decision is needed}
```

## Mock and Test Data Plan

```markdown
## Mock and Test Data Plan

Run ID:
- `{run_id}`

Data Naming Rule:
- `{prefix}-{feature}-{timestamp}-{short_random}`

Mock Scope:
| Mock Item | Type | Why Needed | Source | Creation Method | Used By Cases | Cleanup / Preserve Rule |
|---|---|---|---|---|---|---|
| M-001 | User / Role / Tenant / Permission / App / Product data / File / External object | {purpose} | Inferred from PRD / Generated / Project fixture / Provided | {how to create or provide it} | {case IDs} | Delete if passed / Preserve if failed / Manual cleanup |

Test Subject Matrix:
Add only the subjects required by the PRD, case design, and verification path.

| Subject ID | Account/User | Role | Tenant/Domain | App/Ownership | Permission Purpose | Source |
|---|---|---|---|---|---|---|
| U-001 | {account_or_user} | {role} | {tenant_or_scope} | {owned_resource_or_context} | {permission_needed_for_cases} | Provided / Inferred / To create |

Product Data:
| Data ID | Object Type | Name/Key | Created By | Used By Cases | Cleanup Rule |
|---|---|---|---|---|---|

Files:
| File ID | File Name | Purpose | Generated/Provided | Used By Cases |
|---|---|---|---|---|

External System Data:
| External System | Object Type | Name/Key | Creation Method | Used By Cases | Cleanup Rule |
|---|---|---|---|---|---|

User Must Provide Before Execution:
- {only items that cannot be inferred or safely mocked}

Data Sync Checklist:
- Every case-added account/role/tenant/app is present in the Test Subject Matrix.
- Every case-added product record is present in Product Data.
- Every case-added upload or generated file is present in Files.
- Every case-added external object or verification source is present in External System Data.
- Cleanup rules cover every created record, token, file, and external object.

Plain-Language Notes:
- {which data is mocked and why}
- {which missing items block execution}
- {what can still be designed or tested without those items}
```

## Executable Test Case

```markdown
### {ID} {Priority} {Title}

Purpose:
Validate {business behavior/integration contract/data consistency}.

Actor:
- Account:
- Role/permissions:
- Tenant/domain:

Preconditions:
- Product state:
- External system state:
- Required feature flags/config:

Test Data:
- Generated data:
- Files:
- Records to create:
- Data that must be provided by user:

UI Fidelity Requirement:
- Each tested user action must start from the same visible affordance a real user would use.
- Browser automation may click, type, select, drag, drop, confirm, and wait through the UI, but it must not mutate hidden DOM state, invoke component internals, dispatch synthetic product events, seed storage/session state, or call backend APIs to replace the UI action under test.
- If no visible user path exists for the action, mark the case blocked or failed instead of bypassing the UI.

UI Operation Path:
1. Open {product/page}.
2. Log in as {actor}.
3. Click {visible label}.
4. Open {page/drawer/modal/tab}.
5. Fill {field label} with {value}.
6. Perform the next user action through the visible affordance, such as selecting {file}, choosing an option, dragging an item, or confirming a dialog.
7. Click {button}.
8. Confirm visible result: {toast/state/list row/detail text}.

Independent Verification:
1. Query {product database/table/API} by {stable key}.
2. Verify {field/state/relationship}.
3. Query {external system API/database} by {external ID/reference}.
4. Verify {external object/content/count/version}.
5. Cross-check {product reference} equals {external reference}.

Expected Results:
- UI:
- Product database:
- External system:
- Side effects:

Evidence To Capture:
- Screenshot or visible state:
- Evidence file path, such as `e2e-test-evidence/{run_id}/{case_id}-{step}-{short_desc}.png`:
- Product record ID:
- External system ID:
- Request/correlation ID:
- Query/API result excerpt:

Cleanup:
- Delete or mark test data:
- Revoke subscriptions/tokens:
- External system cleanup:

Blocking Decision Rule:
Stop and ask the user if {condition}, because {impact}.
```

## User Review Request

```markdown
I created/updated the dedicated E2E test file for case review:

- File: {path}
- Status: Waiting for user review
- Cases: {count}
- P0/P1/P2: {counts}
- Mock/test subjects: {summary}
- User-provided dependencies still needed: {summary}

Please review the PM Review Packet first. You should only need the decision digest, automated gate, and reviewer findings to decide whether to execute E2E, request changes, or mark execution blocked. The detailed cases are supporting material, not required reading for the first decision.
```

## Dependency Request

Use this when required inputs cannot be discovered locally.

```markdown
I found:
- {known database/API/UI/test account facts}

I still need:
- {missing product URL/account/credential/API endpoint/test file}

Why it matters:
- {what verification or setup cannot be completed without it}
```

## Blocking Bug Question

```markdown
I hit a blocking issue in {case ID}.

Observed:
- {actual behavior with evidence}

Expected:
- {expected behavior from PRD/test case}

Impact:
- Blocks: {this step/this case/remaining suite}
- Risk if bypassed: {what could be missed}

Recommended decision:
- {pause for fix / allow me to fix this blocking bug then continue / skip affected cases / stop suite}
- {whether this decision should apply only to this bug or to future blocking bugs in the current run}

You can also authorize me to fix future blocking bugs in this run without asking again.

How would you like me to proceed?
```

## Test Run Summary

```markdown
## E2E Test Execution Results

Scope:
- {feature/version/environment}

Result:
| Total | Passed First Try | Passed After Fix | Failed Unrepaired | Blocked | Skipped |
|---:|---:|---:|---:|---:|---:|

Executed Cases:
| ID | Title | Status | First Result | Final Result | Key Evidence | Bug/Fix Status | Notes |
|---|---|---|---|---|---|---|---|

Defects:
| Severity | Case | Bug | Impact | Blocking | Fix Status | Suggested Next Step |
|---|---|---|---|---|---|---|

Deferred Bugs:
| Bug ID | Case | Reason Deferred | Risk | User Decision Needed |
|---|---|---|---|---|

Data Created:
- {records/files/external IDs}

Cleanup Status:
- {done/pending/manual cleanup needed}

User Decisions Needed:
- {whether to fix all remaining bugs now}
- {whether to defer specific bugs}
- {whether to rerun failed or blocked cases}
- {whether to review the post-fix result before accepting the run}

Residual Risks:
- {untested paths, missing credentials, environment limitations}

Recommendation:
- {release confidence / fix-before-continue / rerun needed}
```
