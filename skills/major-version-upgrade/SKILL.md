---
name: major-version-upgrade
description: "Safely migrate software across a breaking version boundary. Use when upgrading a dependency, framework, runtime, database/client, SDK, compiler, build tool, protocol, or other software-stack component to a new major version or otherwise breaking release. Covers migration research, impact inventory, baseline evidence, code/config/data changes, transitive dependencies, rollout/rollback, and post-upgrade verification. Not for routine patch/minor bumps with no breaking contract, or live infrastructure operations with no software migration surface."
license: MIT
metadata:
  author: Bateau
  version: "1.0.0"
---

# Major Version Upgrade

Treat a major upgrade as a controlled migration, not as a version-number edit.

The objective is not merely to make the build green. The objective is to preserve accepted behavior, deliberately adopt intended breaking changes, expose unavoidable incompatibilities, and leave evidence that the new stack component is safe to use in the environments that matter.

Combine this skill with `software-engineering` and the relevant language, framework, database, security, testing, observability, or operations guidance.

## Safety invariants

- **Know the exact transition.** Record the current version, target version, why the upgrade is needed, supported environments, and any compatibility or rollback obligations.
- **Read every breaking boundary crossed.** When skipping majors, inspect authoritative release notes and migration guides for every intervening major. Do not reason only from the target version.
- **Baseline before changing.** Establish what currently builds, tests, starts, integrates, and fails before the upgrade. If the baseline is already red, record the known failures so they cannot be misattributed.
- **Treat defaults as API.** Configuration defaults, security posture, serialization, timeouts, retries, resource limits, generated output, wire formats, and persistence semantics can break behavior even when source code compiles.
- **Treat transitive changes as part of the upgrade.** Lockfile, dependency graph, runtime/toolchain requirements, plugins, generated code, and indirect packages are part of the migration surface.
- **Do not make green by weakening proof.** Do not delete useful tests, loosen assertions, suppress errors, disable checks, or replace real behavior with mocks merely to accommodate the new version.
- **Keep unrelated upgrades out.** Adjacent upgrades are allowed when the target requires them; make those forced changes explicit. Do not opportunistically modernize the rest of the stack.
- **Do not risk irreversible state casually.** Destructive or one-way data/schema/format migration requires a tested recovery, restore, or explicitly accepted no-rollback plan before non-disposable execution.
- **A code revert is not always a rollback.** New persisted data, emitted messages, protocol output, cache entries, or generated artifacts may make an old version unable to resume safely.

## 1. Define the upgrade contract

Before editing, establish the smallest useful contract:

- component or dependency being upgraded;
- current version and target version;
- reason for upgrading;
- environments/platforms that must still work;
- public or internal consumers that must remain compatible;
- whether deployment can be atomic or may run mixed old/new versions;
- persistence, protocol, or generated-format compatibility obligations;
- rollback/recovery expectation;
- accepted intentional behavior changes.

If any of these materially affect the implementation and are unknown, investigate them before committing to a migration design. Do not invent product or architecture policy inside the upgrade.

## 2. Build an authoritative migration map

Use the component's primary documentation where possible: release notes, migration guides, deprecation notices, compatibility matrices, changelogs, and supported-runtime statements.

For every major boundary crossed, extract only changes relevant to this repository and classify them:

- removed or changed APIs;
- changed defaults or configuration;
- runtime/compiler/platform requirements;
- plugin/extension compatibility;
- persistence/schema/serialization changes;
- network or protocol changes;
- security/authentication/TLS changes;
- concurrency, lifecycle, timeout, retry, or cancellation semantics;
- renamed environment variables, CLI flags, files, or generated artifacts;
- performance or resource behavior that can affect operating limits.

Do not treat a codemod, migration command, or automated fixer as authoritative proof. It is an editing aid whose output still needs review and verification.

If authoritative guidance is incomplete, mark the uncertain surface and use focused experiments or compatibility tests rather than guessing.

## 3. Inventory real coupling in the repository

Search beyond direct imports. A stack component may be coupled through:

- imports, API calls, types, annotations, callbacks, and interfaces;
- dependency manifests, lockfiles, vendored modules, images, and toolchain files;
- configuration, environment variables, CLI flags, feature toggles, and defaults;
- plugins, adapters, middleware, drivers, extensions, and code generators;
- database schemas, migrations, serialized data, messages, caches, and files;
- test fixtures, snapshots, mocks, golden files, and test-only helpers;
- build, lint, formatting, packaging, CI, deployment, and release automation;
- health checks, metrics, logs, tracing, alerts, dashboards, and runbooks;
- external consumers or sibling components that share the affected contract.

The upgrade surface is the actual coupling, not the package-manager diff.

## 4. Establish baseline evidence

Run the strongest practical pre-upgrade checks at the boundaries the change can affect.

Typical baseline evidence includes:

