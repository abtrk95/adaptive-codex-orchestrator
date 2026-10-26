#!/usr/bin/env python3
"""Hash current working-tree bytes for Git-tracked publication files."""
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = 'SHA256SUMS.txt'


def main():
    result = subprocess.run(['git', 'ls-files', '--cached', '-z'], cwd=ROOT,
                            check=True, capture_output=True, text=True)
    paths = sorted(set(result.stdout.rstrip('\0').split('\0')) - {MANIFEST, ''})
    if not paths:
        raise ValueError('stage the publication files before generating checksums')
    lines = []
    for rel in paths:
        path = ROOT / rel
        if path.is_symlink() or not path.is_file() or '\n' in rel or '\r' in rel:
            raise ValueError(f'not a supported publication file: {rel}')
        lines.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}\n')
    (ROOT / MANIFEST).write_text(''.join(lines), encoding='utf-8')
    print(f'Wrote {len(lines)} checksums to {MANIFEST}')


if __name__ == '__main__':
    main()
