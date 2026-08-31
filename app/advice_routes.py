from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Advice, Author
from app.utility import response_builder
from sqlalchemy import func
from datetime import datetime
from app.schemas.advice_schemas import AdviceValidator, AdviceResponse, AdviceDelete
from pydantic import ValidationError

advice_bp = Blueprint("advice", __name__)

# Helper functions
def advice_dict_builder(advice_id, advice, author):
    return {
        "advice_id": advice_id,
        "advice": advice,
        "author": {
            "author_id": author.author_id,
            "full_name": f"{author.first_name} {author.second_name}"
        } if author else {}
    }

def validate_advice_payload():
    try:
        data = AdviceValidator.model_validate(request.get_json(silent=True))
        return data, None
    except ValidationError as error:
        return None, (
            jsonify(
                response_builder(error.errors(include_context=False), state="Failed")
            ), 400
        )

def validate_advice_exists(advice_id):
    advice = db.session.get(Advice, advice_id)
    if advice is None:
        return None, (
            jsonify(
                response_builder(
                    "ERROR!! Advice not found. Check advice id",
                    state="Failed"
                )
            ), 404
        )
        
    return advice, None

def validate_author_exists(author_id):
    author = db.session.get(Author, author_id)
    if author is None:
        return None, (
            jsonify(
                response_builder(
                    "ERROR!! Author not found. Check author id",
                    state="Failed"
                )
            ), 404
        )
    return author, None

# =================== ROUTES  ========================
# Search for advice

@advice_bp.route("/advice/search", methods=["GET"])
def advice_search():
    search = request.args.get("search")
    if not search:
        return jsonify(
            response_builder(
                "Search parameter is required!", 
                state="Failed"
            )
        ), 400

    page = request.args.get("page", 1, type=int)
    limit = min(
        request.args.get("limit", 5, type=int), 15
    )

    query = Advice.query.filter(
        Advice.advice.ilike(f"%{search}%")
    )

    advice_list = query.order_by(
        Advice.creation_date.desc()
    ).paginate(page=page, per_page=limit)


    if not advice_list.items:
        return jsonify(
            response_builder(
                "No matching advice",
                state="Failed"
            )
        ), 200

    advices = [
        advice_dict_builder(
            advice.advice_id,
            advice.advice,
            advice.author
        )

        for advice in advice_list.items
    ]
    
    return jsonify(
        response_builder(
            "Search result successful",
            state="Success",
            data=advices
        )
    ), 200


# Get all advices

@advice_bp.route("/advice", methods=["GET"])
def get_advices():
    query = Advice.query

    author_id = request.args.get("author_id", type=int)
    if author_id:
        query = query.filter(
            Advice.author_id == author_id
        )

    date = request.args.get("date")
    if date:
        query = query.filter(
            func.date(Advice.creation_date) == date
        )

    time = request.args.get("time")
    if time:
        query = query.filter(
            func.time(Advice.creation_date) == time
        )

    start_time = request.args.get("start")
    end_time = request.args.get("end")

    if end_time and start_time:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
        query = query.filter(
            Advice.creation_date.between(
                start_time, end_time
            )
        )

    page = request.args.get("page", 1, type=int)
    limit = min(
        request.args.get("limit", 5, type=int), 15
    )

    advice_list = query.order_by(
        Advice.creation_date.desc()
    ).paginate(page=page, per_page=limit)

    if not advice_list.items:
        return jsonify(
            response_builder(
                "No available advice",
                state="Success"
            )
        ), 200

    advices = [
        advice_dict_builder(
            advice.advice_id,
            advice.advice,
            advice.author
        )

        for advice in advice_list.items
    ]
    pagination = {
        "page": advice_list.page,
        "per_page": advice_list.per_page,
        "total": advice_list.total,
        "pages": advice_list.pages,
        "has_next": advice_list.has_next,
        "has_prev": advice_list.has_prev
    }
    response = response_builder(
        "All advices",
        state="Success",
        data=advices
    )
    response["pagination"] = pagination

    return jsonify(response), 200


# Get advice by ID

@advice_bp.route("/advice/<int:advice_id>", methods=["GET"])
def advice(advice_id):
    advice, exist_error = validate_advice_exists(advice_id)
    if exist_error:
        return exist_error

    try:
        valid_advice = AdviceResponse.model_validate(advice)
        advice_dict = advice_dict_builder(
            valid_advice.advice_id, valid_advice.advice, advice.author
        )
        return jsonify(
            response_builder(
                "Advice retrieved successfully",
                state="Success",
                data=advice_dict
            )
        ), 200
    except ValidationError as error:
        return jsonify(response_builder(error.errors(), state="Failed")), 400

# Create new advice

@advice_bp.route("/advice", methods=["POST"])
def create_advice():
    data, error = validate_advice_payload()
    if error:
        return error

    author, exist_error = validate_author_exists(data.author_id)
    if exist_error:
        return exist_error

    advice = Advice(advice=data.advice, author=author)
    db.session.add(advice)
    db.session.commit()

    advice_dict = advice_dict_builder(
        advice.advice_id,
        advice.advice,
        advice.author
    )

    return jsonify(
        response_builder(
            "Advice saved successfully",
            state="Success",
            data=advice_dict
        )
    ), 201

# Update existing advice

@advice_bp.route("/advice/<int:advice_id>", methods=["PUT"])
def update_advice(advice_id):
    advice, exist_error = validate_advice_exists(advice_id)
    if exist_error:
        return exist_error

    data, error = validate_advice_payload()
    if error:
        return error

    # These restrictions unknown author from deleting advices
    author, exist_error = validate_author_exists(data.author_id)
    if exist_error:
        return exist_error

    advice.advice = data.advice
    db.session.commit()
    advice_dict = advice_dict_builder(
        advice.advice_id,
        advice.advice,
        advice.author
    )
    return jsonify(
        response_builder(
            "Advice update successfully",
            state="Success",
            data=advice_dict
        )
    ), 200

# Delete existing advice

@advice_bp.route("/advice/<int:advice_id>", methods=["DELETE"])
def delete_advice(advice_id):
    advice, exist_error = validate_advice_exists(advice_id)
    if exist_error:
        return exist_error
    try:
        payload = AdviceDelete.model_validate(request.get_json(silent=True))

        # These restrictions unknown author from deleting advices
        author, exist_error = validate_author_exists(payload.author_id)
        if exist_error:
            return exist_error

        db.session.delete(advice)
        db.session.commit()

        return jsonify(
            response_builder(
                "Advice deleted successfully",
                state="Success"
            )
        ), 200

    except ValidationError as error:
        return jsonify(response_builder(error.errors(include_context=False), state="Failed")), 400
