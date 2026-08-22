from flask import jsonify, request

from auth import encode_token, token_required
from extensions import db
from models import Customer, ServiceTicket
from . import customer_bp


@customer_bp.route("/", methods=["POST"])
def create_customer():
    data = request.get_json()

    customer = Customer(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        "id": customer.id,
        "name": customer.name,
        "email": customer.email
    }), 201


@customer_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    customer = db.session.execute(
        db.select(Customer).where(Customer.email == data["email"])
    ).scalar_one_or_none()

    if customer is None or customer.password != data["password"]:
        return jsonify({"message": "Invalid email or password"}), 401

    token = encode_token(customer.id)

    return jsonify({"token": token}), 200


@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    tickets = db.session.execute(
        db.select(ServiceTicket).where(
            ServiceTicket.customer_id == customer_id
        )
    ).scalars().all()

    ticket_data = []

    for ticket in tickets:
        ticket_data.append({
            "id": ticket.id,
            "VIN": ticket.VIN,
            "service_date": ticket.service_date.isoformat(),
            "service_desc": ticket.service_desc,
            "inventory_items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price
                }
                for item in ticket.inventory_items
            ]
        })

    return jsonify(ticket_data), 200

@customer_bp.route("/", methods=["GET"])
def get_customers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = db.paginate(
        db.select(Customer).order_by(Customer.id),
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "customers": [
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email
            }
            for customer in pagination.items
        ],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), 200