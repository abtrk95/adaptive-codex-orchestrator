# Validation artifacts

This directory preserves evidence from the original development package. Treat its JSON files as dated records, not as a statement that every check has been rerun on your client.

- `preflight.json`: original skill hash and authoring-environment observations.
- `executed-checks.json`: original reported commands and results.
- `provenance.json`: methodology, deviations, and explicit nonclaims.
- `native-observations.json`: curated native trial observations; complete raw events were not retained.
- `pilot-records.jsonl`: descriptive trial records, with unavailable telemetry left null.
- `pilot/`: saved trial workspaces, manifests, patches, and grades.
- `quality-gate.json` and `review-log.json`: original qualitative assessments and review history.
- `validate_package.py`: read-only structure, basic metadata, TOML syntax, skill hash, and listed checksum checks.

From the repository root:

```sh
python3 -B validation/validate_package.py
```

Checksums detect accidental changes against the manifest; they do not provide an independent signature or security guarantee. The validator checks listed entries, not the absence of every unlisted file. For the release's added files and preserved source hashes, see [evidence notes](../docs/evidence.md).
