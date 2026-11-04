# Python investigation lens

Read the Python version, package environment, entry points, and test configuration. Follow dynamic imports, decorators, dependency injection, and runtime validation when they determine the actual call path.

Distinguish a coroutine object from a scheduled task. Trace task ownership, cancellation propagation, exception handling, and cleanup; inspect synchronous calls inside async paths. Type annotations and a successful static check are not substitutes for inspecting runtime inputs and validators.

Use `python-how-to` to select relevant depth such as `python-async`, `python-error-handling`, `python-type-checking`, or `python-testing`. Reuse the configured checker and focused tests when execution is allowed; importing a module or collecting tests can itself run code.

Primary reference: [asyncio tasks and cancellation](https://docs.python.org/3/library/asyncio-task.html). Use documentation for the project's Python version before relying on a particular task-group or cancellation behavior.
