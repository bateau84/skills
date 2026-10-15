import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_cases import discover
from run_evals import parser, select, validate_live, call_budget

ROOT = Path(__file__).resolve().parents[2]


class CliTests(unittest.TestCase):
    def test_real_cli_provider_free_alias_modes_and_live_safeguards(self):
        script = ROOT / "scripts" / "run_evals.py"
        for argv, code in ((["--validate"], 0), (["--list", "--skills", "work-decomposition"], 0),
                           (["--cases", "product-acceptance:PA1"], 2),
                           (["--cases", "unknown", "--model", "test/model"], 2),
                           (["--target-kind", "skill", "--model", "test/model"], 2),
                           (["--probe", "--cases", ""], 2)):
            with self.subTest(argv=argv), tempfile.TemporaryDirectory() as temp:
                proc = subprocess.run([sys.executable, "-I", "-B", str(script), *argv],
                                      cwd=temp, capture_output=True, text=True, timeout=10)
                self.assertEqual(proc.returncode, code, proc.stderr)
                if argv == ["--validate"]:
                    self.assertIn('"fixture_cases": 235', proc.stdout)
                if "--list" in argv:
                    self.assertEqual(len(proc.stdout.splitlines()), 7)
                if code == 2:
                    self.assertNotIn("live-spend-plan", proc.stdout)

    def test_empty_unknown_selectors_and_no_model_fail_before_invocation(self):
        cases = discover(ROOT)
        for argv in ([], ["--model", "p/m"], ["--cases", ""], ["--cases", "unknown", "--model", "p/m"],
                     ["--skills", "unknown", "--model", "p/m"], ["--cases", "product-acceptance:PA1"]):
            with self.assertRaises(ValueError):
                options = parser().parse_args(argv)
                selected = select(cases, options)
                validate_live(options, selected)

    def test_selection_intersection_and_call_caps(self):
        options = parser().parse_args(["--skills", "product-acceptance", "--cases", "product-acceptance:PA1",
                                      "--model", "p/m", "--iterations", "2", "--transport-retries", "1"])
        selected = select(discover(ROOT), options)
        validate_live(options, selected)
        self.assertEqual(len(selected), 1)
        self.assertEqual(call_budget(len(selected), options), {
            "pairs": 2, "nominal_target_calls": 4, "nominal_judge_calls": 4,
            "maximum_target_calls": 8, "maximum_judge_calls": 8,
        })

    def test_native_target_only_cross_judge_explicit_model_reasoning_timeout_bounds(self):
        for argv in (["--judge-transport", "github-copilot-cli"], ["--container-timeout", "240"],
                     ["--parallel", "0"], ["--iterations", "0"], ["--transport-retries", "6"],
                     ["--model", "p/m#high", "--reasoning", "low"]):
            options = parser().parse_args(["--model", "p/m", "--cases", "product-acceptance:PA1", *argv])
            with self.assertRaises(ValueError):
                validate_live(options, select(discover(ROOT), options))


if __name__ == "__main__":
    unittest.main()
