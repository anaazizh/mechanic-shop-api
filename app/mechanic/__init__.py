from flask import Blueprint

mechanic_bp = Blueprint("mechanic_bp", __name__)

from app.mechanic import routes