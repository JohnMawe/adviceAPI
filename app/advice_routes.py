from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Advice
from app.utility import response_builder

advice_bp = Blueprint("advice", __name__)

# Helper functions
def advice_dict_builder(advice_id, advice):
    return {
        "advice_id": advice_id,
        "advice": advice
    }

def validate_advice_payload():
    data = request.get_json(silent=True)
    if data is None:
        return None, (
            jsonify(response_builder(
                "Request body must be JSON",
                state="Failed"
            )),
            400)

    if "advice" not in data:
        return None, (
            jsonify(response_builder(
                "Advice field is required",
                state="Failed"
            )),
            400)
            
    if not isinstance(data["advice"], str):
        return None, (jsonify(response_builder(
            "Advice must be a string", 
            state="Failed")),
            400)

    if not data["advice"].strip():
        return None, (
            jsonify(response_builder(
                "Advice cannot be empty",
                state="Failed"
            )),
            400)

    return data, None

def validate_advice_exists(advice_id):
    advice = db.session.get(Advice, advice_id)
    if advice is None:
        return None, (jsonify(response_builder("ERROR!! Advice not found. Check advice id", state="Failed")), 404)
    return advice, None


# ---------------------ROUTES------------------------
@advice_bp.route("/")
def home():
    # later return will render home templete
    return jsonify({
        "message": "Advice Saver API"
    }), 200

# Get all advices
@advice_bp.route("/advice", methods=["GET"])
def all_advice():
    advice_list = Advice.query.all()

    if not advice_list:
        return jsonify(response_builder("No available advice", state="Success")), 200

    advices = [
        advice_dict_builder(advice.advice_id, advice.advice)
        
        for advice in advice_list
        ]
    return jsonify(response_builder("All advices", state="Success", data=advices)), 200

# Get advice by ID
@advice_bp.route("/advice/<int:advice_id>", methods=["GET"])
def advice(advice_id):
    advice, exist_error = validate_advice_exists(advice_id)
    if exist_error:
        return exist_error
    
    advice_dict = advice_dict_builder(advice.advice_id, advice.advice)
    return jsonify(response_builder("Advice retrieved successfuly", state="Success", data=advice_dict)), 200

# Create new advice
@advice_bp.route("/advice", methods=["POST"])
def create_advice():
    data, error = validate_advice_payload()
    if error:
        return error
    
    advice = Advice(advice=data["advice"])
    
    db.session.add(advice)
    db.session.commit()
    
    advice_dict = advice_dict_builder(advice.advice_id, advice.advice)
    return jsonify(response_builder("Advice saved successfuly", state="Success", data=advice_dict)), 201

# Updates existing advice
@advice_bp.route("/advice/<int:advice_id>", methods=["PUT"])
def update_advice(advice_id):
    advice, exist_error = validate_advice_exists(advice_id)
    if exist_error:
        return exist_error
    
    data, error= validate_advice_payload()
    if error:
        return error
    
    advice.advice = data["advice"]
    db.session.commit()
    
    advice_dict = advice_dict_builder(advice.advice_id, advice.advice)
    return jsonify(response_builder("Advice update successfuly", state="Success", data=advice_dict)), 200

# Delete existing advice
@advice_bp.route("/advice/<int:advice_id>", methods=["DELETE"])
def delete_advice(advice_id):
    advice, exist_error = validate_advice_exists(advice_id)
    if exist_error:
        return exist_error
    
    db.session.delete(advice)
    db.session.commit()
    return jsonify(response_builder("Advice deleted successfuly", state="Success"))
