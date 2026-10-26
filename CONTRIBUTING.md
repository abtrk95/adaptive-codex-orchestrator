# Contributing

Start with a small, reproducible issue or a focused pull request. Describe the problem, the expected behavior, and the smallest change that addresses it. Include your Codex client/version and operating system for compatibility reports.

## Local checks

Python 3.11+ and Git are sufficient; no pip dependencies are required. From the repository root:

```sh
python3 -B -m unittest discover -s evaluation -p test_eval_suite.py -v
python3 -B evaluation/eval_suite.py self-test
python3 -B -m unittest discover -s tests -v
```

Use disposable workspaces for evaluation. The grader executes fixture code in subprocesses, which are not a security sandbox. Read the [evaluation guide](evaluation/evaluation-guide.md) before executing submissions.

## Updating checksums

After reviewing your changes, stage the files intended for publication. The checksum helper reads Git's tracked paths and hashes their current working-tree bytes, excluding the manifest itself:

```sh
git add <files-you-intend-to-publish>
python3 scripts/update_checksums.py
git add SHA256SUMS.txt
python3 -B validation/validate_package.py
git diff --cached --check
```

If you modify the installable skill, the historical hash in `validation/preflight.json` will no longer match. Preserve the historical record and discuss an explicit versioned validation update in the pull request; do not silently rewrite original pilot evidence to imply it tested a different skill. A skill change needs its own reviewed hash/provenance update before the package validator can pass.

## Evidence and scope

- Keep the skill instruction-only and use the host's actual native controls.
- Preserve explicit user model choices, permissions, ownership boundaries, and existing work.
- Keep examples separate from observed behavior and measured results.
- Do not claim speed, cost, or success-rate improvements without a suitable benchmark and complete telemetry.
- Keep original trial artifacts reproducible and identify any newly collected evidence.
- Exclude credentials, private paths, conversation exports, and unrelated artifacts.

For documentation changes, check relative links and render any changed HTML at desktop and mobile widths. For behavioral changes, include focused verification. Avoid unrelated refactors or new dependencies without a concrete reason.

By submitting a contribution, you agree that it may be distributed under this repository's [MIT License](LICENSE).
