from flask import jsonify, request

from extensions import db, cache, limiter
from models import Inventory
from . import inventory_bp
from .schemas import InventorySchema

inventory_schema = InventorySchema()
inventory_list_schema = InventorySchema(many=True)


@inventory_bp.route("/", methods=["POST"])
def create_inventory_item():
    data = request.get_json()

    new_item = inventory_schema.load(data)
    db.session.add(new_item)
    db.session.commit()

    return inventory_schema.jsonify(new_item), 201


@inventory_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
@limiter.limit("10 per minute")
def get_inventory():
    items = db.session.execute(
        db.select(Inventory)
    ).scalars().all()

    return jsonify(inventory_list_schema.dump(items)), 200


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)

    if item is None:
        return jsonify({"message": "Inventory item not found"}), 404

    return inventory_schema.jsonify(item), 200


@inventory_bp.route("/<int:item_id>", methods=["PUT"])
def update_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)

    if item is None:
        return jsonify({"message": "Inventory item not found"}), 404

    data = request.get_json()
    updated_item = inventory_schema.load(data, instance=item, partial=True)

    db.session.commit()

    return inventory_schema.jsonify(updated_item), 200


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)

    if item is None:
        return jsonify({"message": "Inventory item not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Inventory item deleted"}), 200