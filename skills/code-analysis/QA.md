# Code Analysis Adversarial Validation

Challenge a coherent-looking analysis that has already survived ordinary review. Pick the attacks that could change its answer; do not require every attack for every explanation. Any execution or temporary edit still needs the host's permission and suitable isolation.

## Shared blind spots

- **Correlated evidence:** The explanation, graph, and tests may all come from the same stale/generated model. Compare a decisive edge with a separately observed current source or runtime path. Check that all evidence describes the same revision and configuration.
- **Invisible caller:** Try a plugin registration, reflection-based call, serialized message, feature flag, build target, or external consumer omitted by the index. Does the conclusion survive, or does its scope need narrowing?
- **Wrong execution order:** A cleanup function can exist without running after partial initialization, cancellation, or an exception. Challenge the sequence and owner, not merely the presence of cleanup code.
- **False corroboration:** A reproduction may call a helper directly, mock away the disputed dispatch, or inject the expected state. Inspect what path the evidence actually exercises. Where authorized, vary the input or guard that should change the result and check that the observation changes.
- **Missing counterexample:** Construct the strongest valid caller guarantee or input that would disprove a claimed defect. Conversely, test the weakest allowed precondition behind a "safe" conclusion. Separate impossible states from states the current boundary actually admits.
- **Environment mismatch:** Challenge a conclusion under another supported runtime, target, feature set, or configuration that the analysis claims to cover. Do not demand support for environments outside the accepted contract.

Report the attempted challenge, observed result, and resulting confidence limit. A paper walkthrough is not executed evidence; a failure to reproduce is not proof of absence. If the answer changes, correct the analysis rather than inventing new product requirements.
