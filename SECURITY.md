# Security policy

This is an experimental instruction-only skill with local installation and evaluation tools. Installing it does not sandbox native agents or change their permissions. Review the skill before using it on private or sensitive work.

The evaluator runs submitted Python code. Its copied workspaces and timeouts are not an OS security boundary. Use only trusted disposable fixtures, or an independently secured sandbox as described in the [evaluation guide](evaluation/evaluation-guide.md).

## Report a vulnerability

Use GitHub's [private vulnerability reporting](https://github.com/abtrk95/adaptive-codex-orchestrator/security/advisories/new). Include the affected version or commit, a minimal reproduction, impact, and any proposed fix. Do not publish credentials, personal data, or a working exploit against a third party in a public issue.

Reports are handled on a best-effort basis; there is no guaranteed response time. Review the latest release and changelog for fixes.
