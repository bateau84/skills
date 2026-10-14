# golang-troubleshooting Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer verifies diagnosis is causal, not merely a plausible patch story:

- the symptom is reproduced or bounded with precise evidence/environment; “cannot reproduce” remains explicit;
- hypotheses predict discriminating observations and are falsified/updated rather than accumulated until one sounds right;
- logs/trace/pprof/race detector/delve/bisect/minimal reproducer are chosen to separate hypotheses with minimal perturbation;
- concurrency/timing instrumentation is recognized as capable of changing the bug (Heisenbug); evidence from `-race`, trace, stress, or controlled scheduling is interpreted accordingly;
- root cause is separated from trigger and downstream damage;
- semantic blast radius (implementation vs architecture/obligation/etc.) is established before the fix exceeds diagnostic authority;
- the correction reproduces the original failure before and eliminates it after, with a regression test/probe that would fail on recurrence.
