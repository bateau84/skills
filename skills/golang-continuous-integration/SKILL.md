---
name: golang-continuous-integration
description: "Set up or improve CI/CD pipelines with GitHub Actions for Go projects — testing, linting, SAST, code coverage, Dependabot, Renovate, GoReleaser, and release pipelines. Use when configuring GitHub Actions workflows, adding quality gates, automating dependency updates, or debugging CI failures. Not for Go build tooling or project layout (→ See `golang-project-layout`)."
license: MIT
metadata:
  author: Bateau
  version: "1.0.0"
  adapted-from: samber/cc-skills-golang@golang-continuous-integration
---

> Adapted from `samber/cc-skills-golang@golang-continuous-integration`. Pair with `golang-common-practice` for shared verification guidance.

**Persona:** You are a Go DevOps engineer. You treat CI as a quality gate — every pipeline decision is weighed against build speed, signal reliability, and security posture.

**Modes:**

- **Setup** — adding CI to a project for the first time: start with the Quick Reference table, then generate workflows in this order: test → lint → security → release. Prefer the latest stable major version for each GitHub Action.
- **Improve** — auditing or extending an existing pipeline: read current workflow files first, identify gaps against the Quick Reference table, then propose targeted additions without duplicating existing steps.

**Dependencies:**

- goreleaser: `go install github.com/goreleaser/goreleaser/v2@latest`
- gh: `brew install gh`

# Go Continuous Integration

Set up production-grade CI/CD pipelines for Go projects using GitHub Actions.

## Action Versions

The versions in the examples below are reference versions that may be outdated. GitHub Actions release frequently — the current major version for each action (`actions/checkout`, `actions/setup-go`, `golangci/golangci-lint-action`, `codecov/codecov-action`, `goreleaser/goreleaser-action`, etc.) may differ from what is shown here.

## Quick Reference

| Stage         | Tool                        | Purpose                       |
| ------------- | --------------------------- | ----------------------------- |
| **Test**      | `go test -race`             | Unit + race detection         |
| **Coverage**  | `codecov/codecov-action`    | Coverage reporting            |
| **Lint**      | `golangci-lint`             | Comprehensive linting         |
| **Vet**       | `go vet`                    | Built-in static analysis      |
| **SAST**      | `gosec`, `CodeQL`, `Bearer` | Security static analysis      |
| **Vuln scan** | `govulncheck`               | Known vulnerability detection |
| **Docker**    | `docker/build-push-action`  | Multi-platform image builds   |
| **Deps**      | Dependabot / Renovate       | Automated dependency updates  |
| **Release**   | GoReleaser                  | Automated binary releases     |
| **AI Review** | Claude Code / Copilot       | AI-powered PR review          |

---

## Testing

`.github/workflows/test.yml` — use `github-workflow` for workflow structure and the Go checks below for job steps.

Adapt the Go version matrix to match `go.mod`:

```
go 1.23   → matrix: ["1.23", "1.24", "1.25", "1.26", "stable"]
go 1.24   → matrix: ["1.24", "1.25", "1.26", "stable"]
go 1.25   → matrix: ["1.25", "1.26", "stable"]
go 1.26   → matrix: ["1.26", "stable"]
```

Use `fail-fast: false` so a failure on one Go version doesn't cancel the others.

Test flags:

- `-race`: CI MUST run tests with the `-race` flag (catches data races — undefined behavior in Go)
- `-shuffle=on`: Randomize test order to catch inter-test dependencies
- `-coverprofile`: Generate coverage data
- `git diff --exit-code`: Fails if `go mod tidy` changes anything

### Coverage Configuration

Use coverage thresholds when they support the project's quality policy. If Codecov is used, configure `codecov.yml` according to its [configuration documentation](https://docs.codecov.com/docs/codecov-yaml).

---

## Integration Tests

`.github/workflows/integration.yml` — define real service dependencies and isolation using `github-workflow` and `golang-testing`.

Use `-count=1` to disable test caching — cached results can hide flaky service interactions.

---

## Linting

When golangci-lint is the configured linter, run it in CI using the repository's version and configuration. Use `github-workflow` and `golang-lint` for job and linter guidance.

### golangci-lint Configuration