- dependency resolution;
- build/compile/type checking;
- existing unit and integration tests;
- startup and smoke tests;
- representative API/CLI flows;
- migrations against disposable representative data;
- generated-code or schema consistency;
- critical runtime behavior and resource usage when relevant.

Record pre-existing failures instead of repairing unrelated problems inside the upgrade unless they block meaningful verification.

For a risky change, preserve a representative before/after input or fixture so semantic drift can be compared directly.

## 5. Plan by breaking behavior, not by file

Group migration work around compatibility problems:

- API adaptation;
- configuration/default migration;
- persistence or schema migration;
- generated-code/toolchain migration;
- external protocol/consumer migration;
- rollout and mixed-version compatibility;
- removal of now-obsolete compatibility code.

When several majors are skipped, do not assume the safest final implementation must deploy each intermediate major. Use temporary intermediate steps when they make breakage easier to isolate, when the vendor requires sequential migration, or when persisted state must be transformed in stages. The final production path should remain as simple as the accepted compatibility obligations allow.

Prefer a small number of understandable migration slices over one unreviewable mechanical rewrite.

## 6. Perform the upgrade

Update the owning source of truth: manifest, version constraint, image/toolchain declaration, generator, schema source, or equivalent. Regenerate derived files through their owner rather than editing generated output by hand.

Then migrate repository coupling deliberately:

- replace removed APIs with supported equivalents;
- make changed defaults explicit when old behavior must remain;
- remove configuration that no longer has meaning;
- update validation and error handling for new failure modes;
- adapt tests to the accepted behavior, not merely to the new implementation;
- add compatibility code only for a named consumer, rollout need, or recovery obligation;
- remove temporary shims once the real migration no longer needs them.

Review automated migration output as ordinary code. Generated changes can be syntactically valid and semantically wrong.

## 7. Inspect dependency and artifact drift

Compare before and after:

- direct dependency versions;
- transitive dependency additions/removals/upgrades/downgrades;
- lockfile or checksum changes;
- runtime/compiler/toolchain floor;
- binary/container size when material;
- generated source, schemas, clients, or manifests;
- plugin/extension versions.

Investigate unexpected drift. Do not assume a resolver-selected graph is harmless merely because installation succeeds.

When security, licensing, provenance, or supply-chain policy applies, verify the new graph with the repository's normal controls rather than creating ad-hoc exceptions for the upgrade.

## 8. Verify the migrated behavior

Verification should climb from cheap/local to realistic/systemic, but the required proof comes from the risk surface, not a fixed checklist.

At minimum, verify the defining behavior that motivated or can be broken by the upgrade. Depending on the component, that may include:

- compile/type/static checks;
- unit and integration tests;
- startup/shutdown and health behavior;
- API, CLI, UI, or job flows through real component boundaries;
- persistence read/write and migration behavior;
- protocol compatibility with real or representative peers;
- cancellation, retries, timeouts, cleanup, and failure paths;
- mixed old/new versions during rolling deployment;
- restart and recovery after partial progress;
- performance, memory, CPU, latency, connection, or disk behavior when the major release changes relevant internals.

A successful build proves only that the compiled surface is compatible. A green unit suite proves only the behavior it exercises.

## 9. Prove rollout and recovery where relevant

For components with persistent state, shared protocols, or non-atomic deployment, explicitly test the transition:

1. old state/client with new code/server;
2. new state/client with old code/server when rollback requires it;
3. mixed old/new replicas or workers if the rollout can produce them;
4. interrupted migration or restart after partial progress;
5. rollback or restore after the new version has already produced state.

If rollback is impossible after a specific point, make that boundary explicit and ensure the deployment/recovery plan reflects it. Do not describe a source-control revert as safe rollback when state has crossed an incompatible boundary.

## 10. Finish the migration cleanly

Before completion:

- inspect the whole diff for unrelated modernization or accidental churn;
- remove obsolete shims, deprecated calls, dead config, stale comments, and temporary probes;
- ensure examples, developer setup, CI, deployment config, and runbooks reflect the new version where they are part of the changed contract;
- confirm no required follow-up is being mislabeled as optional;
- record the observed verification and any unverified environment or consumer.

A useful completion record states:

- from-version → target-version;
- important breaking changes encountered;
- repository adaptations made;
- transitive/runtime changes that came with the upgrade;
- compatibility/rollout/rollback conclusions;
- checks actually run and their outcomes;
- remaining limits or assumptions.

Do not claim the upgrade is safe outside the environments and behaviors actually verified.

## Composition

- Load `software-engineering` for baseline implementation discipline.
- Load task-relevant language/framework/database/testing skills for concrete mechanics.
- Load `risk-driven-planning` when an uncertain compatibility fact could invalidate the migration approach.
- Load security or observability skills when the major release changes those boundaries.
- Use the repository's normal Git and PR skills when commits or pull requests are in scope.

This skill supplies migration discipline. It does not authorize deployment, destructive data changes, production writes, or exceptions to project policy.
