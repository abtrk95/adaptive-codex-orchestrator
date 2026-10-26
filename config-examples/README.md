# Optional Codex configuration

These examples are optional and are not installed automatically. The skill can use your client's existing native controls and model selection.

- [`agents.config.toml`](agents.config.toml): a fragment for an existing local Codex configuration. It enables agents, sets explicit Terra defaults, and uses a sample ceiling of three open spawned threads, excluding the primary.
- [`terra-worker.toml`](terra-worker.toml): a standalone custom agent profile that explicitly requests `gpt-6.1-terra` and `medium` reasoning effort.

Review settings against your installed client and account access. Merge the fragment into `~/.codex/config.toml` or a trusted project's `.codex/config.toml`, without duplicating `[agents]` or replacing unrelated settings. A custom profile belongs under `.codex/agents/` in the project, or `~/.codex/agents/` for the user, where supported.

Copying a standalone profile and setting default subagent options are separate choices. Neither configures a hosted `collaboration.*` interface. Neither grants model access, increases managed limits, or bypasses instructions that prohibit delegation.

See official [subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents) and the [compatibility notes](../docs/compatibility.md). TOML syntax checks are not proof of successful local profile execution.
