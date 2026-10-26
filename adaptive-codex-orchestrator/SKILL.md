---
name: adaptive-codex-orchestrator
description: Adaptively plan, delegate, integrate, and verify complex software work using Codex's existing native agents, including explicitly selected GPT-6.1 Terra workers. Use when asked to orchestrate agents, parallelize independent work, coordinate a multi-module implementation, investigate competing bug hypotheses, or manage substantial work with dependencies. Keep tiny or tightly coupled tasks direct. This skill supplies coordination policy, not a new agent runtime.
---

# Adaptive Codex Orchestrator

Keep Codex accountable for the user's objective, integration, evidence, and final answer. Treat scout, implementer, and verifier as responsibilities; perform them yourself or delegate only where useful. Use the exposed native tools. Do not create a framework, spawn a replacement CLI swarm, or assume that loading this skill executes anything automatically.

## 1. Establish the task and available controls

Read applicable instructions and the relevant repository state. Preserve existing edits. Identify the required outcome, material unknowns, acceptance checks, risky actions, dependencies, and useful independent work. Infer routine choices; ask only if an essential decision or actual authorization boundary blocks progress. Continue unaffected authorized work.

Before delegating, establish that current instructions allow it and inspect the live agent surface: spawn/follow-up/wait/status/stop behavior, model selection, context inheritance, shared files, capacity, and permissions. Existing user authorization suffices. If the surface is unfamiliar, read [native capabilities](references/native-capabilities.md). Its examples are host-specific, not universal APIs.

Use the worker model explicitly requested by the user. For the Terra 6.1 profile, request `gpt-6.1-terra` only through a verified native selection field or configured agent. This profile requests that explicit selection subject to the host's authority. Preserve another explicitly requested model. Never silently substitute, infer selection from prose, or claim account access from public model documentation. If selection is unavailable, do useful coordinator work and disclose the limitation; ask about a replacement only when needed. Set reasoning effort only when supported and justified.

## 2. Select the smallest useful strategy

| Observable situation | Initial strategy |
| --- | --- |
| Small change, clear fix, tightly coupled work, or no useful worker output | Execute directly. |
| Bounded research or exploration would isolate substantial context | Delegate one focused investigation; continue complementary work. |
| Several outputs have stable interfaces and independent inputs/write sets | Fan out only ready branches, then integrate. |
| Later decisions depend on earlier discoveries | Use short stages; parallelize only independent preparation. |
| Bug cause is uncertain and hypotheses have different discriminating checks | Investigate a bounded set of distinct hypotheses, then choose by evidence. |
| Consequential change has residual risk a separate check can address | Add focused independent verification. |

Use [orchestration policy](references/orchestration-policy.md) for ambiguous routing, budgets, or replanning. Do not compute a universal complexity score, spawn one worker per role, or require debate. Parallel shell reads may be sufficient without another agent.

For substantial work, keep a compact coordinator-owned record: acceptance criteria, tasks/dependencies, owner/write set, state, evidence, remaining dispatch/recovery allowance, and next action. Use existing planning facilities or an authorized scratch file; do not add bookkeeping files for a tiny task. See [architecture](references/architecture.md) for lifecycle semantics.

## 3. Delegate ready work with a bounded contract

Dispatch only when the result can be evaluated, useful work can overlap or context isolation helps, ownership is safe, and benefit plausibly exceeds startup and integration cost. Prefer the critical path. Reuse a suitable idle worker when its context remains valid; use a fresh context when independence or stale assumptions matter.

Give each worker objective, relevant context, concrete output, boundaries, and completion conditions. For changes or dependent tasks, also supply the task revision, relevant baseline, dependencies/interface contract, exact write ownership, checks, and escalation conditions. Use [delegation protocol](references/delegation-protocol.md); scale its template to the task. A fresh worker needs all necessary user constraints and permission limits explicitly. Do not dump the entire conversation.

Count free capacity using this host's actual semantics, including other active work and any open-thread limits. Never treat an example cap as a target. If capacity is unknown, attempt at most one worker until verified; handle a rejected spawn without repeated retries until capacity or the request changes. Set the phase's dispatch and recovery allowance before fan-out; revising the plan does not erase consumption. Workers must not spawn children unless you explicitly allocate a bounded subtree and shared budget.

Reserve each mutable file or resource to one owner at a time, including yourself, generated outputs, lockfiles, shared fixtures, ports, and databases. In a shared workspace, use disjoint write sets and stable shared interfaces. Use isolated worktrees only when available and appropriate; they do not isolate external services. Read-only work also needs a stable input or a recorded revision. Do not concurrently integrate a worker's unfinished edits.

## 4. Monitor and adapt from evidence

Work on an independent useful task while workers run. Prefer native completion notifications. Check status at a meaningful milestone or ambiguity; silence alone is not failure. Wait only when no useful independent action remains, in intervals that preserve the host's user-update requirements. Send concise progress updates during substantial work.

Replan when evidence changes requirements, assumptions, dependencies, ownership, risk, or feasibility. Group nonurgent changes. Send affected workers a revisioned update; require acknowledgment when safety depends on it. Messages and interruptions may not stop an in-flight command.

Treat worker completion as **returned**, not verified. Inspect outputs and their scope, freshness, changed files, and checks. Resolve contradictions with a discriminating test or primary evidence; consensus and confidence are insufficient. Preserve valid partial work. Read [verification and recovery](references/verification-and-recovery.md) when failures, conflicts, or significant uncertainty arise.

## 5. Integrate, verify, and stop honestly

Integrate serially against the actual baseline, preserving user edits and accounting for untracked or nongit files. Verify the final relevant state against acceptance criteria with the smallest meaningful checks: reproduction, tests, type/build checks, integration, or targeted inspection. Apply existing required gates. Add review when its expected value addresses a concrete risk; do not run every test or create tests for every reversible edit.

Record commands, working directory, result/exit, evidence paths, and tested revision when applicable. Distinguish passed, failed, unavailable, and not run. Recheck only evidence affected by later changes. Read [context management](references/context-management.md) before a long handoff or checkpoint.

Allow at most one unchanged retry for a plausible transient failure. After two attempts without new evidence or progress, stop repeating that approach: narrow scope, change hypothesis, take over directly, or report the blocker. Respect actual hard limits; conserve useful work within soft estimates. Do not reassign an overlapping write set until the previous writer and relevant subprocesses are observably stopped; if this cannot be established, keep it blocked.

Finish when applicable acceptance criteria have adequate current evidence and all known task-owned writers have completed or observably stopped. If a known writer's state is unresolved, keep its paths reserved and label the affected result partial or blocked. Explicitly close/stop workers only through available controls; no invented cleanup calls. If a required check or outcome remains unresolved, deliver a precise partial or blocked result, not a success claim. Report outcome, material changes, verification, and remaining limits concisely. Do not promise autonomous cross-session learning.

## Reference map

- [Native capabilities](references/native-capabilities.md): host adapters, Terra selection, configuration, and permission differences.
- [Architecture](references/architecture.md): task lifecycle, accountable ownership, and dependency records.
- [Orchestration policy](references/orchestration-policy.md): decomposition, allocation, budgets, and evidence-triggered adaptation.
- [Delegation protocol](references/delegation-protocol.md): assignment, return, revision, and failure contracts.
- [Context management](references/context-management.md): selective context, evidence freshness, checkpoints, and memory limits.
- [Verification and recovery](references/verification-and-recovery.md): integration, risk-based checks, failure classes, and cancellation safety.
- [Examples](references/examples.md): representative task applications and invocation prompts.
