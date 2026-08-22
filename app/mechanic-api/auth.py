from datetime import datetime, timedelta
from functools import wraps

from flask import current_app, jsonify, request
from jose import JWTError, jwt


def encode_token(customer_id):
    payload = {
        "sub": str(customer_id),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


def token_required(route_function):
    @wraps(route_function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Bearer token is missing"}), 401

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            customer_id = int(payload["sub"])

        except (JWTError, KeyError, ValueError):
            return jsonify({"message": "Token is invalid or expired"}), 401

        return route_function(customer_id, *args, **kwargs)

    return decorated