# tui-design Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic probes hidden modes, keyboard traps, conflicting shortcuts, resize during modal/progress state, async update while selection/focus changes, terminal capability loss, Ctrl-C/quit during work, and crash restoration.

Block when accepted workflows cannot complete reliably with the supported key/focus model, essential state becomes invisible, resize/capability changes make the interface unusable without declared boundary, destructive shortcuts are unsafe, or terminal state can be left materially corrupted by normal exit/failure.

Do not enforce a universal `80×24` minimum; require an explicit support boundary and graceful behavior appropriate to the product.

## QA depth

Increase depth with pane/mode count, async updates, keybinding density, terminal capability variance, external-process integration, persistent state, and destructive actions.
