# python-common-practice Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic repeats calls/constructors, supplies `0`/`False`/`""`/`None`, consumes generators twice, imports in a clean process, raises during context-manager work, and mutates nested/shared defaults. Attack “Pythonic” shortcuts that silently collapse distinct states.

Block when these semantics cause plausible correctness, data leakage, resource, or public-contract failures. Non-idiomatic but explicit/safe code is not a blocker solely for style.

## QA depth

Increase depth with shared mutable state, resource/context managers, generator/lazy pipelines, import-time behavior, public dynamic interfaces, and long-lived process state.
