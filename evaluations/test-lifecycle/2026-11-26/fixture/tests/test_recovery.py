from pathlib import Path
import select
import subprocess
import sys
import tempfile
import unittest
from orders import OrderStore

ROOT = Path(__file__).resolve().parents[1]

class RecoveryTests(unittest.TestCase):
    def test_committed_order_survives_process_death(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "orders.db")
            child = subprocess.Popen(
                [sys.executable, "-B", str(ROOT / "orders.py"), "hold", path, "order-7"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
            )
            try:
                readable, _, _ = select.select([child.stdout], [], [], 10)
                self.assertTrue(readable, "child did not acknowledge committed order")
                self.assertEqual(child.stdout.readline().strip(), "created")
                child.kill()
                child.wait(timeout=10)
            finally:
                if child.poll() is None:
                    child.kill()
                    child.wait(timeout=10)
                child.stdin.close()
                child.stdout.close()
            restarted = subprocess.run(
                [sys.executable, "-B", str(ROOT / "orders.py"), "create", path, "order-7"],
                capture_output=True, text=True, check=True, timeout=10,
            )
            self.assertEqual(restarted.stdout.strip(), "duplicate")
            store = OrderStore(path)
            try:
                self.assertEqual(store.count(), 1)
            finally:
                store.close()
