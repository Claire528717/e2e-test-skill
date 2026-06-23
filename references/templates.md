# PRD E2E Test Agent Templates

## Dedicated Test File

Use one dedicated Markdown file for the whole test lifecycle. Prefer a filename like:

`e2e-test-plan-{feature}-{run_id}.md`

The same file must contain the proposed cases, the data/mock plan, user review status, execution results, bugs, and cleanup status.

## Test Suite Overview

```markdown
# E2E Test Plan and Run Report: {feature/integration}

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

Review Status:
- Current status: Draft / Waiting for user review / Approved for execution / Executed
- Reviewer:
- Review notes:
- Last updated:

Coverage Summary:
| ID | Priority | Title | Actor | Main UI Path | Independent Verification | Status |
|---|---|---|---|---|---|---|
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
```

## Mock and Test Data Plan

```markdown
## Mock and Test Data Plan

Run ID:
- `{run_id}`

Data Naming Rule:
- `{prefix}-{feature}-{timestamp}-{short_random}`

Test Subject Matrix:
| Subject ID | Account/User | Role | Tenant/Domain | App/Ownership | Permission Purpose | Source |
|---|---|---|---|---|---|---|
| U-001 | {employee_a} | Employee | Tenant A | App A owner | Create/manage own assets | Provided / Inferred / To create |
| U-002 | {domain_admin_a} | Domain admin | Tenant A | - | Review tenant assets | Provided / Inferred / To create |
| U-003 | {employee_b} | Employee | Tenant B | App B owner | Cross-tenant visibility check | Provided / Inferred / To create |
| U-004 | {platform_admin} | Platform admin | Global | - | Platform-level operations | Provided / Inferred / To create |

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

UI Operation Path:
1. Open {product/page}.
2. Log in as {actor}.
3. Click {visible label}.
4. Open {page/drawer/modal/tab}.
5. Fill {field label} with {value}.
6. Upload {file}.
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
I created/updated the dedicated E2E test file:

- File: {path}
- Status: Waiting for user review
- Cases: {count}
- P0/P1/P2: {counts}
- Mock/test subjects: {summary}
- User-provided dependencies still needed: {summary}

Please review the cases and mock data plan. I will not start execution until you approve or tell me what to change.
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
- {whether to fix remaining bugs}
- {whether to defer specific bugs}
- {whether to rerun failed or blocked cases}

Residual Risks:
- {untested paths, missing credentials, environment limitations}

Recommendation:
- {release confidence / fix-before-continue / rerun needed}
```

