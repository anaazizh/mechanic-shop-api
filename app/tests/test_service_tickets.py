import unittest

from app import create_app
from app.extensions import db


class TestServiceTicketRoutes(unittest.TestCase):
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
        response = self.client.post(
            "/customers/",
            json={
                "name": "Ana Hemani",
                "email": "ana@example.com",
                "phone": "555-123-4567"
            }
        )

        self.assertEqual(response.status_code, 201)

        return response.json

    def create_mechanic(self):
        response = self.client.post(
            "/mechanics/",
            json={
                "name": "Jordan Smith",
                "email": "jordan@example.com",
                "phone": "555-123-4567"
            }
        )

        self.assertEqual(response.status_code, 201)

        return response.json

    def create_ticket(self, customer_id):
        response = self.client.post(
            "/service-tickets/",
            json={
                "VIN": "1HGCM82633A123456",
                "service_date": "2026-08-21",
                "service_desc": "Oil change and brake inspection",
                "customer_id": customer_id
            }
        )

        self.assertEqual(response.status_code, 201)

        return response.json

    def test_create_service_ticket(self):
        customer = self.create_customer()

        ticket = self.create_ticket(customer["id"])

        self.assertEqual(ticket["VIN"], "1HGCM82633A123456")
        self.assertEqual(ticket["customer_id"], customer["id"])

    def test_get_service_tickets(self):
        customer = self.create_customer()
        self.create_ticket(customer["id"])

        response = self.client.get("/service-tickets/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_assign_mechanic(self):
        customer = self.create_customer()
        ticket = self.create_ticket(customer["id"])
        mechanic = self.create_mechanic()

        response = self.client.put(
            f"/service-tickets/{ticket['id']}/assign-mechanic/{mechanic['id']}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Mechanic assigned successfully"
        )

    def test_assign_mechanic_ticket_not_found(self):
        mechanic = self.create_mechanic()

        response = self.client.put(
            f"/service-tickets/999/assign-mechanic/{mechanic['id']}"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["message"],
            "Service ticket not found"
        )

    def test_assign_mechanic_already_assigned(self):
        customer = self.create_customer()
        ticket = self.create_ticket(customer["id"])
        mechanic = self.create_mechanic()

        self.client.put(
            f"/service-tickets/{ticket['id']}/assign-mechanic/{mechanic['id']}"
        )

        response = self.client.put(
            f"/service-tickets/{ticket['id']}/assign-mechanic/{mechanic['id']}"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json["message"],
            "Mechanic already assigned"
        )

    def test_remove_mechanic(self):
        customer = self.create_customer()
        ticket = self.create_ticket(customer["id"])
        mechanic = self.create_mechanic()

        self.client.put(
            f"/service-tickets/{ticket['id']}/assign-mechanic/{mechanic['id']}"
        )

        response = self.client.put(
            f"/service-tickets/{ticket['id']}/remove-mechanic/{mechanic['id']}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Mechanic removed successfully"
        )

    def test_remove_mechanic_not_assigned(self):
        customer = self.create_customer()
        ticket = self.create_ticket(customer["id"])
        mechanic = self.create_mechanic()

        response = self.client.put(
            f"/service-tickets/{ticket['id']}/remove-mechanic/{mechanic['id']}"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json["message"],
            "Mechanic is not assigned to this ticket"
        )


if __name__ == "__main__":
    unittest.main()