from flask import jsonify
from sqlalchemy import func

from extensions import db
from models import Mechanic, service_mechanic
from . import mechanic_bp


@mechanic_bp.route("/most-tickets", methods=["GET"])
def mechanics_by_ticket_count():
    results = db.session.execute(
        db.select(
            Mechanic,
            func.count(service_mechanic.c.service_ticket_id).label("ticket_count")
        )
        .outerjoin(
            service_mechanic,
            Mechanic.id == service_mechanic.c.mechanic_id
        )
        .group_by(Mechanic.id)
        .order_by(func.count(service_mechanic.c.service_ticket_id).desc())
    ).all()

    return jsonify([
        {
            "id": mechanic.id,
            "name": mechanic.name,
            "email": mechanic.email,
            "phone": mechanic.phone,
            "salary": mechanic.salary,
            "ticket_count": ticket_count
        }
        for mechanic, ticket_count in results
    ]), 200