# Mac mini deployment

Qualia Lab runs on this Mac mini, reached through a dedicated Cloudflare Tunnel at https://qualialab.fueldeskpro.com. Its public source lives at https://github.com/merolaagi/qualialab.

## Normal iteration

Edit this project, update the research notes for meaningful changes, and run:

```sh
npm run publish -- "Describe this iteration"
```

This runs computational checks, refreshes the downloadable app and documents, commits tracked project content, pushes main, and switches the local static release atomically. If checks or the push fail, the active release remains unchanged. It preserves a previous-release pointer for rollback.

Verify the live `/healthz` commit equals `git rev-parse HEAD`, then exercise the changed workflow in a browser. Ordinary app/document updates do not need a server or tunnel restart. If server.mjs itself changes, restart only the Qualia Lab app service after checks.

Changes pushed from another computer are not deployed silently. In this checkout run `npm run sync` to require a clean checkout, fast-forward from origin/main, test, and activate it. An iteration is complete only after the same repository and domain are updated and verified.

## One-time service activation

If setup was performed from a sandboxed agent session, run this directly in Terminal on the Mac mini:

```sh
python3 /Users/manishbhattarai/Sites/qualialab/scripts/enable-services.py
```

It loads the prepared login services, then replaces only setup processes whose PID, exact command, and working directory match this project. It leaves temporary processes running if service activation fails. No sudo is needed. The app can be live temporarily before this step, but should not be treated as durably supervised until the step succeeds.

## Service lifecycle

The app service is `com.merolaagi.qualialab.app`; the dedicated tunnel is `com.merolaagi.qualialab.tunnel`. Their launch-agent files are in the signed-in user's Library/LaunchAgents. Both are configured to run at login and restart on failure. The Mac must remain awake and online. These are user login services: after a reboot they start when this user logs in, not before login.

The app listens only on 127.0.0.1. The OS-selected port is persisted in `.runtime/config.json`, along with the public hostname. The dedicated tunnel configuration and credentials live in `.runtime`, which is excluded from Git. They are not served by the web app. Existing tunnels for other applications are left unchanged.

To inspect services, use `launchctl print gui/$(id -u)/com.merolaagi.qualialab.app` and the equivalent `.tunnel` label. To restart only this app, use `launchctl kickstart -k gui/$(id -u)/com.merolaagi.qualialab.app`. Logs are in `.runtime/logs`.

## Rollback

```sh
npm run rollback
```

This swaps the active release and previous release. It does not rewrite Git history or change source files. Verify `/healthz` afterward. To correct source permanently, make a new correcting commit and publish normally. With only the initial release there is no previous release to restore.

## Research documents

`scripts/build_research.py` rebuilds the comprehensive README and PDF from the authored narrative plus `research/conversation.json`. It requires Python with ReportLab. Apply the PDF skill's render-and-review workflow whenever regenerating it. `npm run build` copies the final documents into dist and rebuilds the self-contained downloadable HTML.

The recovered transcript and research notes are included in this public project, as part of the requested public Qualia Lab app. Session exports and live experiment state remain in the visitor's browser; there is no server endpoint to collect them.

## Recovery

Clone the repository, install Node.js and cloudflared, recreate the local runtime configuration and tunnel credentials through your Cloudflare account, choose a free port, and install launch agents for the new paths. Credentials are deliberately not backed up in the public repository. Preserve the existing DNS name and tunnel when restoring this same machine.

GitHub Actions runs the computational checks on pushes and pull requests. It does not require a runner on the Mac, store Cloudflare credentials, or grant GitHub remote access to the Mac.
