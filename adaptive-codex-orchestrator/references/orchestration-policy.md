# Routing, allocation, and adaptation

## Routing questions

Identify task type, uncertainty, coupling, risks, checks, and parallelism from actual artifacts, without an unexplained complexity score:

1. What observable outcome satisfies the request, and what evidence distinguishes success from a plausible attempt?
2. What must be learned first? Which unknown changes behavior, architecture, authorization, or verification?
3. What outputs have independent inputs/write sets? Where are shared interfaces, generated files, or external mutable resources?
4. Would delegation shorten the critical path, isolate substantial noisy context, or provide valuable scrutiny after integration cost?
5. Can the coordinator understand and check returned work within the remaining attention/time budget?

If questions 4 or 5 have no useful answer, work directly. Follow any applicable instruction requiring a particular delegation mode without inventing additional roles.

## Strategy selection

| Strategy | Choose when | Change course when |
| --- | --- | --- |
| Direct tool-grounded execution | Small, sequential, or strongly coupled task | A useful independent branch appears. |
| One investigation | Large noisy search has a concise valuable output | Work overlaps the coordinator or produces no actionable evidence. |
| Short stages | New facts determine the next step | An interface stabilizes enough for independent downstream work. |
| Fan-out/fan-in | Clear independent workstreams with affordable integration | Contract churn, conflicts, rate limits, or reviewer saturation appear. |
| Explore, evaluate, implement | Alternatives change consequential tradeoffs | One approach has decisive evidence; stop alternatives. |
| Bounded hypotheses | Different checks can distinguish difficult causes | Causes converge or shared test state interferes. |
| Implement plus focused verifier | Residual correctness/security/compatibility risk warrants scrutiny | Review only repeats assertions or has no distinct check. |
| Shallow hierarchy | A substantial independent subtree has a contract and budget | Cross-subtree dependencies grow; flatten the work. |

Initial planning stops when the next safe useful action, owner, and check are clear. Revisit on new evidence or a meaningful milestone, not merely to improve the plan's appearance.

## Decomposition

Partition by coherent deliverable and verification boundary, not equal file counts, personas, or tokens. Keep tightly coupled changes together. Assign shared interfaces and lockfiles once. For an unfamiliar codebase, ask a bounded scout question such as locating the actual request path and tests rather than understanding everything.

Independent preparation can proceed before a dependency finishes: inspect consumers, identify tests, or implement against an explicit frozen contract. Do not call speculative dependent output complete. If a branch cannot state its input/output contract, investigate or merge it before editing.

## Concurrency and value

Useful worker count cannot exceed the minimum of ready independent tasks, actual free capacity, safe ownership partitions, coordinator integration capacity, and remaining resources. This constraint is not a target to fill.

Count primary, active workers, idle/open threads, and descendants exactly as the host counts them. An active-slot budget and a local open-thread cap differ. Reuse valid idle context; close only if a real tool supports it. Never raise limits or alter global settings to bypass a task boundary.

Compare saved critical-path effort or useful verification against context/setup, duplicate investigation, waiting, conflict, and integration cost. Do not fabricate estimates. Add a worker for a specific valuable output. Reduce concurrency when contracts change, workers wait on one dependency, tests contend, or outputs arrive faster than the coordinator can check them.

## Resource envelope

Before substantial fan-out, record the current independent branches and a bounded recovery allowance, normally one corrective delegation for that phase. Track starts and corrective follow-ups across revisions. Extra work requires an identified new deliverable or changed evidence and remaining budget; renaming tasks does not reset consumption. Descendants share the root's envelope.

Honor explicit deadlines, token/tool limits, model constraints, and slot caps. Label them host-enforced, observable only, or unavailable. A prompt cannot hard-enforce token usage or cancellation. With no user cap, choose a conservative phase size, reserve integration/verification time, and revisit after the next result rather than dispatching a speculative graph.

Under pressure, remove speculative branches and repeated reviews first; preserve required correctness checks. Prefer a verified core result with precise omissions over broad unverified completion. An estimate alone is not a reason to abandon useful authorized work.

## Replanning and termination

Replan when a requirement changes, an assumption fails, a dependency appears, a branch blocks/fails, ownership collides, or remaining work threatens a real limit. Record the new fact, affected tasks, smallest change, and confirming check. Preserve unaffected work. Group nonurgent updates; avoid interrupting productive agents repeatedly.

After two no-progress attempts on the same issue, do not repeat the same prompt, check, or role. Seek a discriminating observation, narrow scope, change strategy, take over directly, or mark the branch blocked. Planning without a new observation counts as no progress. A fresh team is not a remedy for an unchanged question.

Stop spawning when work becomes serial/integrative, assignments are too small, useful parallelism ends, results cannot be checked in time, or a real limit would be exceeded. Finish when acceptance is verified, or report a precise partial/blocked result when a specific boundary prevents further useful authorized work.
