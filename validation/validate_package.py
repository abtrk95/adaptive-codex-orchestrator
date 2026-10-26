#!/usr/bin/env python3
"""Read-only package integrity checks, not a runtime or full format validator."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tomllib
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / 'adaptive-codex-orchestrator'
EXPECTED = {'SKILL.md', 'agents/openai.yaml', 'references/architecture.md',
            'references/context-management.md', 'references/delegation-protocol.md',
            'references/examples.md', 'references/native-capabilities.md',
            'references/orchestration-policy.md', 'references/verification-and-recovery.md'}


def is_cache(path):
    return '__pycache__' in path.parts or path.suffix in ('.pyc', '.pyo')


def main():
    errors, checks = [], {}
    def check(name, fn):
        try:
            checks[name] = fn()
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
            checks[name] = 'failed'
            errors.append(f'{name}: {exc}')

    def files():
        actual = set()
        for p in SKILL.rglob('*'):
            if p.is_symlink():
                raise ValueError(f'symlink disallowed: {p.relative_to(SKILL)}')
            if p.is_file() and not is_cache(p.relative_to(SKILL)):
                actual.add(p.relative_to(SKILL).as_posix())
        if actual != EXPECTED:
            raise ValueError(f'missing={sorted(EXPECTED-actual)} unexpected={sorted(actual-EXPECTED)}')
        return 'passed'

    def frontmatter():
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        match = re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|\Z)', text, re.S)
        if not match:
            raise ValueError('missing basic frontmatter delimiters')
        body = match.group(1)
        if not re.search(r'^name:\s*adaptive-codex-orchestrator\s*$', body, re.M):
            raise ValueError('unexpected skill name')
        if not re.search(r'^description:\s*\S', body, re.M):
            raise ValueError('missing description')
        return 'passed (basic only)'

    def links():
        count = 0
        for path in SKILL.rglob('*.md'):
            text = path.read_text(encoding='utf-8')
            for target in re.findall(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)', text):
                target = target.strip('<>')
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                local = unquote(parsed.path)
                dest = (path.parent / local).resolve()
                if not dest.is_relative_to(SKILL.resolve()) or not dest.is_file():
                    raise ValueError(f'{path.relative_to(SKILL)}: invalid link {target}')
                count += 1
        return f'passed ({count} inline relative links)'

    def yaml_strings():
        content = (SKILL / 'agents/openai.yaml').read_text(encoding='utf-8')
        for term in ('interface:', 'display_name:', 'short_description:', 'default_prompt:', '$adaptive-codex-orchestrator'):
            if term not in content:
                raise ValueError(f'missing {term}')
        return 'passed (essential strings only; not YAML validation)'

    def toml():
        for name in ('agents.config.toml', 'terra-worker.toml'):
            with (ROOT / 'config-examples' / name).open('rb') as f:
                tomllib.load(f)
        return 'passed (syntax only)'

    def tree_hash():
        h = hashlib.sha256()
        paths = sorted(p.relative_to(SKILL).as_posix() for p in SKILL.rglob('*')
                       if p.is_file() and not is_cache(p.relative_to(SKILL)))
        for rel in paths:
            h.update(rel.encode('utf-8') + b'\0' + (SKILL / rel).read_bytes() + b'\0')
        actual = h.hexdigest()
        expected = json.loads((ROOT / 'validation/preflight.json').read_text())['skill_tree_sha256']
        if actual != expected:
            raise ValueError(f'preflight mismatch: actual={actual} expected={expected}')
        return actual

    def sums():
        manifest = ROOT / 'SHA256SUMS.txt'
        if not manifest.exists():
            return 'skipped (SHA256SUMS.txt absent)'
        seen = set()
        for number, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
            match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
            if not match:
                raise ValueError(f'line {number}: invalid format')
            expected, rel = match.groups()
            pp = PurePosixPath(rel)
            if pp.is_absolute() or any(x in ('..', '.') for x in rel.split('/')) or '\\' in rel or not pp.parts:
                raise ValueError(f'line {number}: unsafe path')
            if rel in seen:
                raise ValueError(f'line {number}: duplicate path {rel}')
            seen.add(rel)
            path = ROOT / rel
            if is_cache(pp) or path.is_dir():
                continue
            if not path.resolve().is_relative_to(ROOT.resolve()) or path.is_symlink() or not path.is_file():
                raise ValueError(f'line {number}: missing or unsafe file {rel}')
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(f'line {number}: checksum mismatch {rel}')
        if not seen:
            raise ValueError('empty checksum manifest')
        return f'passed ({len(seen)} entries; directories/cache skipped)'

    for name, fn in [('runtime_files', files), ('frontmatter', frontmatter), ('relative_links', links),
                     ('agent_yaml', yaml_strings), ('toml', toml), ('skill_tree_sha256', tree_hash),
                     ('package_checksums', sums)]:
        check(name, fn)
    print(json.dumps({'success': not errors, 'checks': checks, 'errors': errors,
                      'scope': 'Static checks only; no execution, network, activation, full YAML or specification validation.'}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
