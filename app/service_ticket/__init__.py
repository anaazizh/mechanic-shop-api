from flask import Blueprint

service_ticket_bp = Blueprint("service_ticket_bp", __name__)

from app.service_ticket import routes