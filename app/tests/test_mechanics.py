import unittest

from app import create_app
from app.extensions import db


class TestMechanicRoutes(unittest.TestCase):
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

    def create_mechanic(self):
        mechanic_data = {
            "name": "Jordan Smith",
            "email": "jordan@example.com",
            "phone": "555-123-4567"
        }

        response = self.client.post("/mechanics/", json=mechanic_data)

        self.assertEqual(response.status_code, 201)

        return response.json

    def test_create_mechanic(self):
        mechanic = self.create_mechanic()

        self.assertEqual(mechanic["name"], "Jordan Smith")
        self.assertEqual(mechanic["email"], "jordan@example.com")

    def test_get_mechanics(self):
        self.create_mechanic()

        response = self.client.get("/mechanics/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_mechanic(self):
        mechanic = self.create_mechanic()

        response = self.client.put(
            f"/mechanics/{mechanic['id']}",
            json={"phone": "555-999-0000"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["phone"], "555-999-0000")

    def test_update_mechanic_not_found(self):
        response = self.client.put(
            "/mechanics/999",
            json={"name": "Missing Mechanic"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Mechanic not found")

    def test_delete_mechanic(self):
        mechanic = self.create_mechanic()

        response = self.client.delete(f"/mechanics/{mechanic['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Mechanic deleted successfully"
        )

    def test_delete_mechanic_not_found(self):
        response = self.client.delete("/mechanics/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Mechanic not found")


if __name__ == "__main__":
    unittest.main()