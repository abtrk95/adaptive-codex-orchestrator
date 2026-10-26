# Verification, integration, and recovery

## Risk-based evidence

Define how consequential requested behavior can be checked before delegation. Select the smallest checks reducing a concrete risk, plus required project gates. Inspect whether authoritative tests exercise the actual request; a pass is evidence, not universal proof.

| Work | Useful evidence |
| --- | --- |
| Small bug | Reproducer/relevant regression, targeted inspection, material boundary case. |
| Multi-module feature | Module checks plus real integration, errors, and compatibility. |
| Refactor | Regression/differential behavior, public interfaces, moved/deleted files. |
| Intermittent failure | Controlled reproduction/interleavings or repeated observations; distinguish mitigation from demonstrated fix. |
| Build/type/config | Relevant parser/type/build check and affected consumer behavior. |
| Sensitive/destructive | Authorization and scope, safe local checks, focused independent scrutiny where useful. |
| Research/review | Primary evidence, claim/source alignment, decisive artifact inspection. |
| Reversible prose/style | Focused inspection; avoid ritual tests. |

Record passed, failed, unavailable, and not-run separately. Missing dependencies do not mean a check passed. Investigate preexisting failure enough to avoid misattribution; do not indiscriminately run an expensive baseline suite.

## Integration

1. Capture relevant baseline and existing user edits. Git status/diff helps but must cover relevant untracked, ignored, generated, renamed, or nongit files. Never stash, reset, discard, or stage unrelated work.
2. Confirm task revision and stopped writer. Inspect actual changed paths, ownership, and evidence. A claimed path list is insufficient where shared-state risk matters.
3. Integrate serially. In a shared workspace, inspect already-present changes instead of applying the same patch twice. For worktrees, follow supported repository procedures, preserve attribution, and inspect conflict resolutions.
4. Validate interface assumptions and real integrated behavior, not only mocks.
5. Associate acceptance outcomes with current evidence; recheck affected scopes after subsequent edits and report residual gaps.

Tests can write outputs, caches, ports, databases, and generated files. Reserve or isolate those resources. A worktree does not isolate external services.

## Failure classes

| Failure | Immediate response | Recovery |
| --- | --- | --- |
| Transient tool/service | Capture error and uncertain side effects | At most one unchanged retry if plausible; check idempotence first. |
| Model/tool unavailable | Distinguish absent schema, rejection, execution failure | Continue useful root work; disclose; substitute only if authorized. |
| Context/scope mismatch | Identify missing input/constraint; inspect partial changes | Send narrow corrected contract without restarting unrelated work. |
| Implementation error | Reproduce criterion and locate cause | Repair with new observation/hypothesis; focused review when useful. |
| Dependency changed | Freeze affected writes; identify assumptions | Revise affected tasks and verify integration. |
| Edit conflict | Preserve contributions and user changes | Serialize resolution under one owner. |
| Contradictory findings | Compare revisions, inputs, tests, and sources | Discriminate by evidence; preserve unresolved impact. |
| Approval rejection | Respect boundary and preserve concrete work | Continue unaffected actions; ask with actual reason if required. |
| Resource exhaustion | Preserve output; distinguish hard cap from estimate | Reduce parallelism; prioritize acceptance-critical work; disclose gaps. |
| Unknown worker state | Inspect native status/known session when needed | Do not infer failure or create a duplicate writer. |

After two no-progress attempts on one issue, change strategy, take over, seek a discriminating observation, or block it. Track repairs across revisions and reassignments. A new agent is not a fresh retry budget.

## Cancellation and reassignment

Use an available stop/interrupt when warranted and record what it confirms. In the observed collaboration host, `interrupt_agent` returns prior status; it does not prove all shell processes ended. Messages/follow-ups may arrive after a tool call.

Before another actor writes the same resource, observe completion/termination of the worker turn and known relevant process sessions, then inspect partial effects. Query only relevant session/process state. Never broadly kill unrelated work. If termination or effects remain unknown, reserve ownership and continue independent work; report blocked paths if needed.

Do not retry an external side effect with unknown completion. Use supported status/idempotency controls or resolve uncertainty first. Continue reversible preparation. Roll back only attributable task changes through safe supported procedures; never use broad reset. Preserve useful recoverable partial output where permitted.

## Completion and control

Verified means applicable criteria have adequate evidence on the final relevant state, material contradictions are resolved, and all known task-owned writers have completed or observably stopped. An unresolved known writer blocks a verified claim for its affected paths; do not demand proof about hypothetical unknown processes. Independent review is optional and cannot replace required behavioral checks.

For partial work, state completed outcomes, failed/unavailable checks, blocked dependencies, and minimum next action. A worker's done does not erase failure. Report tokens, cost, elapsed time, or concurrency only if observed; use unknown for missing telemetry. Prepare a concrete reviewable action before requesting approval when approval is the final blocker, citing the actual rule or rejection. Delegation never increases authority or bypasses a denied action.
