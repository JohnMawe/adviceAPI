from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Advice
from app.utility import return_info

advice_bp = Blueprint("advice", __name__)

def advice_dict_builder(id, advice):
    return {
        "advice_id": id,
        "advice": advice
    }

@advice_bp.route("/")
def home():
    return {
        "message": "Advice Saver API"
    }

# Get all advices
@advice_bp.route("/advice", methods=["GET"])
def all_advice():
    advice_list = Advice.query.all()

    if not advice_list:
        return jsonify(return_info("No available advice", state="Success")), 200

    advices = [
        advice_dict_builder(advice.advcie_id, advice.advice)
        
        for advice in advice_list
        ]
    return jsonify(return_info("All advices", state="Success", data=advices)), 200

# Get advice by ID
@advice_bp.route("/advice/<int:advice_id>", methods=["GET"])
def advice(advice_id):
    # advice = Advice.query.get(advice_id)
    advice = db.session.get(Advice, advice_id)
    if advice is None:
        return jsonify(return_info("ERROR!! Advice not found. Check advice id", state="Failed")), 404
    
    advice_dict = advice_dict_builder(advice.advice_id, advice.advice)
    return jsonify(return_info("Advice retrieved successfuly", state="Success", data=advice_dict)), 200

# Create new advice
@advice_bp.route("/advice", methods=["POST"])
def create_advice():
    data = request.get_json()
    advice = Advice(advice=data["advice"])
    
    db.session.add(advice)
    db.session.commit()
    
    advice_dict = advice_dict_builder(advice.advcie_id, advice.advice)
    return jsonify(return_info("Advice saved successfuly", state="Success", data=advice_dict)), 201

# Updates existing advice
@advice_bp.route("/advice/<int:advice_id>", methods=["PUT"])
def update_advice(advice_id):
    advice = db.session.get(advice_id)
    if advice is None:
        return jsonify(return_info("ERROR!! Advice not found. Check advice id", state="Failed")), 404
    
    data = request.get_json()
    advice.advice = data["advice"]
    
    db.session.commit()
    
    advice_dict = advice_dict_builder(advice.advcie_id, advice.advice)
    return jsonify(return_info("Advice update successfuly", state="Success", data=advice_dict)), 200

# Delete existing advice
@advice_bp.route("/advice/<int:advice_id>", methods=["DELETE"])
def delete_advice(advice_id):
    advice = db.session.get(advive_id)
    if advice is None:
        return jsonify(return_info("ERROR!! Advice not found. Check advice id", state="Failed")), 404
    
    db.session.delete(advice)
    db.session.commit()
    return jsonify("Advice deleted successfuly", state="Success")
