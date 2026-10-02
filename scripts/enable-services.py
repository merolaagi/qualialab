"""One-time, user-run activation of the prepared macOS login services."""
import json
import os
from pathlib import Path
import signal
import subprocess
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.runtime'
DOMAIN = f'gui/{os.getuid()}'
LABELS = ['com.merolaagi.qualialab.app', 'com.merolaagi.qualialab.tunnel']

def command(args, check=True):
    return subprocess.run(args, text=True, capture_output=True, check=check)

# Identify this setup's temporary processes by exact command and project directory.
# This runs in the user's Terminal, where macOS permits process inspection.
temporary = []
expected = {
    'node server.mjs',
    '/opt/homebrew/opt/node@22/bin/node server.mjs',
    'cloudflared --no-autoupdate tunnel --config .runtime/cloudflared.yml run',
}
for line in command(['ps', '-axo', 'pid=,command=']).stdout.splitlines():
    parts = line.strip().split(None, 1)
    if len(parts) != 2 or parts[1] not in expected:
        continue
    pid, actual = parts
    cwd = command(['/usr/sbin/lsof', '-a', '-p', pid, '-d', 'cwd', '-Fn'], False).stdout.splitlines()
    if 'n' + str(ROOT) in cwd:
        temporary.append({'pid': int(pid), 'command': actual})

# Load both services before replacing any temporary process. If macOS refuses,
# leave the existing app and tunnel running and surface the error.
for label in LABELS:
    if command(['launchctl', 'print', f'{DOMAIN}/{label}'], False).returncode:
        plist = Path.home() / 'Library' / 'LaunchAgents' / f'{label}.plist'
        result = command(['launchctl', 'bootstrap', DOMAIN, str(plist)], False)
        if result.returncode:
            raise SystemExit(f'Could not activate {label}: {result.stderr.strip()}\nRun this command directly in Terminal on the Mac mini.')

# Stop only the exact temporary processes recorded during this app's setup.
# PID, command and working directory must all still match; never kill a port owner blindly.
for item in temporary:
    pid = str(item['pid'])
    actual = command(['ps', '-p', pid, '-o', 'command='], False).stdout.strip()
    cwd = command(['/usr/sbin/lsof', '-a', '-p', pid, '-d', 'cwd', '-Fn'], False).stdout.splitlines()
    if actual == item['command'] and 'n' + str(ROOT) in cwd:
        os.kill(item['pid'], signal.SIGTERM)

for label in LABELS:
    command(['launchctl', 'kickstart', '-k', f'{DOMAIN}/{label}'])

port = json.loads((RUNTIME / 'config.json').read_text())['port']
for attempt in range(30):
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/healthz', timeout=2) as response:
            status = json.load(response)
        if status.get('app') == 'qualialab':
            print('Qualia Lab login services are active. Local release:', status['commit'])
            print('Open https://qualialab.fueldeskpro.com to verify the tunnel.')
            break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit('Services loaded but the app is not responding. Inspect .runtime/logs.')