Create `.golangci.yml` at the root of the project. See the `golang-lint` skill for the recommended configuration.

---

## Security & SAST

`.github/workflows/security.yml` — use `github-workflow` and `golang-security` for applicable security checks.

CI MUST run `govulncheck`. It only reports vulnerabilities in code paths your project actually calls — unlike generic CVE scanners. CodeQL results appear in the repository's Security tab. Bearer is good at detecting sensitive data flow issues.

### CodeQL Configuration

If CodeQL is used, configure its query suite according to the project's threat surface and [CodeQL documentation](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning/customizing-your-advanced-setup-for-code-scanning).

Available query suites:

- **default**: Standard security queries
- **security-extended**: Extra security queries with slightly lower precision
- **security-and-quality**: Security queries plus maintainability and reliability checks

### Container Image Scanning

If the project produces Docker images and uses Trivy, include container scanning in the Docker workflow; verify the project's actual configuration rather than assuming a bundled workflow exists.

---

## Dependency Management

### Dependabot

`.github/dependabot.yml` — follow the [Dependabot configuration documentation](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file).

Minor/patch updates are grouped into a single PR. Major updates get individual PRs since they may have breaking changes.

#### Auto-Merge for Dependabot

If automated dependency merging is part of repository policy, require the configured checks and respect workflow trust boundaries; use `github-workflow` for implementation guidance.

