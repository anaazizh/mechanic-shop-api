from extensions import db


service_mechanic = db.Table(
    "service_mechanic",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanics.id"))
)

service_inventory = db.Table(
    "service_inventory",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_tickets.id")),
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"))
)


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_mechanic,
        back_populates="mechanics"
    )


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_inventory,
        back_populates="inventory_items"
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.String(17), nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    service_desc = db.Column(db.String(500), nullable=False)
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    customer = db.relationship("Customer", back_populates="service_tickets")

    mechanics = db.relationship(
        "Mechanic",
        secondary=service_mechanic,
        back_populates="service_tickets"
    )

    inventory_items = db.relationship(
        "Inventory",
        secondary=service_inventory,
        back_populates="service_tickets"
    )