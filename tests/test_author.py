import pytest

# Global function
base_url = "/advice"
author_url = "/author"
first_name = "john"
second_name = "James"
sample_id = 1
author_payload = {
    "first_name": first_name,
    "second_name": second_name
}
bad_first_payload = {
    "first": first_name,
    "second_name": second_name
}

bad_second_payload = {
    "first_name": first_name,
    "second": second_name
}

empty_first_name = {
    "first_name": " ",
    "second_name": second_name
}

empty_second_name = {
    "first_name": first_name,
    "second_name": " "
}

first_name_int = {
    "first_name": 123,
    "second_name": second_name
}

second_name_int = {
    "first_name": first_name,
    "second_name": 123
}

new_payload = {
    "first_name": "James",
    "second_name": "John"
}

json_payload = {
    "advice": "Test before push to production",
    "author_id": sample_id
}

invalid_payload_key = [
    pytest.param(
        {},
        id="empty_json"
    ),
    pytest.param(
        bad_first_payload,
        id="bad_first_payload"
    ),
    pytest.param(
        bad_second_payload,
        id="bad_second_payload"
    )
]


invalid_payload_value = [
    pytest.param(
        empty_first_name,
        "First name cannot be empty",
        id="empty_first_name"
    ),
    pytest.param(
        empty_second_name,
        "Second name cannot be empty",
        id="empty_second_name"
    ),
    pytest.param(
        first_name_int,
        "First name must be a string",
        id="first_name_int"
    )
]

# Helper function

def create_new_author(client, json=author_payload, code=201):
    response = client.post(author_url, json=json)
    assert response.status_code == code
    return response

def create_new_advice(client, json=json_payload, code=201):
    response = client.post(base_url, json=json)
    assert response.status_code == code
    return response


#---------------------TESTING----------------------

def test_search_no_result(client):
    response = client.get(
        f"{author_url}/search?search=john"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "No matching author"

def test_search_found(client):
    new_author = create_new_author(client)
    author_id = new_author.get_json()["data"]["author_id"]
    
    response = client.get(
        f"{author_url}/search?search={first_name}"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Search result successful"
    author_id_result = data["data"][0]["author_id"]
    assert author_id_result == author_id

def test_search_invalid_url(client):
    response = client.get(
        f"{author_url}/search"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Search parameter is required!"

def test_get_empty_author(client):
    response = client.get(author_url)

    assert response.status_code == 200
    data = response.get_json()
    assert data["data"] is None
    assert data["message"] == "No available author"

def test_get_authors(client):
    create_new_author(client)

    response = client.get(author_url)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["data"]) == 1
    assert data["success"] is True
    assert data["data"][0]["first_name"] == first_name

def test_get_author(client):
    new_author = create_new_author(client)
    author_id = new_author.get_json()["data"]["author_id"]

    response = client.get(
        f"{author_url}/{author_id}"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Author retrieved successfuly"
    assert isinstance(data["data"]["author_id"], int)
    assert data["data"]["second_name"] == second_name

def test_author_not_found(client):
    response = client.get(
        f"{author_url}/{sample_id}"
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Author not found. Check author id"

def test_get_author_advices(client):
    new_author = create_new_author(client)
    author_id = new_author.get_json()["data"]["author_id"]
    create_new_advice(client)

    response = client.get(
        f"{author_url}/{author_id}/advices"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "All author advices"
    advices = data["data"]["advices"]
    assert len(advices) == 1

def test_author_no_advices(client):
    new_author = create_new_author(client)
    author_id = new_author.get_json()["data"]["author_id"]

    response = client.get(
        f"{author_url}/{author_id}/advices"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "No available advices for this author"

def test_create_new_author(client):
    response = create_new_author(client)

    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Author saved successfuly"
    assert isinstance(data["data"]["author_id"], int)

def test_no_json(client):
    response = client.post(author_url)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Request body must be JSON"
@pytest.mark.parametrize(
    "payload",
    invalid_payload_key
)
def test_create_key_validation(client, payload):
    response = create_new_author(
        client, json=payload, code=400
    )

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == " 'first_name' and 'second_name' field are required"

@pytest.mark.parametrize(
    "payload, error_message",
    invalid_payload_value
)
def test_create_value_validation(client, payload, error_message):
    response = create_new_author(
        client, json=payload, code=400
    )
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == error_message

def test_update_author(client):
    new_author = create_new_author(client)
    author_id = new_author.get_json()["data"]["author_id"]

    response = client.put(
        f"{author_url}/{author_id}", json=new_payload
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Author updated successfuly"

@pytest.mark.parametrize(
    "payload",
    invalid_payload_key
)
def test_update_key_validation(client, payload):
    new_author = create_new_author(client)
    author_id = new_author.get_json()["data"]["author_id"]

    response = client.put(
        f"{author_url}/{author_id}",
        json=payload
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == " 'first_name' and 'second_name' field are required"

@pytest.mark.parametrize(
    "payload, error_message",
    invalid_payload_value
)
def test_update_value_validation(client, payload, error_message):
    new_author = create_new_author(client)
    author_id = new_author.get_json()["data"]["author_id"]

    response = client.put(
        f"{author_url}/{author_id}",
        json=payload
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == error_message

def test_update_not_found(client):
    response = client.put(
        f"{author_url}/{sample_id}", json=new_payload
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Author not found. Check author id"

def test_delete_author(client):
    response = create_new_author(client)
    author_id = response.get_json()["data"]["author_id"]
    response = client.delete(f"{author_url}/{author_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Author deleted successfuly"

    response = client.get(f"{author_url}/{author_id}")
    assert response.status_code == 404

def test_delete_not_found(client):
    response = client.delete(f"{author_url}/{sample_id}")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Author not found. Check author id"

def test_delete_with_advices(client):
    new_author = create_new_author(client)
    author_id = new_author.get_json()["data"]["author_id"]
    create_new_advice(client)

    response = client.delete(
        f"{author_url}/{author_id}"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Cannot delete author because they still have advice."
