"""Guard this integration against overwriting the incoming enrichment/pilot bytes."""
import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDED = {
    "skills/README.md",
    "skills/product-acceptance/evals/evals.json",
    "skills/work-decomposition/evals/evals.json",
}
EXPECTED = "abee72b9b30cf09ca7106fbd053239214949ad98c5738c842ca98b1989a3ba1f"


def incoming_digest():
    h = hashlib.sha256()
    for folder in (ROOT / "skills", ROOT / "evaluations" / "selective-enrichment"):
        for path in sorted(folder.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            if relative not in EXCLUDED:
                h.update(relative.encode() + b"\0" + path.read_bytes() + b"\0")
    return h.hexdigest()


class PreservationTests(unittest.TestCase):
    def test_incoming_enrichment_rename_history_and_original_fixtures_unchanged(self):
        self.assertEqual(incoming_digest(), EXPECTED)


if __name__ == "__main__":
    if "--snapshot" in sys.argv:
        print(incoming_digest())
    else:
        unittest.main()
