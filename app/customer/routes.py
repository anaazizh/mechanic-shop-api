from flask import request, jsonify
from app.extensions import db
from app.customer import customer_bp
from app.customer.schemas import CustomerSchema
from app.models import Customer


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@customer_bp.route("/", methods=["POST"])
def create_customer():
    """
    Create a customer
    ---
    tags:
      - Customers
    summary: Create a new customer
    description: Creates and saves a customer using JSON request data.
    parameters:
      - in: body
        name: customer
        required: true
        description: Customer information to create.
        schema:
          id: CustomerPayload
          type: object
          required:
            - name
            - email
            - phone
          properties:
            name:
              type: string
              example: Ana Hemani
            email:
              type: string
              example: ana@example.com
            phone:
              type: string
              example: 555-123-4567
    responses:
      201:
        description: Customer created successfully
        schema:
          id: CustomerResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: Ana Hemani
            email:
              type: string
              example: ana@example.com

      400:
        description: Invalid or missing customer data
    """
    customer_data = request.get_json()

    new_customer = customer_schema.load(customer_data)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201


@customer_bp.route("/", methods=["GET"])
def get_customers():
    """
    Get all customers
    ---
    tags:
      - Customers
    summary: Retrieve all customers
    description: Returns every customer currently stored in the database.
    responses:
      200:
        description: Customers retrieved successfully
        schema:
          type: array
          items:
            $ref: "#/definitions/CustomerResponse"
        examples:
          application/json:
            - id: 1
              name: Ana Hemani
              email: ana@example.com
    """
    customers = db.session.query(Customer).all()

    return customers_schema.jsonify(customers), 200


@customer_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    """
    Get one customer
    ---
    tags:
      - Customers
    summary: Retrieve one customer by ID
    description: Returns one customer if the provided customer ID exists.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The customer's database ID.
    responses:
      200:
        description: Customer retrieved successfully
        schema:
          $ref: "#/definitions/CustomerResponse"
        examples:
          application/json:
            id: 1
            name: Ana Hemani
            email: ana@example.com
      404:
        description: Customer not found
        examples:
          application/json:
            message: Customer not found
    """
    customer = db.session.get(Customer, id)

    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    return customer_schema.jsonify(customer), 200


@customer_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    """
    Update a customer
    ---
    tags:
      - Customers
    summary: Update a customer by ID
    description: Updates one or more fields for an existing customer.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The customer's database ID.
      - in: body
        name: customer
        required: true
        description: Customer fields to update.
        schema:
          $ref: "#/definitions/CustomerPayload"
    responses:
      200:
        description: Customer updated successfully
        schema:
          $ref: "#/definitions/CustomerResponse"
        examples:
          application/json:
            id: 1
            name: Ana Hemani
            email: ana@example.com
      404:
        description: Customer not found
    """
    customer = db.session.get(Customer, id)

    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    customer_data = request.get_json()

    updated_customer = customer_schema.load(
        customer_data,
        instance=customer,
        partial=True
    )

    db.session.commit()

    return customer_schema.jsonify(updated_customer), 200


@customer_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    """
    Delete a customer
    ---
    tags:
      - Customers
    summary: Delete a customer by ID
    description: Deletes a customer if the provided customer ID exists.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The customer's database ID.
    responses:
      200:
        description: Customer deleted successfully
        examples:
          application/json:
            message: Customer deleted successfully
      404:
        description: Customer not found
        examples:
          application/json:
            message: Customer not found
    """
    customer = db.session.get(Customer, id)

    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully"}), 200