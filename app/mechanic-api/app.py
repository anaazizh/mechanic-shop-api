from flask import Flask, jsonify

from config import DevelopmentConfig
from extensions import db, ma, limiter, cache
from models import Customer, Mechanic, ServiceTicket, Inventory

from blueprints.inventory import inventory_bp

from blueprints.service_tickets import service_ticket_bp

from blueprints.customers import customer_bp

from blueprints.mechanics import mechanic_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(
        service_ticket_bp,
        url_prefix="/service-tickets"
    )
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")

    @app.get("/")
    def home():
        return jsonify({"message": "Mechanic Shop API is running"})

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)