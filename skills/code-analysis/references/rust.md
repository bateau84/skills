# Rust investigation lens

Read `Cargo.toml`, `Cargo.lock`, any `rust-toolchain` file, edition, features, and target. Trace the enabled implementation, including macros, generated code, FFI, and conditional compilation where relevant.

Follow ownership, borrowing, `Drop`, error/panic paths, lock order, and task lifetime. At `unsafe` or FFI boundaries, identify the required invariants and who establishes them. Do not infer deadlock freedom or business correctness from successful compilation.

Use the project's configured checks and narrowly relevant tests or Clippy diagnostics when permitted. Cargo commands may execute build scripts or procedural macros and write artifacts; inspect the environment first. `cargo check` is not a runtime test and may miss diagnostics emitted only during code generation.

There is no assumed Rust specialist skill or mandatory tool installation. Use repository guidance and version-matched primary references:

- [Rust shared-state concurrency](https://doc.rust-lang.org/book/ch16-03-shared-state.html)
- [Cargo check](https://doc.rust-lang.org/cargo/commands/cargo-check.html)
