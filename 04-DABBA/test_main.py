import unittest

from fastapi.testclient import TestClient

from main import app


class OrderApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("DABBA", response.json()["message"])

    def test_create_and_list_orders(self):
        payload = {
            "customer_name": "Alice",
            "customer_address": "123 Main St",
            "customer_phone": "555-0100",
        }

        create_response = self.client.post("/orders", json=payload)
        self.assertEqual(create_response.status_code, 201)
        order = create_response.json()
        self.assertEqual(order["customer_name"], "Alice")
        self.assertEqual(order["status"], "preparing")

        list_response = self.client.get("/orders")
        self.assertEqual(list_response.status_code, 200)
        self.assertGreaterEqual(len(list_response.json()), 1)

    def test_update_order_status(self):
        payload = {
            "customer_name": "Bob",
            "customer_address": "456 Elm St",
            "customer_phone": "555-0101",
        }

        created = self.client.post("/orders", json=payload).json()
        order_id = created["id"]

        update_response = self.client.patch(
            f"/orders/{order_id}/status",
            json={"status": "in transit"},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["status"], "in transit")


if __name__ == "__main__":
    unittest.main()
