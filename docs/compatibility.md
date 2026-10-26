# Compatibility

This release preserves the original skill and report from 26 October 2026. Native tools, account access, model options, and configuration schemas can change independently of this repository.

| Component | Evidence and boundary |
| --- | --- |
| Skill format | `SKILL.md`, relative references, and `agents/openai.yaml` are included. The package validator checks basic structure and essential metadata strings. |
| Local installation | The installer targets the documented `~/.agents/skills` location by default and accepts another skills parent with `--dest`. It does not activate tools or configure models. |
| Native workers | The original authoring session completed explicit native worker requests. Its `collaboration.*` tool names are host-specific examples. Use the live tool schema in your client. |
| Worker models | Preserve the user's explicitly requested model. Otherwise, use the current client's selection and inheritance rules. Terra is an optional profile, not an installation requirement. |
| Local custom agent profile | The included TOML examples are syntax-checked. Local profile execution and universal account access have not been validated. |
| Limits and permissions | Current instructions and runtime controls govern delegation, shared files, approvals, and capacity. The skill does not expand them. |
| Evaluation tooling | Python 3.11+; standard library only. Fixtures and the grader are not an agent runner or an OS sandbox. |

The original preflight recorded `codex-cli 0.159.2`; that is historical provenance, not a tested minimum version or a recommendation to install that version. Hosted worker observations and local CLI configuration are separate evidence.

For current setup, consult official [skill discovery](https://learn.chatgpt.com/docs/build-skills), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), and the [configuration reference](https://developers.openai.com/codex/config-reference). These links were checked for the public packaging on 26 October 2026. Public documentation does not establish access for a particular account.

See [native capabilities](../adaptive-codex-orchestrator/references/native-capabilities.md) for the original adapter details. If those examples differ from the live schema, follow the live schema and record the difference in an issue.
