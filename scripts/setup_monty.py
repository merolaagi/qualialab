"""Prepare a pinned source checkout using an existing compatible Python environment."""
import argparse
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import urllib.request

PIN = 'ed67dcbcacdded0418b59ff47667e59159116aa5'
root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--python', required=True, help='Existing Monty-compatible Python environment; not system Python')
args = parser.parse_args()
python = str(Path(args.python).resolve(strict=True))
runtime = root / '.runtime'
runtime.mkdir(exist_ok=True, mode=0o700)
source = runtime / 'monty-source'
marker = runtime / 'monty-source-commit.txt'
if source.exists() and (not marker.exists() or marker.read_text().strip() != PIN):
    raise SystemExit('Existing source lacks the expected pin marker. Inspect it before replacing it.')
if not source.exists():
    req = urllib.request.Request(f'https://api.github.com/repos/merolaagi/tbp.monty/tarball/{PIN}', headers={'User-Agent': 'Qualia-Lab-setup'})
    with urllib.request.urlopen(req, timeout=60) as response:
        archive = response.read(60_000_001)
    if len(archive) > 60_000_000:
        raise SystemExit('Archive exceeds expected size')
    source.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
        for member in tar.getmembers():
            parts = Path(member.name).parts[1:]
            if not parts:
                continue
            if '..' in parts or member.issym() or member.islnk() or not (member.isdir() or member.isfile()):
                raise SystemExit('Unsafe archive entry')
            target = source.joinpath(*parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(tar.extractfile(member).read())
    marker.write_text(PIN + '\n')
subprocess.run([python, '-m', 'pip', 'install', '--target', str(runtime / 'python-overlay'), '--no-deps',
                'omegaconf==2.3.0', 'hydra-core==1.3.2', 'antlr4-python3-runtime==4.9.3', 'eval_type_backport==0.4.0'], check=True)
(runtime / 'mpl').mkdir(exist_ok=True)
(runtime / 'monty.json').write_text(json.dumps({'python': python, 'sourceCommit': PIN}, indent=2))
env = dict(os.environ, MPLCONFIGDIR=str(runtime / 'mpl'))
subprocess.run([python, str(root / 'tests/monty_bridge_test.py')], env=env, check=True)
print('Pinned Monty graph-learning integration is ready.')
