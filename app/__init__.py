from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from app.extensions import db, ma


def create_app(config_class):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    from app.customer import customer_bp
    from app.mechanic import mechanic_bp
    from app.service_ticket import service_ticket_bp

    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")

    @app.route("/swagger.json")
    def swagger_spec():
        swag = swagger(app)
        swag["info"] = {
            "title": "Mechanic Shop API",
            "version": "1.0.0",
            "description": "Documentation for the Mechanic Shop API."
        }
        swag["host"] = "mechanic-shop-api-1nfm.onrender.com"
        swag["schemes"] = ["https"]
        swag["securityDefinitions"] = {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter your token as: Bearer <token>"
            }
        }
        return jsonify(swag)

    swaggerui_blueprint = get_swaggerui_blueprint(
        "/api/docs",
        "/swagger.json",
        config={
            "app_name": "Mechanic Shop API Documentation"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix="/api/docs")

    from app import models

    with app.app_context():
        db.create_all()

    return app