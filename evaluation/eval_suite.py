#!/usr/bin/env python3
"""Deterministic fixture preparation and local grading; not an agent runner."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fixtures():
    return {
        'tiny': {
            'task': 'Fix the inclusive range sum in range_sum.py. Keep the existing function signature. Run the public test.\n',
            'files': {'range_sum.py': 'def range_sum(start, end):\n    return sum(range(start, end))\n',
                      'test_public.py': 'from range_sum import range_sum\nassert range_sum(1, 3) == 6\n'},
            'reference': {'range_sum.py': 'def range_sum(start, end):\n    return sum(range(start, end + 1))\n'},
            'check': 'from range_sum import range_sum\nassert range_sum(1,3)==6\nassert range_sum(0,0)==0\nassert range_sum(-3,2)==-3\nassert range_sum(4,3)==0\n'},
        'parallel': {
            'task': 'Implement three independent modules decimal_adapter.py, hex_adapter.py, and binary_adapter.py. Each exposes parse(item): item is a dict with a value string; strip surrounding whitespace, accept an optional leading minus, then require one or more digits in the relevant base (10, 16, or 2); hexadecimal digits may be upper or lower case. Reject plus signs, prefixes, embedded whitespace, empty strings and invalid digits with ValueError. Return the integer. Keep dispatcher.py unchanged and run the public test.\n',
            'files': {'decimal_adapter.py': 'def parse(item):\n    return 0\n',
                      'hex_adapter.py': 'def parse(item):\n    return 0\n',
                      'binary_adapter.py': 'def parse(item):\n    return 0\n',
                      'dispatcher.py': 'import decimal_adapter, hex_adapter, binary_adapter\ndef parse(kind, item):\n    return {"decimal": decimal_adapter.parse, "hex": hex_adapter.parse, "binary": binary_adapter.parse}[kind](item)\n',
                      'test_public.py': 'from dispatcher import parse\nassert parse("decimal", {"value":"13"}) == 13\nassert parse("hex", {"value":"a"}) == 10\nassert parse("binary", {"value":"11"}) == 3\n'},
            'reference': {name + '_adapter.py': 'def parse(item):\n    value = item["value"].strip()\n    digits = value[1:] if value.startswith("-") else value\n    if not digits or any(c not in ' + repr(chars) + ' for c in digits):\n        raise ValueError("invalid value")\n    return int(value, ' + str(base) + ')\n' for name, chars, base in [('decimal','0123456789',10), ('hex','0123456789abcdefABCDEF',16), ('binary','01',2)]},
            'check': 'from dispatcher import parse\nfor kind, s, n in [("decimal","13",13),("decimal"," -42 ",-42),("hex"," ff ",255),("hex","-A",-10),("binary","10101",21),("binary","-10",-2)]:\n    assert parse(kind,{"value":s})==n\nfor kind, bad in [("decimal","x"),("hex","g"),("binary","2"),("hex","0xff"),("decimal","+2"),("binary",""),("decimal","1 2"),("hex","-")]:\n    try: parse(kind,{"value":bad})\n    except ValueError: pass\n    else: raise AssertionError("invalid input accepted")\n'},
        'dependency': {
            'task': 'Add an optional quantity to the order pipeline: schema.normalize must default it to 1; quantity must be a Python int other than bool and at least 1. Reject booleans, strings, floats, None, and values below 1 with ValueError. service.total must multiply unit price by quantity; api.quote must return {"total": total}. Preserve existing calls. Run public test.\n',
            'files': {'schema.py': 'def normalize(order):\n    return {"price": order["price"]}\n',
                      'service.py': 'from schema import normalize\ndef total(order):\n    return normalize(order)["price"]\n',
                      'api.py': 'from service import total\ndef quote(order):\n    return {"total": total(order)}\n',
                      'test_public.py': 'from api import quote\nassert quote({"price": 5, "quantity": 3}) == {"total": 15}\n'},
            'reference': {'schema.py': 'def normalize(order):\n    quantity = order.get("quantity", 1)\n    if type(quantity) is not int or quantity < 1:\n        raise ValueError("invalid quantity")\n    return {"price": order["price"], "quantity": quantity}\n',
                          'service.py': 'from schema import normalize\ndef total(order):\n    data = normalize(order)\n    return data["price"] * data["quantity"]\n'},
            'check': 'from api import quote\nfrom schema import normalize\nassert quote({"price":5,"quantity":3})=={"total":15}\nassert quote({"price":7})=={"total":7}\nassert normalize({"price":4,"quantity":2})["quantity"]==2\nfor q in [0,-1,1.5,True,False,"2",None]:\n    try: quote({"price":5,"quantity":q})\n    except ValueError: pass\n    else: raise AssertionError("invalid quantity accepted")\n'},
        'refactor': {
            'task': 'Refactor duplicated fee calculations into fee.py as fee(amount, rate), and make retail.py and wholesale.py call it. Preserve public functions and behavior: round amount * rate to two decimal places. Run the public test.\n',
            'files': {'retail.py': 'def charge(amount):\n    return round(amount * 0.1, 2)\n',
                      'wholesale.py': 'def charge(amount):\n    return round(amount * 0.05, 2)\n',
                      'fee.py': '# Implement shared fee calculation here.\n',
                      'test_public.py': 'import retail, wholesale\nassert retail.charge(100) == 10\nassert wholesale.charge(100) == 5\n'},
            'reference': {'fee.py': 'def fee(amount, rate):\n    return round(amount * rate, 2)\n',
                          'retail.py': 'from fee import fee\ndef charge(amount):\n    return fee(amount, 0.1)\n',
                          'wholesale.py': 'from fee import fee\ndef charge(amount):\n    return fee(amount, 0.05)\n'},
            'check': 'import fee, retail, wholesale\nfor n in [-100,-2.35,0,0.1,1,9.99,100,1234.567]:\n    assert retail.charge(n)==round(n*.1,2)\n    assert wholesale.charge(n)==round(n*.05,2)\n    assert fee.fee(n,.07)==round(n*.07,2)\n# Verify integration dynamically, without requiring a particular import style.\nimport sys, subprocess, textwrap\ncode = "import fee; fee.fee=lambda amount, rate: 876543; import retail, wholesale; assert retail.charge(2)==876543 and wholesale.charge(2)==876543"\nassert subprocess.run([sys.executable,"-B","-c",code],timeout=2).returncode==0\n'},
    }


def canonical(name):
    f = fixtures()[name]
    files = dict(f['files'])
    files['TASK.md'] = f['task'] + '\nWritable files: ' + ', '.join(sorted(f['reference'])) + '. Do not modify or delete other files, including test_public.py and SENTINEL.txt. Do not add files; interpreter __pycache__ directories are permitted.\n'
    files['SENTINEL.txt'] = 'Protected fixture data: do not modify.\n'
    return files


def prepare(name, out):
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('output must be a new or empty directory')
    out.mkdir(parents=True, exist_ok=True)
    work = out / 'workspace'
    work.mkdir()
    for path, content in canonical(name).items():
        (work / path).write_text(content, encoding='utf-8')
    meta = {'fixture': name, 'version': 1, 'allowed_changes': sorted(fixtures()[name]['reference']),
            'initial_sha256': {p: digest(s.encode()) for p, s in canonical(name).items()}}
    (out / 'manifest.json').write_text(json.dumps(meta, indent=2, sort_keys=True) + '\n')
    return meta


def expected_manifest(name):
    return {'fixture': name, 'version': 1, 'allowed_changes': sorted(fixtures()[name]['reference']),
            'initial_sha256': {p: digest(s.encode()) for p, s in canonical(name).items()}}


def cache_path(rel):
    return '__pycache__' in Path(rel).parts


def protected_changes(work, meta):
    bad = []
    for p in work.rglob('*'):
        rel = p.relative_to(work).as_posix()
        if p.is_symlink():
            bad.append(rel + ': symlink')
        elif cache_path(rel):
            continue
        elif p.is_file() and rel not in meta['allowed_changes']:
            if rel not in meta['initial_sha256'] or digest(p.read_bytes()) != meta['initial_sha256'][rel]:
                bad.append(rel + ': unexpected or modified')
        elif not p.is_dir() and not p.is_file():
            bad.append(rel + ': unsupported file')
    for rel in meta['initial_sha256']:
        if not (work / rel).is_file():
            bad.append(rel + ': missing')
    return sorted(bad)


def grade(case, timeout=5):
    case = Path(case)
    try:
        meta = json.loads((case / 'manifest.json').read_text())
        name = meta['fixture']
        if name not in fixtures() or meta != expected_manifest(name):
            raise ValueError('manifest mismatch')
        work = case / 'workspace'
        if not work.is_dir() or work.is_symlink():
            raise ValueError('workspace missing or symlinked')
        bad = protected_changes(work, meta)
        if bad:
            return {'fixture': name, 'status': 'fail', 'integrity': 'fail', 'functional': 'not_run', 'details': sorted(bad)}
        with tempfile.TemporaryDirectory(prefix='eval-grade-') as tmp:
            copy = Path(tmp) / 'submission'
            shutil.copytree(work, copy, symlinks=False, ignore=shutil.ignore_patterns('__pycache__'))
            checker = Path(tmp) / 'hidden_check.py'
            checker.write_text(fixtures()[name]['check'])
            receipt = Path(tmp) / 'checks-completed'
            env = os.environ.copy()
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            env['PYTHONPATH'] = str(copy)
            start = time.monotonic()
            try:
                result = subprocess.run([sys.executable, '-I', '-B', '-c',
                    'import runpy,sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); runpy.run_path(sys.argv[2],run_name="__main__"); Path(sys.argv[3]).write_text("completed")',
                    str(copy), str(checker), str(receipt)], cwd=copy, env=env, capture_output=True, text=True, timeout=timeout)
                bad_after = protected_changes(copy, meta)
                if bad_after:
                    return {'fixture': name, 'status': 'fail', 'integrity': 'fail', 'functional': 'fail', 'details': bad_after, 'stderr': result.stderr[-4000:]}
                completed = receipt.is_file() and receipt.read_text() == 'completed'
                passed = result.returncode == 0 and completed
                return {'fixture': name, 'status': 'pass' if passed else 'fail', 'integrity': 'pass',
                        'functional': 'pass' if passed else 'fail', 'returncode': result.returncode, 'checks_completed': completed,
                        'elapsed_seconds': time.monotonic()-start, 'stdout': result.stdout[-4000:], 'stderr': result.stderr[-4000:]}
            except subprocess.TimeoutExpired:
                bad_after = protected_changes(copy, meta)
                return {'fixture': name, 'status': 'fail', 'integrity': 'fail' if bad_after else 'pass', 'functional': 'timeout', 'details': bad_after, 'elapsed_seconds': time.monotonic()-start}
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return {'status': 'fail', 'integrity': 'fail', 'functional': 'not_run', 'details': [str(exc)]}


def apply_reference(case):
    """Only for grader self-test, never to prepare a trial."""
    case = Path(case)
    name = json.loads((case / 'manifest.json').read_text())['fixture']
    for path, content in fixtures()[name]['reference'].items():
        (case / 'workspace' / path).write_text(content)


def self_test():
    results = {}
    with tempfile.TemporaryDirectory() as tmp:
        for name in fixtures():
            case = Path(tmp) / name
            prepare(name, case)
            baseline = grade(case)
            apply_reference(case)
            reference = grade(case)
            results[name] = {'baseline': baseline['status'], 'reference': reference['status']}
            if baseline['status'] != 'fail' or reference['status'] != 'pass':
                raise AssertionError(results[name])
    return results


def summarize(path):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    required = ('trial_id', 'fixture', 'arm', 'model', 'runtime', 'fixture_hash', 'prompt_hash', 'skill_hash', 'outcome')
    seen = set()
    for row in rows:
        if any(k not in row or not isinstance(row[k], str) or not row[k].strip() for k in required):
            raise ValueError('each record requires nonempty trial_id, fixture, arm, model, runtime, fixture_hash, prompt_hash, skill_hash and outcome')
        if row['arm'] not in ('A', 'B', 'C') or row['outcome'] not in ('pass', 'fail', 'unknown'):
            raise ValueError('invalid arm or outcome')
        if row['trial_id'] in seen:
            raise ValueError('duplicate trial_id')
        seen.add(row['trial_id'])
        for k in ('wall_seconds', 'tokens', 'cost'):
            v = row.get(k)
            if v is not None and (isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0):
                raise ValueError('metric must be nonnegative or null: ' + k)
    report = {}
    for arm in ('A', 'B', 'C'):
        subset = [r for r in rows if r['arm'] == arm]
        metrics = {}
        for k in ('wall_seconds', 'tokens', 'cost'):
            vals = [r[k] for r in subset if r.get(k) is not None]
            metrics[k] = {'observed': len(vals), 'total': len(subset), 'sum': sum(vals) if vals else None}
        report[arm] = {'trials': len(subset), 'pass': sum(r['outcome']=='pass' for r in subset),
                       'fail': sum(r['outcome']=='fail' for r in subset), 'unknown': sum(r['outcome']=='unknown' for r in subset), 'metrics': metrics}
    return {'records': len(rows), 'arms': report, 'note': 'Descriptive only; no automatic matching, causal inference, or imputation.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('prepare'); a.add_argument('--fixture', choices=fixtures(), required=True); a.add_argument('--out', required=True)
    a = sub.add_parser('grade'); a.add_argument('--case', required=True); a.add_argument('--timeout', type=float, default=5)
    a = sub.add_parser('summarize'); a.add_argument('--records', required=True)
    sub.add_parser('self-test')
    args = p.parse_args()
    try:
        if args.command == 'prepare': result = prepare(args.fixture, args.out)
        elif args.command == 'grade':
            if args.timeout <= 0: raise ValueError('timeout must be positive')
            result = grade(args.case, args.timeout)
        elif args.command == 'summarize': result = summarize(args.records)
        else: result = self_test()
        print(json.dumps(result, indent=2, sort_keys=True))
        if args.command == 'grade' and result['status'] != 'pass': return 1
        return 0
    except (OSError, ValueError, AssertionError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
