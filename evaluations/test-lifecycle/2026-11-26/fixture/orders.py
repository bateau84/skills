import sqlite3
import sys

def qualifies(amount, minimum):
    return amount > minimum

class OrderStore:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY)")
        self.db.commit()

    def _insert(self, order_id):
        self.db.execute("INSERT INTO orders (id) VALUES (?)", (order_id,))

    def create(self, order_id):
        try:
            self._insert(order_id)
            self.db.commit()
            return "created"
        except sqlite3.IntegrityError:
            self.db.rollback()
            return "duplicate"

    def count(self):
        return self.db.execute("SELECT count(*) FROM orders").fetchone()[0]

    def close(self):
        self.db.close()

if __name__ == "__main__":
    mode, path, order_id = sys.argv[1:]
    store = OrderStore(path)
    print(store.create(order_id), flush=True)
    if mode == "hold":
        sys.stdin.readline()
    store.close()
