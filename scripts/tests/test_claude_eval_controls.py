"""Provider-free checks for the opt-in Claude Agent skill profile."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from run_evals import parser, validate_live


class ClaudeEvalControlTests(unittest.TestCase):
    def args(self, *extra):
        return parser().parse_args(["--target", "agent-run-audit", "--model", "claude-agent/claude-sonnet-5-5", *extra])

    def test_native_profile_is_explicit_and_requires_known_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp)
            options = self.args("--claude-config-dir", str(profile))
            with self.assertRaisesRegex(ValueError, "dedicated native profile"):
                validate_live(options, ("case",))
            (profile / ".credentials.json").write_text('{"claudeAiOauth":{"accessToken":"FAKE"}}')
            with patch.dict("os.environ", {}, clear=True):
                validate_live(options, ("case",))

    def test_never_falls_back_to_api_or_default_host_login(self):
        with self.assertRaisesRegex(ValueError, "requires --claude-config-dir"):
            validate_live(self.args(), ("case",))
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp)
            (profile / ".credentials.json").write_text("{}")
            options = self.args("--claude-config-dir", str(profile))
            with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "FAKE-KEY"}, clear=True):
                with self.assertRaisesRegex(ValueError, "refuses API"):
                    validate_live(options, ("case",))


if __name__ == "__main__":
    unittest.main()
