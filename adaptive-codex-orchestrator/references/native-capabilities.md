# Native capabilities and compatibility adapters

Checked against official documentation and the authoring session on 2026-10-26. Recheck when the current host differs. These are distinct surfaces; do not transplant parameters between them.

## Capability gate

Identify actual spawn/message/follow-up/status/wait/stop operations, model selection, context inheritance, active/open-thread limits, filesystem sharing, and approvals. Live schemas are the execution contract. Public documentation does not establish account entitlement. Do not inspect credentials to resolve availability.

If native delegation is absent, do useful work directly and disclose the limitation. Do not replace it with API calls, CLI loops, or a framework. Loading the skill supplies instructions; the coordinator must make real authorized tool calls.

## Observed hosted collaboration adapter

These names were exposed in the authoring conversation, not promised in every client:

| Operation | Observed behavior |
| --- | --- |
| `collaboration.spawn_agent` | task_name, message, optional fork_turns/model/reasoning_effort; returns canonical task name. |
| `collaboration.send_message` | Queues information without triggering an idle agent. |
| `collaboration.followup_task` | Restarts idle work; delivery to running agents follows boundaries. |
| `collaboration.list_agents` | Reports team status for capacity/state clarification. |
| `collaboration.wait_agent` | Waits for updates; summary is not completion evidence. Read actual returned messages. |
| `collaboration.interrupt_agent` | Interrupts a turn and returns prior status; not subprocess-termination proof. |

Agents shared filesystem and working directory. The session allowed four active agents including the primary and exposed no close-agent tool. These are observations, not skill defaults. Collaboration calls were direct, outside the JavaScript orchestration namespace.

An authorized Terra request used this host-specific shape:

```json
{
  "task_name": "inspect_parser",
  "fork_turns": "none",
  "model": "gpt-6.1-terra",
  "message": "Inspect src/parser.py and its tests for the supplied boundary failure. Read-only; no child agents. Return exact symbols, evidence, uncertainty, and the smallest relevant check. Follow the supplied task constraints."
}
```

Supply the real task context first. Here `fork_turns="all"` inherited parent model/effort and disallowed overrides; `"none"` permitted overrides but omitted conversation history. Do not add agent_type, cwd, max_tokens, sandbox, timeout, or close flags unless exposed by the current schema.

## Documented local Codex adapter

Merge optional settings into existing `~/.codex/config.toml` or a trusted project's `.codex/config.toml`; do not overwrite files or duplicate tables. These do not configure the hosted adapter.

```toml
[agents]
enabled = true
default_subagent_model = "gpt-6.1-terra"
default_subagent_reasoning_effort = "medium"
max_concurrent_threads_per_session = 3
```

Three is an example ceiling, not a target. The documented cap counts open spawned threads excluding the primary; omission lets Codex choose. `max_threads` is a legacy alias. Configure the primary separately. Avoid obsolete feature-flag recipes unless the installed version requires them. [Configuration reference](https://developers.openai.com/codex/config-reference).

Optional standalone profile, `.codex/agents/terra-worker.toml` or `~/.codex/agents/terra-worker.toml`:

```toml
name = "terra_worker"
description = "Complete one bounded software task and return artifacts and evidence."
model = "gpt-6.1-terra"
model_reasoning_effort = "medium"
developer_instructions = """
Follow the coordinator's contract and inherited permissions.
Own only assigned files/resources and preserve user changes.
Do not spawn children without an explicitly allocated subtree.
Report changes, checks/results, unverified claims, and blockers.
"""
```

Custom-file model/effort takes precedence over pre-resolved spawn/default/parent settings. Parent permissions, provider, and MCP configuration remain inherited. A read-only instruction is not an isolated sandbox. [Subagents](https://developers.openai.com/codex/subagents). Verify the installed role and version before relying on precedence.

## Model and validation limits

OpenAI publishes `gpt-6.1-terra`, released 2026-10-26. The authoring session accepted explicit native selection of that ID and returned completed workers. This establishes interface invocation, not backend attestation, universal access, or a local custom-profile test. [Model](https://developers.openai.com/api/docs/models/gpt-6.1-terra); [release](https://developers.openai.com/api/docs/changelog).

The API model page and hosted tool described different effort defaults/options: API medium versus hosted low. Do not assume options transfer; omit overrides unless useful. Medium was listed on both observed surfaces.

The local binary reported `codex-cli 0.159.2`. A strict-config/features-list attempt was rejected because that subcommand does not support strict-config; it neither validates nor invalidates these fields. TOML parsing checks syntax only. Hosted native tests do not prove local-client deployment or profile behavior.
