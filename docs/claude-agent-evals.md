# Evaluate skills through Claude Agent in OpenCode (qualification pending)

The official runner image previously pinned OpenCode 2.2.2, before the native
`claude-agent` provider. Runner PR
[opencode-eval-runner#91](https://github.com/bateau84/opencode-eval-runner/pull/91)
adds a separate exact OpenCode 2.2.6 + Claude Code 2.1.318 OCI target.

This project keeps its original paired fixture normalization, native skill-load
assertions, baseline/candidate isolation, rubric grader, and result format. The
change is **only** an opt-in execution profile. It does not replace the runner,
weaken checks, or automatically use a subscription.

## Setup

Use the **exact runner PR head SHA** recorded in `scripts/eval_runner.py` in
a dedicated, clean checkout; this is an unmerged dependency pin. The checkout
must contain no modified, untracked, or ignored files. After the runner PR is
merged, update the pin to its accepted merge commit and repeat verification.

Build `--target claude-agent` explicitly from that runner revision:

```sh
podman build -f /path/to/opencode-eval-runner/Containerfile \
  --target claude-agent -t skills-claude-agent:local /path/to/opencode-eval-runner
export CLAUDE_IMAGE_ID="$(podman image inspect skills-claude-agent:local --format '{{.Id}}')"
```

Verify your own dedicated native login with Claude Code on the host:

```sh
mkdir -p "$HOME/.claude-eval-profile"
chmod 700 "$HOME/.claude-eval-profile"
CLAUDE_CONFIG_DIR="$HOME/.claude-eval-profile" claude auth login
CLAUDE_CONFIG_DIR="$HOME/.claude-eval-profile" claude auth status --json
```

Do not mount your normal `~/.claude` or pass a Claude OAuth token, API key, cloud
account or provider base URL. Disable paid extra usage at account level if
included-only usage is required. Native subscription status does **not** prove
that the account cannot incur charges. No paid requests are authorized by CI.

## First qualification

Run the provider-free probe first, selecting one existing case:

```sh
bun run eval:live -- \
  --probe --engine podman --image "$CLAUDE_IMAGE_ID" \
  --cases agent-run-audit:RUN-AUDIT-01 --claude-config-dir "$HOME/.claude-eval-profile"
```

This checks exact image/adapter bytes, OpenCode version and Claude binary version
without mounting credentials, networking or invoking a model. Then, **only
after explicit personal authorization**, run one real matched comparison:

```sh
bun run eval:live -- \
  --cases agent-run-audit:RUN-AUDIT-01 \
  --model 'claude-agent/<EXACT_AVAILABLE_MODEL_ID>' \
  --claude-config-dir "$HOME/.claude-eval-profile" \
  --engine podman --image "$CLAUDE_IMAGE_ID" \
  --iterations 1 --parallel 1 --transport-retries 0 --verbose
```

The runner currently requires `--parallel 1` for Claude Agent subscription trials because concurrent native credential refresh is unqualified. Cross-provider/API judges are rejected. The default judge uses the same model and native subscription. Every pair
nominally invokes two targets and two judges; one invocation can contain
multiple model turns. Use a small explicit selection, never `--all` initially.

## Acceptance gaps

No production/model calls were run in developing this integration. Treat
provider availability, native login, credentials refresh, exact native tool
observation, isolation, rate-limit behavior and billing as **unqualified**
until tested on the pinned image and real account. A dedicated profile is
bind-mounted read/write so the official Claude executable can refresh tokens;
OpenCode tools run in the same container namespace, so **credential
confidentiality from a malicious evaluated agent is not proven**. Do not use
with untrusted tool-bearing tasks before an independent isolation review.

This pilot is intended for controlled author-run trials with disposable profiles
and limited permissions, not unattended CI execution.
