import hashlib
import hmac
import os
from datetime import datetime
from app.models.user_model import users_collection
from app.utils.age_utils import calculate_age
import re

HMAC_SECRET = os.environ.get("HMAC_SECRET", "default_secret_key")

def hmac_hash(value):
    return hmac.new(HMAC_SECRET.encode(), value.encode(), hashlib.sha256).hexdigest()

def is_email_unique(email):
    return users_collection.find_one({"email": email}) is None

def signup_user(**kwargs):
    email = kwargs.get("email")
    password = kwargs.get("password")
    pan_number = kwargs.get("pan_number")
    contact_number = kwargs.get("contact_number")
    dob = kwargs.get("dob")  # expected: "YYYY-MM-DD"
    date_of_registration = kwargs.get("date_of_registration")  # expected: "YYYY-MM-DD"
    broker_name = kwargs.get("broker_name")

    if not is_email_unique(email):
        return {"success": False, "message": "Email already exists."}

    try:
        dob_obj = datetime.strptime(dob, "%Y-%m-%d")
        registration_date_obj = datetime.strptime(date_of_registration, "%Y-%m-%d")
    except ValueError:
        return {"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}

    # Hash sensitive fields
    hashed_password = hmac_hash(password)
    hashed_pan = hmac_hash(pan_number)
    hashed_contact = hmac_hash(contact_number)

    age = calculate_age(dob)

    user_data = {
        "email": email,
        "password": hashed_password,
        "pan_number": hashed_pan,
        "contact_number": hashed_contact,
        "dob": dob_obj,
        "age":age,
        "date_of_registration": registration_date_obj,
        "broker_name": broker_name
    }

    result = users_collection.insert_one(user_data)
    return {"success": True, "user_id": str(result.inserted_id)}

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def get_password_strength(password):
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))

    score = sum([has_lower, has_upper, has_digit, has_special])

    if length < 6:
        return "Weak"
    elif length >= 6 and score == 2:
        return "Better"
    elif length >= 8 and score == 3:
        return "Strong"
    elif length >= 10 and score == 4:
        return "Very Strong"
    else:
        return "Weak"
