from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Advice, Author
from app.utility import response_builder
from sqlalchemy import func

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
    data = request.get_json(silent=True)
    if data is None:
        return None, (
            jsonify(response_builder(
                "Request body must be JSON",
                state="Failed"
            )),
            400)

    if "advice" not in data or "author_id" not in data:
        return None, (
            jsonify(
                response_builder(
                    "'advice' and 'author_id' field is required",
                    state="Failed"
                )
            ), 400
        )

    if not isinstance(data["advice"], str):
        return None, (
            jsonify(
                response_builder(
                    "Advice must be a string",
                    state="Failed"
                )
            ), 400
        )

    if not data["advice"].strip():
        return None, (
            jsonify(
                response_builder(
                    "Advice cannot be empty",
                    state="Failed"
                )
            ), 400
        )

    return data, None


def validate_delete_payload():
    data = request.get_json(silent=True)
    if data is None:
        return None, (
            jsonify(
                response_builder(
                    "Request body must be JSON",
                    state="Failed"
                )
            ), 400
        )
        
    if "author_id" not in data:
        return None, (
            jsonify(
                response_builder(
                    " 'author_id' field is required",
                    state="Failed"
                )
            ), 400
        )

    return data, None


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

# ---------------------ROUTES------------------------
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
                "Search not found",
                state="Failed"
            )
        ), 404

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

    advice_dict = advice_dict_builder(
        advice.advice_id,
        advice.advice,
        advice.author
    )

    return jsonify(
        response_builder(
            "Advice retrieved successfuly",
            state="Success",
            data=advice_dict
        )
    ), 200


# Create new advice

@advice_bp.route("/advice", methods=["POST"])
def create_advice():
    data, error = validate_advice_payload()
    if error:
        return error

    # This restrictics unknown author from creating advices
    author, exist_error = validate_author_exists(data["author_id"])
    if exist_error:
        return exist_error


    advice = Advice(advice=data["advice"], author=author)
    db.session.add(advice)
    db.session.commit()

    advice_dict = advice_dict_builder(
        advice.advice_id,
        advice.advice,
        advice.author
    )

    return jsonify(
        response_builder(
            "Advice saved successfuly",
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

    # This restrictics unknown author from updating advices
    author, exist_error = validate_author_exists(data["author_id"])
    if exist_error:
        return exist_error


    advice.advice = data["advice"]
    db.session.commit()

    advice_dict = advice_dict_builder(
        advice.advice_id,
        advice.advice,
        advice.author
    )

    return jsonify(
        response_builder(
            "Advice update successfuly",
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

    data, error = validate_delete_payload()
    if error:
        return error

    # This restrictics unknown author from deleting advices
    author, exist_error = validate_author_exists(data["author_id"])
    if exist_error:
        return exist_error

    db.session.delete(advice)
    db.session.commit()

    return jsonify(
        response_builder(
            "Advice deleted successfuly",
            state="Success"
        )
    ), 200
