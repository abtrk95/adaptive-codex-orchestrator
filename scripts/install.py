#!/usr/bin/env python3
"""Copy the skill to a discovery directory without replacing existing files."""
import argparse
from pathlib import Path
import shutil
import sys

SOURCE = Path(__file__).resolve().parent.parent / 'adaptive-codex-orchestrator'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path,
                        default=Path.home() / '.agents' / 'skills',
                        help='skills parent directory (default: ~/.agents/skills)')
    args = parser.parse_args()
    target = args.dest.expanduser().resolve() / SOURCE.name
    if target.exists() or target.is_symlink():
        parser.error(f'destination already exists; back it up before updating: {target}')
    try:
        shutil.copytree(SOURCE, target,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
    except OSError as exc:
        print(f'Installation failed: {exc}', file=sys.stderr)
        return 1
    print(f'Installed: {target}')
    print('Invoke $adaptive-codex-orchestrator in Codex. Restart Codex if needed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
