#!/usr/bin/env python3
"""Create a Markdown E2E test plan scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path

from create_run_id import create_run_id, slugify


def plan_markdown(feature: str, run_id: str, plan_path: Path, evidence_dir: Path) -> str:
    return f"""# E2E Test Plan: {feature}

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
- Test data run ID: `{run_id}`
- Plan file location: `{plan_path.as_posix()}`
- Evidence directory: `{evidence_dir.as_posix()}`

Review Status:
- Current status: Draft
- Reviewer:
- Review notes:
- Last updated:

Execution Authorization:
- Current status: Not requested
- Authorized by:
- Authorization notes:
- Authorized at:

Coverage Summary:
| ID | Priority | Title | Actor | Main UI Path | Independent Verification | Status |
|---|---|---|---|---|---|---|
| CASE-E2E-001 | P0 | {{title}} | {{actor}} | {{main visible path}} | {{database/API/log/external check}} | Draft |

## Dependency Discovery

Found:
| Category | Source | Detail | Confidence |
|---|---|---|---|

Missing:
| Category | Required Item | Needed For | User Input Required |
|---|---|---|---|

Execution Impact:
- {{what can run now}}
- {{what is blocked until user provides data}}
- Plain-language explanation for non-technical reviewers:
  - {{what this means and what decision is needed}}

## Mock and Test Data Plan

Run ID:
- `{run_id}`

Data Naming Rule:
- `{run_id}-{{object_type}}-{{short_name}}`

Mock Scope:
| Mock Item | Type | Why Needed | Source | Creation Method | Used By Cases | Cleanup / Preserve Rule |
|---|---|---|---|---|---|---|
| M-001 | User / Role / Tenant / Permission / App / Product data / File / External object | {{purpose}} | Inferred from PRD / Generated / Project fixture / Provided | {{how to create or provide it}} | {{case IDs}} | Delete if passed / Preserve if failed / Manual cleanup |

Test Subject Matrix:
| Subject ID | Account/User | Role | Tenant/Domain | App/Ownership | Permission Purpose | Source |
|---|---|---|---|---|---|---|
| U-001 | {{primary_actor_account}} | {{primary_role}} | {{tenant_or_scope}} | {{owned_resource_or_context}} | {{primary_workflow_permission}} | Provided / Inferred / To create |
| U-002 | {{restricted_or_reviewer_account}} | {{role}} | {{tenant_or_scope}} | {{context}} | {{permission_or_negative_check}} | Provided / Inferred / To create |

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
- {{only items that cannot be inferred or safely mocked}}

Plain-Language Notes:
- {{which data is mocked and why}}
- {{which missing items block execution}}
- {{what can still be designed or tested without those items}}

### CASE-E2E-001 P0 {{Title}}

Purpose:
Validate {{business behavior/integration contract/data consistency}}.

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
- Automation must not mutate hidden DOM state, invoke component internals, dispatch synthetic product events, seed storage/session state, or call backend APIs to replace the UI action under test.
- If no visible user path exists, mark the case blocked or failed.

UI Operation Path:
1. Open {{product/page}}.
2. Log in as {{actor}}.
3. Click {{visible label}}.
4. Perform {{next user action}} through the visible UI affordance.
5. Confirm visible result: {{state/list row/detail text}}.

Independent Verification:
1. Query {{product database/table/API/log/external system}} by {{stable key}}.
2. Verify {{field/state/relationship/count}}.

Expected Results:
- UI:
- Product database:
- External system:
- Side effects:

Evidence To Capture:
- Screenshot or visible state: `{evidence_dir.as_posix()}/CASE-E2E-001-{{step}}-{{short_desc}}.png`
- Product record ID:
- External system ID:
- Request/correlation ID:
- Query/API result excerpt:

Cleanup:
- Delete or mark test data:
- Revoke subscriptions/tokens:
- External system cleanup:

Blocking Decision Rule:
Stop and ask the user if {{condition}}, because {{impact}}.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create an E2E test plan scaffold.")
    parser.add_argument("feature", help="Feature or integration name.")
    parser.add_argument("--run-id", help="Existing run ID. Generated if omitted.")
    parser.add_argument("--output-dir", default="e2e-test-plans")
    parser.add_argument("--evidence-root", default="e2e-test-evidence")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    feature_slug = slugify(args.feature)
    run_id = args.run_id or create_run_id(args.feature)
    output_dir = Path(args.output_dir)
    evidence_dir = Path(args.evidence_root) / run_id
    plan_path = output_dir / f"e2e-test-plan-{feature_slug}-{run_id}.md"

    if plan_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {plan_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(
        plan_markdown(args.feature, run_id, plan_path, evidence_dir),
        encoding="utf-8",
    )
    print(plan_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
