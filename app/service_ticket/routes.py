from flask import request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from app.service_ticket import service_ticket_bp
from app.service_ticket.schemas import ServiceTicketSchema


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)


@service_ticket_bp.route("/", methods=["POST"])
def create_service_ticket():
    """
    Create a service ticket
    ---
    tags:
      - Service Tickets
    summary: Create a new service ticket
    description: Creates and saves a service ticket using JSON request data.
    parameters:
      - in: body
        name: service_ticket
        required: true
        description: Service-ticket information to create.
        schema:
          id: ServiceTicketPayload
          type: object
          required:
            - VIN
            - service_date
            - service_desc
            - customer_id
          properties:
            VIN:
              type: string
              example: 1HGCM82633A123456
            service_date:
              type: string
              example: 2026-08-21
            service_desc:
              type: string
              example: Oil change and brake inspection
            customer_id:
              type: integer
              example: 1
    responses:
      201:
        description: Service ticket created successfully
        schema:
          id: ServiceTicketResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            VIN:
              type: string
              example: 1HGCM82633A123456
            service_date:
              type: string
              example: 2026-08-21
            service_desc:
              type: string
              example: Oil change and brake inspection
            customer_id:
              type: integer
              example: 1
      400:
        description: Invalid or missing service-ticket data
    """
    ticket_data = request.get_json()

    new_ticket = service_ticket_schema.load(ticket_data)

    db.session.add(new_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_ticket), 201


@service_ticket_bp.route("/", methods=["GET"])
def get_service_tickets():
    """
    Get all service tickets
    ---
    tags:
      - Service Tickets
    summary: Retrieve all service tickets
    description: Returns every service ticket currently stored in the database.
    responses:
      200:
        description: Service tickets retrieved successfully
        schema:
          type: array
          items:
            $ref: "#/definitions/ServiceTicketResponse"
        examples:
          application/json:
            - id: 1
              VIN: 1HGCM82633A123456
              service_date: 2026-08-21
              service_desc: Oil change and brake inspection
              customer_id: 1
    """
    tickets = db.session.query(ServiceTicket).all()

    return service_tickets_schema.jsonify(tickets), 200


@service_ticket_bp.route(
    "/<int:ticket_id>/assign-mechanic/<int:mechanic_id>",
    methods=["PUT"]
)
def assign_mechanic(ticket_id, mechanic_id):
    """
    Assign a mechanic to a service ticket
    ---
    tags:
      - Service Tickets
    summary: Assign one mechanic to one ticket
    description: Adds an existing mechanic to an existing service ticket.
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
        description: The service ticket's database ID.
      - name: mechanic_id
        in: path
        type: integer
        required: true
        description: The mechanic's database ID.
    responses:
      200:
        description: Mechanic assigned successfully
        examples:
          application/json:
            message: Mechanic assigned successfully
      400:
        description: Mechanic is already assigned to this ticket
        examples:
          application/json:
            message: Mechanic already assigned
      404:
        description: Service ticket or mechanic not found
        examples:
          application/json:
            message: Service ticket not found
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    if mechanic in ticket.mechanics:
        return jsonify({"message": "Mechanic already assigned"}), 400

    ticket.mechanics.append(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic assigned successfully"}), 200


@service_ticket_bp.route(
    "/<int:ticket_id>/remove-mechanic/<int:mechanic_id>",
    methods=["PUT"]
)
def remove_mechanic(ticket_id, mechanic_id):
    """
    Remove a mechanic from a service ticket
    ---
    tags:
      - Service Tickets
    summary: Remove one mechanic from one ticket
    description: Removes a mechanic who is currently assigned to an existing service ticket.
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
        description: The service ticket's database ID.
      - name: mechanic_id
        in: path
        type: integer
        required: true
        description: The mechanic's database ID.
    responses:
      200:
        description: Mechanic removed successfully
        examples:
          application/json:
            message: Mechanic removed successfully
      400:
        description: Mechanic is not assigned to this ticket
        examples:
          application/json:
            message: Mechanic is not assigned to this ticket
      404:
        description: Service ticket or mechanic not found
        examples:
          application/json:
            message: Service ticket not found
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    if mechanic not in ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this ticket"}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic removed successfully"}), 200