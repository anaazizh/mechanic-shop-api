from flask import jsonify

from extensions import db
from models import ServiceTicket, Mechanic, Inventory
from . import service_ticket_bp

from datetime import datetime
from flask import jsonify, request

@service_ticket_bp.route("/", methods=["POST"])
def create_service_ticket():
    data = request.get_json()

    service_date = datetime.strptime(
        data["service_date"],
        "%Y-%m-%d"
    ).date()

    ticket = ServiceTicket(
        VIN=data["VIN"],
        service_date=service_date,
        service_desc=data["service_desc"],
        customer_id=data["customer_id"]
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify({
        "id": ticket.id,
        "VIN": ticket.VIN,
        "service_date": ticket.service_date.isoformat(),
        "service_desc": ticket.service_desc,
        "customer_id": ticket.customer_id
    }), 201

@service_ticket_bp.route("/<int:ticket_id>/add-part/<int:inventory_id>", methods=["PUT"])
def add_part_to_ticket(ticket_id, inventory_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, inventory_id)

    if ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    if part is None:
        return jsonify({"message": "Inventory item not found"}), 404

    if part not in ticket.inventory_items:
        ticket.inventory_items.append(part)
        db.session.commit()

    return jsonify({
        "message": "Part added to service ticket",
        "ticket_id": ticket.id,
        "inventory_id": part.id
    }), 200
    
@service_ticket_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    data = request.get_json()
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)

        if mechanic is not None and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)

        if mechanic is not None and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()

    return jsonify({
        "message": "Ticket mechanics updated",
        "ticket_id": ticket.id,
        "mechanic_ids": [mechanic.id for mechanic in ticket.mechanics]
    }), 200