> **Security warning:** This workflow requires `contents: write` and `pull-requests: write` — these are elevated permissions that allow merging PRs and modifying repository content. The `if: github.actor == 'dependabot[bot]'` guard restricts execution to Dependabot only. Do not remove this guard. Note that `github.actor` checks are not fully spoof-proof — **branch protection rules are the real safety net**. Ensure branch protection is configured (see [Repository Security Settings](#repository-security-settings)) with required status checks and required approvals so that auto-merge only succeeds after all checks pass, regardless of who triggered the workflow.

### Renovate (alternative)

Renovate is a more mature and configurable alternative to Dependabot. It supports automerge natively, grouping, scheduling, regex managers, and monorepo-aware updates. If Dependabot feels too limited, Renovate is the go-to choice.

If choosing Renovate, install the [Renovate GitHub App](https://github.com/apps/renovate) or the project's supported deployment and configure it using the [Renovate configuration reference](https://docs.renovatebot.com/configuration-options/).

Key advantages over Dependabot:

- **`gomodTidy`**: Automatically runs `go mod tidy` after updates
- **Native automerge**: No separate workflow needed
- **Better grouping**: More flexible rules for grouping PRs
- **Regex managers**: Can update versions in Dockerfiles, Makefiles, etc.
- **Monorepo support**: Handles Go workspaces and multi-module repos

---

## Release Automation

GoReleaser automates binary builds, checksums, and GitHub Releases. The configuration varies significantly depending on the project type.

### Release Workflow

`.github/workflows/release.yml` — use `github-workflow` for triggers, permissions, artifacts, and release jobs.

> **Security warning:** This workflow requires `contents: write` to create GitHub Releases. It is restricted to tag pushes (`tags: ["v*"]`) so it cannot be triggered by pull requests or branch pushes. Only users with push access to the repository can create tags.

### GoReleaser for CLI/Programs

Programs need cross-compiled binaries, archives, and optionally Docker images.

`.goreleaser.yml` — configure CLI builds and archives with the [GoReleaser documentation](https://goreleaser.com/customization/).

### GoReleaser for Libraries

Libraries don't produce binaries — they only need a GitHub Release with a changelog. Use a minimal config that skips the build.

For libraries, use the project's tag and release-note workflow; configure GoReleaser only for the release artifacts actually needed.

For libraries, you may not even need GoReleaser — a simple GitHub Release created via the UI or `gh release create` is often sufficient.

### GoReleaser for Monorepos / Multi-Binary

When a repository contains multiple commands (e.g., `cmd/api/`, `cmd/worker/`).

For monorepos, configure module-specific release boundaries and tag conventions according to the repository and installed release tooling.

### Docker Build & Push

For projects that produce Docker images. This workflow builds multi-platform images, generates SBOM and provenance attestations, pushes to both GitHub Container Registry (GHCR) and Docker Hub, and includes Trivy container scanning.

`.github/workflows/docker.yml` — use `github-workflow` for container build/publish permissions and job structure.

> **Security warning:** Permissions are scoped per job: the `container-scan` job only gets `contents: read` + `security-events: write`, while the `docker` job gets `packages: write` (to push to GHCR) and `attestations: write` + `id-token: write` (for provenance/SBOM signing). This ensures the scan job cannot push images even if compromised. The `push` flag is set to `false` on pull requests so untrusted code cannot publish images. The `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets must be configured in the repository secrets settings — never hardcode credentials.

Key details:

- **QEMU + Buildx**: Required for multi-platform builds (`linux/amd64,linux/arm64`). Remove platforms you don't need.
- **`push: false` on PRs**: Images are built but never pushed on pull requests — this validates the Dockerfile without publishing untrusted code.
- **Metadata action**: Automatically generates semver tags (`v1.2.3` → `1.2.3`, `1.2`, `1`), branch tags (`main`), and SHA tags.
- **Provenance + SBOM**: `provenance: mode=max` and `sbom: true` generate supply chain attestations. These require `attestations: write` and `id-token: write` permissions.
- **Dual registry**: Pushes to both GHCR (using `GITHUB_TOKEN`, no extra secret needed) and Docker Hub (requires `DOCKERHUB_USERNAME` + `DOCKERHUB_TOKEN` secrets). Remove the Docker Hub login and image line if not needed.
- **Trivy**: Scans the built image for CRITICAL and HIGH vulnerabilities and uploads results to the Security tab.
- Adapt the image names and registries to your project. For GHCR-only, remove the Docker Hub login step and the `docker.io/` line from `images:`.

---

## Repository Security Settings

Repository security settings (branch protection, workflow permissions, secrets, environments) form the security foundation for the CI pipeline — these are documented in [repo-security.md](./references/repo-security.md).

---

## AI-Driven Code Review

AI-assisted PR review can supplement traditional static analysis when the project chooses it. Provide task-relevant Go guidance by ordinary file reads or a supported loader; no skill plugin is assumed. Assess findings against the code and tests rather than treating AI review as guaranteed detection or a substitute for required independent review.

> **Cost note:** If the integration runs multiple review jobs per PR, limit jobs and triggers to the project's needs and observe actual cost.

### Claude Code

If the project uses an AI review integration, configure its documented action and permissions in the repository's workflow. No AI review service is required by this skill.

A project may group review areas as below. These are optional work categories, not required agents or parallel jobs:

| Job | Areas | Priority |
| --- | --- | --- |
| `quality` | Code style, Naming, Documentation, Design patterns | Suggestion-first |
| `correctness` | Error handling, Code safety, Concurrency | Blocking-first |
| `security` | Security, Dependencies | Blocking-first |
| `quality-depth` | Tests, Performance, Observability, Modernize | Mixed |

Additional skills that may be relevant depending on the project: `golang-cli`, `golang-context`, `golang-data-structures`, `golang-database`, `golang-dependency-injection`, or any library-specific skill.

The Claude Code GitHub App integration is configured via the `/install-github-app` command, which sets up the required API secrets.

### GitHub Copilot

If Copilot review is used, provide concise project-specific review instructions in its supported configuration. The following is an optional example; no copied template is required:

```bash
npx skills add https://github.com/samber/cc-skills-golang --agent github-copilot --skill '*' -y --copy
ln -s .agents .copilot
```

---

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Missing `-race` in CI tests | Always use `go test -race` |
| No `-shuffle=on` | Randomize test order to catch inter-test dependencies |
| Caching integration test results | Use `-count=1` to disable caching |
| `go mod tidy` not checked | Add `go mod tidy && git diff --exit-code` step |
| Missing `fail-fast: false` | One Go version failing shouldn't cancel other jobs |
| Not pinning action versions | GitHub Actions MUST use pinned major versions (e.g. `@vN`, not `@master`) |
| No `permissions` block | Follow least-privilege per job |
| Ignoring govulncheck findings | Fix or suppress with justification |
| Treating AI review as guaranteed coverage | Keep it optional, validate findings, and retain the project's required checks and review |

## Related Skills

See `golang-lint`, `golang-security`, `golang-testing`, `golang-dependency-management`, `golang-modernize` skills.
