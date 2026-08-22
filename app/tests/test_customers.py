import unittest

from app import create_app
from app.extensions import db


class TestCustomerRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_customer(self):
        customer_data = {
            "name": "Ana Hemani",
            "email": "ana@example.com",
            "phone": "555-123-4567"
        }

        response = self.client.post("/customers/", json=customer_data)

        self.assertEqual(response.status_code, 201)

        return response.json

    def test_create_customer(self):
        customer = self.create_customer()

        self.assertEqual(customer["name"], "Ana Hemani")
        self.assertEqual(customer["email"], "ana@example.com")

    def test_get_customers(self):
        self.create_customer()

        response = self.client.get("/customers/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_customer(self):
        customer = self.create_customer()

        response = self.client.get(f"/customers/{customer['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["email"], "ana@example.com")

    def test_get_customer_not_found(self):
        response = self.client.get("/customers/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Customer not found")

    def test_update_customer(self):
        customer = self.create_customer()

        update_data = {
            "name": "Ana Aziz Hemani"
        }

        response = self.client.put(
            f"/customers/{customer['id']}",
            json=update_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Ana Aziz Hemani")

    def test_update_customer_not_found(self):
        response = self.client.put(
            "/customers/999",
            json={"name": "Missing Customer"}
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_customer(self):
        customer = self.create_customer()

        response = self.client.delete(f"/customers/{customer['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Customer deleted successfully"
        )

    def test_delete_customer_not_found(self):
        response = self.client.delete("/customers/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()