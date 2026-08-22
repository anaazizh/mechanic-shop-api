from flask import request, jsonify
from app.extensions import db
from app.mechanic import mechanic_bp
from app.mechanic.schemas import MechanicSchema
from app.models import Mechanic


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    """
    Create a mechanic
    ---
    tags:
      - Mechanics
    summary: Create a new mechanic
    description: Creates and saves a mechanic using JSON request data.
    parameters:
      - in: body
        name: mechanic
        required: true
        description: Mechanic information to create.
        schema:
          id: MechanicPayload
          type: object
          required:
            - name
            - email
            - phone
          properties:
            name:
              type: string
              example: Jordan Smith
            email:
              type: string
              example: jordan@example.com
            phone:
              type: string
              example: 555-123-4567
    responses:
      201:
        description: Mechanic created successfully
        schema:
          id: MechanicResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: Jordan Smith
            email:
              type: string
              example: jordan@example.com
            phone:
              type: string
              example: 555-123-4567
      400:
        description: Invalid or missing mechanic data
    """
    mechanic_data = request.get_json()

    new_mechanic = mechanic_schema.load(mechanic_data)

    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201


@mechanic_bp.route("/", methods=["GET"])
def get_mechanics():
    """
    Get all mechanics
    ---
    tags:
      - Mechanics
    summary: Retrieve all mechanics
    description: Returns every mechanic currently stored in the database.
    responses:
      200:
        description: Mechanics retrieved successfully
        schema:
          type: array
          items:
            $ref: "#/definitions/MechanicResponse"
        examples:
          application/json:
            - id: 1
              name: Jordan Smith
              email: jordan@example.com
              phone: 555-123-4567
    """
    mechanics = db.session.query(Mechanic).all()

    return mechanics_schema.jsonify(mechanics), 200


@mechanic_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    """
    Update a mechanic
    ---
    tags:
      - Mechanics
    summary: Update a mechanic by ID
    description: Updates one or more fields for an existing mechanic.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The mechanic's database ID.
      - in: body
        name: mechanic
        required: true
        description: Mechanic fields to update.
        schema:
          $ref: "#/definitions/MechanicPayload"
    responses:
      200:
        description: Mechanic updated successfully
        schema:
          $ref: "#/definitions/MechanicResponse"
        examples:
          application/json:
            id: 1
            name: Jordan Smith
            email: jordan@example.com
            phone: 555-123-4567
      404:
        description: Mechanic not found
        examples:
          application/json:
            message: Mechanic not found
    """
    mechanic = db.session.get(Mechanic, id)

    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    mechanic_data = request.get_json()

    updated_mechanic = mechanic_schema.load(
        mechanic_data,
        instance=mechanic,
        partial=True
    )

    db.session.commit()

    return mechanic_schema.jsonify(updated_mechanic), 200


@mechanic_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    """
    Delete a mechanic
    ---
    tags:
      - Mechanics
    summary: Delete a mechanic by ID
    description: Deletes a mechanic if the provided mechanic ID exists.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The mechanic's database ID.
    responses:
      200:
        description: Mechanic deleted successfully
        examples:
          application/json:
            message: Mechanic deleted successfully
      404:
        description: Mechanic not found
        examples:
          application/json:
            message: Mechanic not found
    """
    mechanic = db.session.get(Mechanic, id)

    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic deleted successfully"}), 200