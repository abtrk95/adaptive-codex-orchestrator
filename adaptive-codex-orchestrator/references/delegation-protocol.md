# Assignment and return contracts

## Minimum assignment

Give every worker an objective, task-local context, concrete deliverable, boundaries, and completion conditions. A read-only question may fit in one paragraph. Add the extended fields for edits, dependencies, shared resources, or recovery. Never invent commit IDs, usage statistics, or tools.

```text
Task: <ID and revision when useful>
Objective: <bounded outcome and user acceptance criteria>
Context: <relevant user requirements, repository facts, applicable instructions>
Inputs: <paths, symbols, source links, baseline/dirty-state description>
Dependencies: <available artifacts or agreed provisional interface; assumptions>
Responsibility: <investigate | implement | verify>
Allowed changes: <exact files/directories/resources, or read-only>
Prohibited changes: <shared interfaces/lockfiles/user edits/external actions outside scope>
Tools and permissions: <actual tools and inherited limits; no expansion>
Deliverable: <patch/artifact/findings with provenance>
Verification: <specific checks/evidence, not every possible test>
Finish: <observable completion condition>
Escalate: <missing dependency, consequential ambiguity, file overlap,
           incompatible model/tool, failed check, or authorization boundary>
Budget: <applicable limits, expected milestone, recovery allowance>
Report: <status, output/changes, evidence, uncertainty/blockers, next action>
No child agents unless explicitly allocated by the coordinator.
```

Restate necessary context for a no-history worker. Supply only paths it can access. Separate repository facts from assumptions. Omit credentials and irrelevant personal information.

## Return contract

Request concise structured prose or an object. This is an instruction contract, not a tool-enforced schema.

```text
Task/revision:
Status: completed | partial | blocked | failed
Completed:
Actual changes/artifacts: <paths and summary; none if read-only>
Evidence: <check/source; cwd; result/exit where applicable;
           tested revision/input snapshot; log/artifact path>
Unverified: <claims not demonstrated; omitted checks and reason>
Assumptions/dependencies:
Problems/blockers: <impact and minimum resolution>
Recommended next action:
Writer status: <finished; remaining tool/process sessions if any>
```

Completed describes the worker's assignment, not final integration. The coordinator inspects it. Research uses source URL/date and claim relevance instead of command fields. Reviews identify file/symbol, reproducible concern, and consequence, without invented confidence percentages.

## Revisioned updates

Send `T3 r2 supersedes r1: <new fact>; change <scope>; preserve <valid outputs>; stop before <unsafe action>; acknowledge before writing <shared path>`. Delivery may occur only at a model boundary or after a tool call. A message does not cancel a running command. If safety depends on the update, await acknowledgement or a result tied to the new revision.

Use a non-triggering message for information to a running agent where supported. Use the current follow-up operation to restart an idle agent. Check live schemas; names and parameters vary.

## Recovery assignment

Supply the failed criterion, logs/artifacts, partial changes, current baseline, and changed hypothesis or missing context. Preserve valid work; do not simply resend the original prompt. Report the original failure and repair separately.

Before reassigning writes, establish that the previous worker and relevant process sessions stopped. Silence, delivered messages, or an interrupt's prior-status response do not establish termination. Otherwise assign nonconflicting work or report blocked paths.

## Examples

**Read-only:** Find the code path rejecting empty pagination cursors. Read src/api and relevant tests; do not edit. Return exact symbols, observed behavior, and the smallest relevant check. Stop once the path is supported by code evidence. No child agents.

**Implementation:** T2 r1: implement CSV import against contract C1 in docs/import-contract.md. Own only src/import_csv.py and tests/test_import_csv.py; the coordinator owns registry.py and lockfiles. Preserve the public API and user changes described in baseline.txt. Check normal, empty, and malformed input. Return paths, command/cwd/exit, assumptions, and any remaining process sessions. Escalate if C1 is insufficient; do not edit another adapter or spawn children.

**Review:** Inspect the current migration patch against the idempotence criteria. Do not edit or apply migrations. Identify counterexamples with file/symbol evidence and safe local checks where available. Report unverified risks separately. Agreement with the author is not a completion condition.
