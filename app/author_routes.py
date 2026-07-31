from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Author, Advice
from app.utility import response_builder
from sqlalchemy import func

author_bp = Blueprint("author", __name__)


# Helper functions

def author_dict_builder(author_id, first_name, second_name, advices_count):
    return {
        "author_id": author_id,
        "first_name": first_name,
        "second_name": second_name,
        "advice_count": advices_count
    }

def advice_count(author, author_id):
    return db.session.query(Advice.advice_id).filter_by(author_id=author.author_id).count()

def pagination_builder(data_obj):
    return {
        "page": data_obj.page,
        "per_page": data_obj.per_page,
        "total": data_obj.total,
        "pages": data_obj.pages,
        "has_next": data_obj.has_next,
        "has_prev": data_obj.has_prev
    }

def validate_author_payload():
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

    if "first_name" not in data or "second_name" not in data:
        return None, (
            jsonify(
                response_builder(
                    "first_name and second_name field are required",
                    state="Failed"
                )
            ), 400
        )

    if not isinstance(data["first_name"], str):
        return None, (
            jsonify(
                response_builder(
                    "First name must be a string",
                    state="Failed"
                )
            ), 400
        )

    if not isinstance(data["second_name"], str):
        return None, (
            jsonify(
                response_builder(
                    "Second name must be a string",
                    state="Failed"
                )
            ), 400
        )

    if not data["first_name"].strip():
        return None, (
            jsonify(
                response_builder(
                    "First name cannot be empty",
                    state="Failed"
                )
            ), 400
        )

    if not data["second_name"].strip():
        return None, (
            jsonify(
                response_builder(
                    "Second name cannot be empty",
                    state="Failed"
                )
            ), 400
        )

    return data, None


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


#-------------------------ROUTES------------------------

# Search for author

@author_bp.route("/author/search", methods=["GET"])
def author_search():
    search = request.args.get("search")
    if not search:
        return jsonify(
            response_builder(
                "Search parameter is required!",
                state="Failed"
            )
        ), 400

    search_result = Author.query.filter(
        (Author.first_name.ilike(f"%{search}%")) | 
        (Author.second_name.ilike(f"%{search}%"))
    ).all()

    if not search_result:
        return jsonify(
            response_builder(
                "No matching author",
                state="Failed"
            )
        ), 200

    authors = [
        author_dict_builder(
            author.author_id,
            author.first_name,
            author.second_name,
            advice_count(author, author.author_id)
        )

        for author in search_result
    ]

    return jsonify(
        response_builder(
            "Search result successful",
            state="Success",
            data=authors
        )
    ), 200


# Get all authors

@author_bp.route("/author", methods=["GET"])
def get_authors():
    query = Author.query

    date = request.args.get("date")
    if date:
        query = query.filter(
            func.date(Author.date_joined) == date
        )
    
    page = request.args.get("page", 1, type=int)
    limit = min(
        request.args.get("limit", 5, type=int), 15
    )
    author_list = query.order_by(
        Author.date_joined.desc()
    ).paginate(page=page, per_page=limit)

    if not author_list.items:
        return jsonify(
            response_builder(
                "No available author",
                state="Success"
            )
        ), 200

    authors = [
        author_dict_builder(
            author.author_id,
            author.first_name, author.second_name,
            advice_count(author, author.author_id)
        )
        for author in author_list.items
    ]

    pagination = pagination_builder(author_list)

    response = response_builder(
        "All authors", 
        state="Success", 
        data=authors
    )

    response["pagination"] = pagination

    return jsonify(response), 200


# Get all author's advices

@author_bp.route("/author/<int:author_id>/advices")
def get_author_advices(author_id):
    author, exist_error = validate_author_exists(author_id)
    if exist_error:
        return exist_error

    query = Advice.query.filter_by(author_id=author.author_id)
    page = request.args.get("page", 1, type=int)
    limit = min(
        request.args.get("limit", 5, type=int), 15
    )
    author_advices = query.order_by(
        Advice.creation_date.desc()
    ).paginate(page=page, per_page=limit)

    if not author_advices.items:
        return jsonify(
            response_builder(
                "No available advices for this author",
                state="Success"
            )
        ), 200

    advice_list = [
        {
            "advice_id": advice.advice_id,
            "advice": advice.advice
        }
        for advice in author_advices.items
    ]
    
    pagination = pagination_builder(author_advices)

    author_dict = author_dict_builder(
        author.author_id,
        author.first_name,
        author.second_name,
        advice_count(author, author_id)
    )
    
    author_dict["advices"] = advice_list
    author_dict["pagination"] = pagination

    return jsonify(
        response_builder(
            "All author advices",
            state="Success",
            data = author_dict
        )
    )


# Get author by id

@author_bp.route("/author/<int:author_id>", methods=["GET"])
def author(author_id):
    author, exist_error = validate_author_exists(author_id)
    if exist_error:
        return exist_error

    author_dict = author_dict_builder(
        author.author_id,
        author.first_name,
        author.second_name,
        advice_count(author, author_id)
    )

    return jsonify(
        response_builder(
            "Author retrieved successfuly",
            state="Success",
            data=author_dict
        )
    ), 200


# Create new author

@author_bp.route("/author", methods=["POST"])
def create_author():
    data, error = validate_author_payload()
    if error:
        return error

    author = Author(
        first_name=data["first_name"],
        second_name=data["second_name"]
    )

    db.session.add(author)
    db.session.commit()

    author_dict = author_dict_builder(
        author.author_id,
        author.first_name,
        author.second_name,
        advice_count(author, author.author_id)
    )

    return jsonify(
        response_builder(
            "Author saved successfuly",
            state="Success",
            data=author_dict
        )
    ), 201


# Update existing author

@author_bp.route("/author/<int:author_id>", methods=["PUT"])
def update_author(author_id):
    author, exist_error = validate_author_exists(author_id)
    if exist_error:
        return exist_error

    data, error = validate_author_payload()
    if error:
        return error

    author.first_name = data["first_name"]
    author.second_name = data["second_name"]
    db.session.commit()

    author_dict = author_dict_builder(
        author.author_id,
        author.first_name,
        author.second_name,
        advice_count(author, author_id)
    )
    return jsonify(
        response_builder(
            "Author updated successfuly",
            state="Success",
            data=author_dict
        )
    ), 200


# Delete existing author
@author_bp.route("/author/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    author, exist_error = validate_author_exists(author_id)
    if exist_error:
        return exist_error

    # Denay deletion right if author has existing advice
    if advice_count(author, author_id):
        return jsonify(
            response_builder(
                "Cannot delete author because they still have advice.",
                state="Failed"
            )
        ), 400

    db.session.delete(author)
    db.session.commit()

    return jsonify(
        response_builder(
            "Author deleted successfuly",
            state="Success"
        )
    ), 200
