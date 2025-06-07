import re
from flask import Blueprint, request, jsonify
from app.services.auth_service import signup_user, is_valid_email, get_password_strength
from app.models.user_model import users_collection 

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    pan_number = data.get("pan_number")
    contact_number = data.get("contact_number")
    dob = data.get("dob")  # format: "YYYY-MM-DD"
    date_of_registration = data.get("date_of_registration")  # format: "YYYY-MM-DD"
    broker_name = data.get("broker_name")

    required_fields = [email, password, pan_number, contact_number, dob, date_of_registration, broker_name]
    if not all(required_fields):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    if users_collection.find_one({"pan_number": pan_number}):
        return jsonify({"success": False, "message": "PAN number already registered."}), 400

    if users_collection.find_one({"contact_number": contact_number}):
        return jsonify({"success": False, "message": "Contact number already registered."}), 400

    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email format. Only alphanumeric, '@', and '.' allowed."}), 400

    password_strength = get_password_strength(password)
    if password_strength == "Weak":
        return jsonify({"success": False, "message": "Password is too weak. Please choose a stronger password."}), 400

    result = signup_user(
        email=email, 
        password=password,
        pan_number=pan_number,
        contact_number=contact_number,
        dob=dob,
        date_of_registration=date_of_registration,
        broker_name=broker_name
    )
    status_code = 200 if result["success"] else 400

    # Optionally, include password strength in the response
    response = result
    response["password_strength"] = password_strength

    return jsonify(response), status_code