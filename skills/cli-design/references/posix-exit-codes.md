# POSIX Exit Code Specification and Extended Conventions

## Normative source

IEEE Std 1003.1-2017 (POSIX.1-2017), §2.8.2 Exit Status for Commands.
Available at: https://pubs.opengroup.org/onlinepubs/9699919799/
Verified live: 2026-09-02.

---

## POSIX-normative exit codes

| Code | Meaning | Authority |
|---|---|---|
| `0` | Success — the utility ran successfully | POSIX normative |
| `1` | Often general failure, but utility-specific (grep uses it for no match) | Convention, not universal POSIX assignment |
| `2` | Often usage/error status; consult the utility contract | Convention, not universal POSIX assignment |

POSIX does not universally assign 1 or 2 to those meanings. Utilities define statuses in the nonreserved range; shells specify 126/127 and signal-related values greater than 128.

---

## Shell-reserved conventional codes (non-normative)

POSIX specifies 126 and 127; 128+N is a common shell encoding of its greater-than-128 signal requirement. They should be avoided for application-defined meanings to prevent confusion:

| Code | Conventional meaning | Source |
|---|---|---|
| `126` | Command found but not executable | POSIX shell requirement |
| `127` | Command not found | POSIX shell requirement |
| `128` | Invalid argument to `exit` (some shells) | Shell convention |
| `128+N` | Process terminated by signal N | Shell convention (e.g., 130 = terminated by SIGINT/Ctrl-C) |
| `130` | Script terminated by Ctrl-C (SIGINT = signal 2, 128+2=130) | Shell convention |

Application exit codes should be in the range **3–125** for domain-specific meanings, avoiding the shell-reserved range.

---

## Real-world exit code designs

### `grep` (three-way)

| Code | Meaning |
|---|---|
| `0` | Match found |
| `1` | No match found (not an error — searching succeeded, found nothing) |
| `2` | Error (permission denied, file not found, invalid regex) |

This is a clean design that enables the idiom `if grep pattern file; then ...` where no-match is a meaningful non-error outcome distinct from actual errors.

### `curl` (multi-code)

`curl` defines ~100 distinct exit codes for different network failure modes, enabling scripts to distinguish connection timeout from DNS failure from SSL error. This is appropriate for a tool used heavily in automation where failure type determines recovery action.

### `rg` (ripgrep) — same as grep

| Code | Meaning |
|---|---|
| `0` | Match found |
| `1` | No match |
| `2` | Error |

Intentionally mirrors `grep` — users who know `grep`'s codes know `rg`'s codes.

---

## Design guidance for exit code tables

When designing a CLI's exit code taxonomy:

1. **Start from use cases, not codes.** Ask: what outcomes does a calling script need to distinguish? Each distinct branch in a script's logic requires a distinct exit code.

2. **Keep the table small.** More codes means more documentation burden and more opportunities for the implementation to get it wrong. One to five domain-specific codes is typical. `curl`'s 100 codes serve a tool with unusually high scripting requirements.

3. **Document the table as a contract.** Once exit codes are published, changing them breaks every script that depends on them. Treat the exit code table as a stable API.

4. **Consider 2 for usage errors when consistent with the existing CLI contract.** A user who passes an invalid flag should get exit 2, not exit 1. This enables scripts to distinguish "ran successfully but operation failed" from "was called incorrectly."

5. **Test the table explicitly.** Exit code behavior is easy to get wrong under partial success conditions. The implementation must match the table — verify it.
