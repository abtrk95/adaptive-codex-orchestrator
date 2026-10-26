# Native orchestration evaluation guide

This package contains four deterministic local coding fixtures, a grader, and a descriptive record summarizer. It does **not** invoke an agent, run native workers, collect runtime telemetry, or prove the adaptive skill works. Run actual trials separately through the native runtime. Results from these small synthetic fixtures alone do not establish performance on real repositories.

**Before executing submissions:** use an independent OS sandbox for untrusted code. A copied workspace and a subprocess timeout do not isolate filesystem/network access or terminate every descendant. The smoke tests authored here use benign disposable fixtures; they are not hostile-code security tests.

## Quick start

From this directory, with Python 3:

```sh
python -B -m unittest -v test_eval_suite.py
python -B eval_suite.py self-test
python -B eval_suite.py prepare --fixture tiny --out /tmp/orchestration-trial-a
# Give the agent only /tmp/orchestration-trial-a/workspace.
# Execute its native trial independently, then:
python -B eval_suite.py grade --case /tmp/orchestration-trial-a --timeout 5
python -B eval_suite.py summarize --records /tmp/trials.jsonl
```

Use a new output directory for each trial; preparation refuses existing nonempty directories. The fixture names are `tiny`, `parallel`, `dependency`, and `refactor`. A public smoke test and task instructions are in each workspace. Run the public tests with `python -B test_public.py`. Interpreter `__pycache__` directories are allowed and excluded from the grader copy. Empty extra directories are permitted; this is a file-content integrity check, not a proof that the entire directory tree is unchanged. The grader permits edits only to the implementation files named in the generated manifest, requires all initial files to remain present, rejects unexpected files and symlinks, and verifies protected files against independently reconstructed original hashes before and after submission execution. TASK.md states the writable files and protected-file rules. The grader loads no submission code in its own process: it first copies the workspace and executes checks in a subprocess with a timeout. It exits 0 for a pass, 1 for a failed grade and 2 for invalid CLI input. It reports timeout as a failure. The self-test uses the bundled reference mutations only for checking the grader, never as a trial setup.

**Isolation:** Python subprocesses and copying are not a security sandbox. An independent OS sandbox/container with no network, restricted filesystem, bounded CPU, memory, processes and storage, and process-tree cleanup is required for untrusted or hostile submissions. A subprocess timeout alone may not stop grandchildren or prevent system access. Make the grader and hidden checks inaccessible to the agent during a trial; they are in `eval_suite.py`, so mount only the workspace. The executable code itself is not a secret, and a knowledgeable agent could infer the test cases if it has previously seen this package. Do not claim rigorous holdout protection without separately secured hidden tests. Keep the manifest outside the workspace. Inspect grader output and preserve logs.

## A/B/C protocol

Freeze and hash this package, the skill, the task prompt, runtime version, models and configuration before the experiment. For each fixture, create three separately prepared identical workspaces, labeled A, B and C, and run in randomized balanced order. These fixtures have no generated seeds or meaningful variants: repeating the same fixture produces an identical task, not an independent task variant. Record the randomization seed and repeat fresh agent trials where resources permit; report task-level results and repetitions explicitly. A small four-fixture demonstration cannot support general statistical claims.

Delegation in B and C must be authorized by the current host and user request; the evaluation protocol cannot override a higher-priority restriction. Record an unavailable arm rather than bypassing it.

Give all arms the **same** task in `TASK.md`, workspace files, root model, runtime settings, available tools, deadline, total budget, environment and finish instruction. Set the intended native worker model to `gpt-6.1-terra` for both B and C if supported; record the actual root and worker model, reasoning settings, tool access and runtime. Count all root and worker consumption against the same total cap. Record whether each cap is enforced, observed only, or unavailable. Use isolated copies with equivalent hardware and cache state. Do not disclose arm or grader internals as task-specific hints.

- **A, direct:** prohibit worker spawning and have the root solve and verify the task.
- **B, fixed:** instruct the root at the outset to start two native workers, within the common cap. Assign independent diagnosis or disjoint work; root integrates and verifies. On shared-file tasks workers should report findings or proposed patches rather than concurrently overwrite the same file. If the cap prevents two, record the deviation rather than exceeding it.
- **C, adaptive:** enable the candidate instruction-only skill. The root chooses whether and how to use native workers within the same cap, including zero workers.

Use `prompt_hash` for the shared TASK.md content, and record separate `arm_instruction_hash` and `config_hash` for the deliberately different control instructions and configuration. Skill activation and orchestration instructions are the intervention; the underlying task stays identical.

For each run, record the actual prompt and skill hashes, timestamps, native worker events and outcomes, resource records, final patch, grader result, exceptions and environment. Run the grader after the trial against the submitted workspace. Do not fix failures before grading. Score all trials including failures, deadlines and worker errors. Only exclude predeclared infrastructure failures that prevented the agent from starting; preserve evidence and report exclusions by arm. The actual model's random seed is unknown unless the runtime exposes one; schedule seeds do not seed model behavior.

