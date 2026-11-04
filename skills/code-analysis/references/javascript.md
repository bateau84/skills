# JavaScript investigation lens

Identify the host, module system, package exports, and test environment. Do not transfer browser timing or API assumptions to Node.js or Bun without checking them.

Trace values and identity, coercion, closures, object mutation, Promise settlement, callback registration, and exception/rejection ownership where they affect the result. For ordering claims, establish the relevant scheduling rules rather than assuming that source order is execution order. A timeout or completed Promise race does not by itself explain who stops the underlying work.

Use `javascript-runtime` for language behavior, `browser-runtime` for browser APIs, and `typescript-testing` for the shared JavaScript/TypeScript test mechanics where applicable. Prefer a small reproduction in the actual supported host when an ordering claim needs execution evidence.

Primary reference for Node.js scheduling: [Node.js event loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick). Consult the actual host's documentation for other environments.
