# Architecture and lifecycle

## Ownership

The coordinator owns requirements, task graph, boundaries, evidence reconciliation, integration, and final status. A worker owns a bounded deliverable. It may explore, implement, or verify; a role label does not require a separate agent. Give an independent verifier criteria and raw artifacts rather than the author's preferred conclusion.

This is an instruction policy over existing tools. Its task record does not provide a scheduler, file lock, transaction, durable execution, automatic cancellation, or exactly-once side effects.

## Smallest useful state

For a short task, track goal, check, and result in context. For several workstreams, maintain a coordinator-owned table in an existing planning location or authorized scratch directory. Workers must not concurrently edit the ledger.

| Field | Meaning |
| --- | --- |
| Acceptance | Observable required outcomes; use IDs when they improve traceability. |
| Task/revision | Stable assignment ID and revision when scope or contract changes. |
| Dependencies | Prerequisite artifact/interface and evidence permitting downstream work. |
| Owner/write set | One responsible actor and exact files/resources it may change. |
| State | Lifecycle value below; a returned claim is not verification. |
| Evidence | Artifact/check, baseline/current revision, unresolved assumptions. |
| Envelope | Slots, dispatch/recovery allowance, hard limits and soft estimates. |
| Next action | Concrete action, owner, and condition for doing it. |

Example: `T2 r1 | A2 | needs C1 | worker-normalizer | src/normalize.py | running | baseline: relevant hashes in snapshot.json | return patch and targeted checks`.

Keep dependencies acyclic within a plan revision. If tasks need each other's final results, assign their shared interface first or merge them. Plan changes preserve completed valid work and cumulative resource counters.

## Lifecycle

| State | Entry evidence | Next action |
| --- | --- | --- |
| Planned | Outcome and scope identified | Clarify dependency/ownership, or make ready. |
| Ready | Inputs exist, ownership is free, usable interface agreed, including a recorded provisional contract | Execute/delegate if useful and permitted; revalidate changed assumptions. |
| Running | Actual dispatch or coordinator execution started | Observe, revise, or safely stop. |
| Returned | Worker produced output, even if it claims success | Inspect scope, artifacts, and evidence. |
| Integrating | Contribution accepted for integration | Apply/inspect changes and check interactions serially. |
| Verified | Applicable criteria have current adequate evidence | Release dependents or finish. |
| Blocked | Missing dependency, authorization, capacity, or writer termination | Preserve output; continue other branches; resolve blocker. |
| Failed | Attempt cannot meet its contract | Diagnose and choose bounded recovery. |
| Cancelled | Task intentionally ended and writing has stopped | Retain useful evidence; remove from active plan. |

An interrupt request is not evidence for cancelled. Until writing stops, mark the task blocked/stopping and retain ownership.

## Dependency release

Release implementation when its immediate contract is stable enough; do not require upstream end-to-end verification before downstream code exists. Agree a request schema, permit separate validator and consumer work, then verify their real integration. Label provisional assumptions and give the shared interface one owner. A changed contract invalidates affected downstream work; notify owners and recheck relevant evidence.

## Boundaries

Keep coordination primarily centralized. A relevant peer update is permitted when the interface allows it and ownership stays accurate; it cannot expand scope or grant authorization. Use a second decomposition layer only for a substantial independent subtree with root-allocated budget, ownership, and integration responsibility. One layer is the default. A worker must not recursively invoke this skill to manufacture a team.

The coordinator delivers verified, partial, or blocked status. Successful task execution is the objective; perfect-looking bookkeeping is not an acceptance condition.