## Fixture coverage and remaining scenarios

| Scenario | Status and intended evidence |
|---|---|
| Tiny one-file bug | Implemented: inclusive range with hidden edge cases. |
| Multi-module feature | Implemented through dependency fixture: schema, service and API contract. |
| Large behavior-preserving refactor | Implemented as a **small** proxy: shared fee function and differential behavioral checks. It is not a large-repository test. |
| Unfamiliar repository | Conceptual/live: sparse docs and misleading entry point, with independently authored integration checks. |
| Intermittent bug | Conceptual/live: deterministic interleaving plus repeated stress; measure reproductions and flakes. |
| Conflicting findings | Conceptual/live: plausible competing diagnoses; verify root reconciles evidence and final integration passes. |
| Failed worker | Conceptual/live: inject and log an eligible worker failure, score recovery; distinguish nonactivation and apply comparable fault exposure where feasible. |
| Dependency-heavy work | Implemented: a sequential schema-to-service-to-API change. |
| Highly parallel work | Implemented as a **small** proxy: three independently editable adapter modules with a protected dispatcher and a specified parsing contract. |
| Incomplete requirements | Conceptual/live: consequential ambiguity and controlled user response; accept justified clarification. |
| Strict resource bound | Conceptual/live: externally enforce limits and record peak concurrency and complete consumption; unknown telemetry is not compliance. |
| Destructive operation | Conceptual/live: isolated disposable data, approval gate and sentinel integrity; safe clarification can be success. |

The eight conceptual/live scenario labels are unfamiliar repository, intermittent bug, conflicting findings, failed worker, incomplete requirements, strict resource bound, destructive operation, and a genuinely large refactor. The latter extends the implemented small refactor proxy. A broader multi-module feature and a truly highly parallel multi-file task also need larger fixtures before claiming representative coverage.

## Records and measures

Manually create one JSON object per actual trial in UTF-8 JSONL. Required nonempty strings are `trial_id`, `fixture`, `arm` (`A`, `B`, `C`), `model`, `runtime`, `fixture_hash`, `prompt_hash`, `skill_hash`, and `outcome` (`pass`, `fail`, `unknown`). Use the literal `disabled` for arms A and B, where the candidate skill is disabled; retain actual hashes in provenance storage. Optional `wall_seconds`, `tokens`, and `cost` are nonnegative numbers or `null`; omit them if unavailable. For example, the following illustrates schema only and is **not a trial result**:

```json
{"trial_id":"example-id","fixture":"tiny","arm":"A","model":"example-model","runtime":"example-version","fixture_hash":"example-hash","prompt_hash":"example-hash","skill_hash":"disabled","outcome":"unknown","wall_seconds":null,"tokens":null,"cost":null}
```

The summarizer counts outcomes by arm and reports observed metric counts and sums; missing values remain unknown, never zero. It does not verify hashes or claim that records represent actual runs. Keep grader output and runtime evidence with each record, and manually verify matching, provenance and budget compliance. Use elapsed monotonic time from start to completion or stop; total tokens must include root and workers without double counting; cost must be actual billing or an identified estimate with rate card and currency. Report safety and cap violations and telemetry coverage separately. Do not treat unavailable telemetry as a pass.

The primary metric is the share of all assigned trials passing functional, integrity, safety and enforceable budget checks. Report unknown separately and conservatively count it as unsuccessful when calculating success rates. Compare speed and cost only after correctness, report denominators and success rates beside conditional distributions, and include failed-run resources in any cost per successful trial. This tool's `outcome` is a manually recorded judgment and does not itself establish safety, budget compliance, matched comparisons, confidence intervals or causal effect. Analyze matched instance outcomes and failures externally; do not mix hypothetical policy simulations with actual native results.

## Future benchmark procedure

1. Independently author and validate larger fixtures and secured hidden checks. Verify each original fails, a reference passes, and plausible wrong solutions fail. Freeze sources, hashes, grading, arm instructions and analysis before confirmatory work.
2. Prepare isolated matched workspaces; randomize run order; configure equal enforceable resource limits and pinned runtime/models. Record schedules, hardware and versions. Prevent workers from accessing other arms and hidden checks.
3. Run actual A/B/C agents through native runtime; preserve raw events, final patches and all failures. Record whether a worker-failure injection actually fired. Do not replace failed trials selectively.
4. Grade each final workspace in an independent OS sandbox, assess safety and limits, and write one truthful JSONL record per trial. Summarize with the command above, check data coverage and matching, and publish per-fixture outcomes before any aggregate.
5. For a larger preregistered suite, compare paired correctness first, with uncertainty calculated at task-family level; present conditional performance and resource metrics only with success rates and missingness. Report changes, deviations and limitations. Rerun when the skill, model, runtime or evaluator changes.
