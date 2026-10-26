# Evidence and limitations

## What the original package records

Six final development trials produced outputs that passed the supplied functional and protected-file checks:

| Trial | Work pattern |
| --- | --- |
| `tiny-A` | Direct execution control |
| `tiny-B` | Two fixed read-only workers, with coordinator edits |
| `tiny-C-final` | Adaptive skill chose direct execution |
| `parallel-C` | Two requested workers plus coordinator implementation |
| `dependency-C-v2` | Direct execution for a small coupled pipeline |
| `refactor-C` | Direct execution for a small shared-function extraction |

The original [provenance](../validation/provenance.json), [records](../validation/pilot-records.jsonl), [curated native observations](../validation/native-observations.json), and [pilot artifacts](../validation/pilot/) are included. The [research report](https://abtrk95.github.io/adaptive-codex-orchestrator/) discusses the sources, architecture, and evidence in detail. It is also [available offline](../adaptive-codex-orchestration-report.html).

## What those results do not establish

- The trials were development smoke tests, not a randomized, matched comparative benchmark.
- Complete raw native event exports and exact initial control prompts were not retained.
- The parallel trial explicitly requested workers, so it does not demonstrate autonomous selection of optimal fan-out.
- Comparable end-to-end timing, tokens, cost, and peak utilization were unavailable. Grader subprocess timing is not agent latency.
- Four small synthetic task families do not establish scalability, production reliability, or superiority over another workflow.
- Failure injection, cancellation races, hostile submissions, long-session context loss, and local custom-role deployment were not tested.

Repeatedly grading a saved output confirms that artifact against the current grader; it is not a new agent trial. Running evaluator self-tests checks the evaluator, not the orchestration policy.

## Public packaging

The original installable skill tree remains unchanged, with SHA-256:

```text
581cb9bc1f13e4a330161f153fded7f6062003e951ebd8627de6d37fcd404e50
```

The standalone HTML report and the report in the supplied archive were byte-identical. Its SHA-256 is:

```text
bc7c14358bec98ca4bcd2207da1054ff8a3f64146c617a321ef802397eaa73b9
```

This public release adds installation and contribution docs, licensing, an installer with tests, CI, and a report publishing workflow. `SHA256SUMS.txt` is regenerated for the public repository contents. Historical validation JSON files retain their original claims and dates; they are not records of the new GitHub publication or new native trials. The commit hash mentioned in them belongs to the original development context.

For a stronger evaluation, follow the [evaluation guide](../evaluation/evaluation-guide.md) with larger independently authored tasks, secured hidden checks, actual native runs, and complete resource telemetry. Publish failed runs and missing measurements alongside passes.
