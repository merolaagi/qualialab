# Qualia Lab continuity

This is the canonical Qualia Lab project. Continue iterations here, in the same GitHub repository and at the same domain. Do not create another repo, hosting project, or tunnel for normal updates.

- Repository: https://github.com/merolaagi/qualialab (public)
- Domain: https://qualialab.fueldeskpro.com
- Permanent Mac mini checkout: /Users/manishbhattarai/Sites/qualialab
- Deployment instructions: DEPLOYMENT.md

Keep the distinction between simulated representations and phenomenal experience visible. Preserve the recovered conversation and provenance. Update research/implementation documentation when the experimental model changes; rebuild the PDF with scripts/build_research.py if its content changes, then render and review it using the PDF skill.

Use `npm run publish -- "Describe the iteration"` to test, rebuild downloads, commit, push, and activate a release. The user's standing request authorizes updates to this same repo and site with each requested iteration. Do not schedule unsolicited iterations or publish unrelated files. Verify the live /healthz commit and key workflows. Keep .runtime, Cloudflare credentials, local logs, and secrets out of Git.

Before starting a listener, use the persisted .runtime/config.json port. Bind only to 127.0.0.1 and fail on a conflict. Never kill another project's listener. The port was allocated by the OS at initial setup. Do not change it without updating the dedicated tunnel ingress too.

Public static files are served only from the active release through an explicit allowlist. The repository, runtime directory, and credentials must never be exposed by the app server.
