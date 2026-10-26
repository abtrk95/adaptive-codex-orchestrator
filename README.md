# Adaptive Codex Orchestrator

[![Checks](https://github.com/abtrk95/adaptive-codex-orchestrator/actions/workflows/ci.yml/badge.svg)](https://github.com/abtrk95/adaptive-codex-orchestrator/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/downloads/)

**A Codex skill for choosing when to work directly, when to delegate, and how to verify the integrated result.**

Keep one coordinator accountable. Give native workers bounded tasks and separate file ownership. Use parallel work when the inputs and interfaces are ready, then integrate and verify against the user's goal.

[Read the research report](https://abtrk95.github.io/adaptive-codex-orchestrator/) · [Download a release](https://github.com/abtrk95/adaptive-codex-orchestrator/releases/latest) · [Installation guide](docs/getting-started.md) · [Examples](adaptive-codex-orchestrator/references/examples.md)

> **Status: experimental v1.0.0.** This is an instruction-only community project, unaffiliated with OpenAI. Six recorded development smoke trials passed narrow functional and file-integrity checks. Relative speed, cost, production reliability, and superiority over direct execution have not been established. See [evidence and limitations](docs/evidence.md).

## What it does

- Chooses direct execution for small or tightly coupled tasks.
- Delegates independent investigations or implementations when useful.
- Defines worker objectives, ownership, constraints, and completion checks.
- Adapts to dependencies, changed requirements, failures, and stale evidence.
- Integrates serially and reports actual verification and unresolved limits.

The skill uses the native agent tools exposed by your Codex client. It does not add an agent runtime, call a model API, grant permissions, or enable unavailable tools. Without delegation support, it can still guide direct work. Model selection remains subject to the current client, instructions, and account access.

## Quick start

You need Git and Python 3.11+ for these commands, plus a Codex client that supports local skills. The installed skill itself has no Python or third-party package dependency.

```sh
git clone https://github.com/abtrk95/adaptive-codex-orchestrator.git
cd adaptive-codex-orchestrator
python3 scripts/install.py
```

On Windows, use `py -3` instead of `python3` if needed. The installer copies only the skill folder into `~/.agents/skills/adaptive-codex-orchestrator` and refuses to overwrite an existing destination. It does not change Codex configuration. Review the [skill instructions](adaptive-codex-orchestrator/SKILL.md) before installing.

In Codex, invoke it with a concrete task:

```text
$adaptive-codex-orchestrator Add CSV and JSON imports. Use native workers
for independent adapters where useful. Preserve the public API and verify
the integrated import flow.
```

For a repository-only installation, updating, removing, or configuring optional Terra workers, follow the [installation guide](docs/getting-started.md). If the skill does not appear, restart Codex.

## How it works

1. Establish the goal, acceptance checks, repository state, and available controls.
2. Choose the smallest useful strategy: direct work, focused investigation, or independent branches.
3. Assign bounded work with explicit ownership and completion conditions.
4. Revise the plan when new evidence changes dependencies, risk, or feasibility.
5. Integrate, run relevant checks, and finish with an evidence-based result.

Worker roles are responsibilities, not mandatory slots. Loading the skill does not automatically start workers. Current user instructions and permission boundaries always apply.

## What's included

| Path | Purpose |
| --- | --- |
| [`adaptive-codex-orchestrator/`](adaptive-codex-orchestrator/SKILL.md) | Installable skill, UI metadata, and seven focused references |
| [`config-examples/`](config-examples/README.md) | Optional local Codex settings and a Terra worker profile |
| [`evaluation/`](evaluation/evaluation-guide.md) | Four deterministic fixtures, grader, tests, and evaluation protocol |
| [`validation/`](validation/README.md) | Original pilot artifacts, provenance, and package validator |
| [`adaptive-codex-orchestration-report.html`](adaptive-codex-orchestration-report.html) | Self-contained research report, also available as a hosted page |
| [`docs/`](docs/getting-started.md) | Installation, compatibility, and evidence notes |

## Verify the package

From the repository root, with Python 3.11+:

```sh
python3 -B validation/validate_package.py
python3 -B -m unittest discover -s evaluation -p test_eval_suite.py -v
python3 -B evaluation/eval_suite.py self-test
python3 -B -m unittest discover -s tests -v
```

These checks validate packaging, the evaluator, and the installer. They do not execute a new native-agent benchmark or establish compatibility with every Codex client. The evaluator is for trusted disposable fixtures; its subprocesses are not a security sandbox. See the [evaluation guide](evaluation/evaluation-guide.md) before running submissions.

## Contribute

Bug reports, compatibility observations, and reproducible evaluations are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md), and use [Issues](https://github.com/abtrk95/adaptive-codex-orchestrator/issues) for public reports. Follow [SECURITY.md](SECURITY.md) for vulnerabilities.

Released under the [MIT License](LICENSE). OpenAI and Codex are trademarks of their respective owners. Referenced publications remain the property of their authors.
