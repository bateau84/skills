import unittest
from unittest.mock import patch
from orders import OrderStore

class OrderTests(unittest.TestCase):
    def setUp(self):
        self.store = OrderStore(":memory:")
        self.addCleanup(self.store.close)

    def test_create_records_one_order(self):
        self.assertEqual(self.store.create("order-1"), "created")
        self.assertEqual(self.store.count(), 1)

    def test_duplicate_order_is_rejected(self):
        self.assertEqual(self.store.create("order-1"), "created")
        self.assertEqual(self.store.create("order-1"), "duplicate")
        self.assertEqual(self.store.count(), 1)

    def test_existing_order_id_is_rejected(self):
        self.assertEqual(self.store.create("order-1"), "created")
        self.assertEqual(self.store.create("order-1"), "duplicate")
        self.assertEqual(self.store.count(), 1)

    def test_create_uses_insert_once(self):
        with patch.object(self.store, "_insert", wraps=self.store._insert) as insert:
            self.assertEqual(self.store.create("order-1"), "created")
            insert.assert_called_once_with("order-1")
