# Installation and use

## Requirements

- A Codex client that supports local skills.
- Native delegation tools if you want worker-based execution. Their availability depends on the client, account, and current instructions.
- Python 3.11+ for the installer and validation tools. No pip packages are required.
- Git for cloning, or a ZIP downloaded from [Releases](https://github.com/abtrk95/adaptive-codex-orchestrator/releases).

The skill consists of Markdown and UI metadata. It has no background process, API key requirement, or separate agent runtime. Any agents you use consume your normal Codex resources.

## Install for your user

Review [SKILL.md](../adaptive-codex-orchestrator/SKILL.md) and its references first. From an extracted release or clone:

```sh
python3 scripts/install.py
```

This copies `adaptive-codex-orchestrator/` into `~/.agents/skills/adaptive-codex-orchestrator`. An existing file, folder, or symlink at that destination causes the installer to stop without replacing it. On Windows, `py -3 scripts/install.py` is an alternative.

Codex's documented user and repository skill locations are described in [Build skills](https://learn.chatgpt.com/docs/build-skills). If your client uses a different discovery location, pass its skills parent directory with `--dest`.

## Install for one repository

Choose an absolute path to the target repository's skills directory:

```sh
python3 scripts/install.py --dest /absolute/path/to/your-repo/.agents/skills
```

Run Codex in that repository. You can commit the installed skill folder to share it with collaborators. If you have both user and repository copies, remove the unwanted copy to avoid duplicate entries.

## Install by asking Codex

If your Codex client includes the Skill Installer skill, you can give it this prompt:

```text
Use $skill-installer to install the skill from
https://github.com/abtrk95/adaptive-codex-orchestrator/tree/main/adaptive-codex-orchestrator
```

This follows the installer available in that client; its destination may differ from the manual installer above.

## Use the skill

Open your project in Codex and provide a concrete outcome:

```text
$adaptive-codex-orchestrator Investigate duplicate jobs. Preserve existing
changes, use independent native investigations where useful, and verify
the smallest supported fix.
```

For a small change, direct execution is a valid result. To request a particular worker model, name it explicitly and ensure your account and client support it:

```text
$adaptive-codex-orchestrator Implement the independent CSV and JSON adapters
with native gpt-6.1-terra workers where useful. Keep registry integration
under one owner and test the integrated result.
```

For a resource limit, make it explicit, for example: `Use at most one native worker.` The skill must follow current instructions even when they prohibit delegation. See [more examples](../adaptive-codex-orchestrator/references/examples.md).

## Optional agent settings

No configuration changes are required to install the skill. To customize local delegation, see [configuration examples](../config-examples/README.md) and [compatibility notes](compatibility.md). Merge settings manually into the correct existing tables. Do not replace your configuration with an example file.

## Update

Download the new release or run `git pull --ff-only` in your clean clone. Review the [changelog](../CHANGELOG.md). Move your installed skill folder to a backup outside the skills discovery directory, then rerun the installer. It deliberately has no overwrite option.

Do not leave a backup containing `SKILL.md` under a scanned skills folder, because Codex may discover both copies.

## Remove

Delete only the installed `adaptive-codex-orchestrator` folder from the destination you chose. If you manually added optional agent configuration or a custom worker profile, remove those specific additions separately.

## Troubleshoot

| Symptom | Next step |
| --- | --- |
| Skill does not appear | Check the destination contains `adaptive-codex-orchestrator/SKILL.md`, then restart Codex. |
| Installer reports an existing destination | Inspect and back up the existing installation outside the discovery directory before updating. |
| Workers are unavailable | Check current client capabilities and instructions. Continue direct work; the skill cannot enable missing tools. |
| Terra selection fails | Verify the exact model is available to your account and native runtime. Do not silently substitute another model. |
| TOML parses but a setting is rejected | Consult your installed client's schema and the current official configuration documentation. Syntax checks do not prove runtime support. |

For reproducible issues, include your client/version, operating system, installation scope, relevant sanitized settings, expected behavior, and observed output. Do not include credentials or private conversation content.
