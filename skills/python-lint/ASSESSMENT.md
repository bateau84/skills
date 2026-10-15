# python-lint Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer verifies lint evidence represents the effective Python codebase:

- Ruff/Flake8/Pylint/etc. version, target Python version, selected/ignored rules, per-file ignores, excludes, namespace/package discovery, and generated/vendor policy are explicit;
- formatter/linter/import-sorter/type-checker responsibilities are not conflated; a green formatter is not static correctness proof;
- `noqa`/disable comments are narrow and justified; broad file/category suppressions do not erase new defects silently;
- CI invocation covers relevant source/tests and exits non-zero on findings; caches/wrappers do not stale/ignore output;
- config changes are reviewed for rules silently removed/renamed by tool upgrades;
- auto-fix changes are checked for behavior/API/import side effects rather than trusted mechanically.
