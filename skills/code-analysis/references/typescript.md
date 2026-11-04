# TypeScript investigation lens

Read `tsconfig`, package scripts and lockfiles, module resolution, and the actual runtime: Node.js, Bun, a browser, or another host. Follow project references and generated types only where they affect the question.

At HTTP, storage, message, and JavaScript boundaries, trace the runtime value into its validation and use. Distinguish narrowing from assertions, `any`, and non-null assertions that may bypass proof. Follow Promise ownership, rejection, cancellation, and cleanup when relevant.

Use `typescript-type-safety` for type/runtime boundaries, `typescript-async` for async ownership, and `typescript-testing` for test evidence. Use `javascript-runtime` when the issue is JavaScript semantics rather than type modeling; browser API behavior belongs to `browser-runtime`.

Inspect the configured check before running it. A successful type check does not prove validation of external data or runtime correctness.

Primary reference: [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html). Check the pinned compiler and library definitions when semantics are version-sensitive.
