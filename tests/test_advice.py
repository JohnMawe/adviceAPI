import pytest

# Global variables
advice_url = "/advice"
author_url = "/author"
first_name = "john"
second_name = "James"
sample_id = 1

json_payload = {
    "advice": "Test before push to production",
}
author_payload = {
    "first_name": first_name,
    "second_name": second_name
}
new_json_payload = {
    "advice": " New test before push to production"
}
empty_advice = {
    "advice": " "
}
invalid_key = {
    "advi": "Test before push to production"
}
integer_advice = {
    "advice": 1234
}

# Helper function
def create_new_advice(client, json, code=201):
    response = client.post(advice_url, json=json)
    assert response.status_code == code
    return response

def create_new_author(client, json=author_payload, code=201):
    response = client.post(author_url, json=json)
    assert response.status_code == code
    return response.get_json()["data"]["author_id"]


#---------------------TESTING------------------------
def test_search_no_result(client):
    response = client.get(
        f"{advice_url}/search?search=test"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "No matching advice"

def test_search_found(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    advice_respo = create_new_advice(
        client, json_payload
    )
    advice_id = advice_respo.get_json()["data"]["advice_id"]

    response = client.get(
        f"{advice_url}/search?search=test"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Search result successful"
    advice_id_result = data["data"][0]["advice_id"]
    assert advice_id_result == advice_id

def test_search_invalid_url(client):
    response = client.get(
        f"{advice_url}/search"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Search parameter is required!"

def test_get_empty_advices(client):
    response = client.get(advice_url)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "No available advice"
    assert data["data"] is None


def test_get_advices(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    create_new_advice(client, json_payload)
    
    response = client.get(advice_url)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "All advices"
    assert data["data"][0]["advice"] == json_payload["advice"]

def test_get_advice_success(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    new_advice = create_new_advice(
        client, json_payload
    )
    advice_id = new_advice.get_json()["data"]["advice_id"]

    response = client.get(f"{advice_url}/{advice_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert isinstance(data["data"]["advice_id"], int)
    assert data["data"]["advice"] == json_payload["advice"]
    assert data["message"] == "Advice retrieved successfully"


def test_advice_not_found(client):
    response = client.get(f"{advice_url}/{sample_id}")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Advice not found. Check advice id"

def test_create_advice(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    response = create_new_advice(
        client, json_payload
    )
    
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Advice saved successfully"
    assert isinstance(data["data"]["advice_id"], int)
    assert data["data"]["advice"] == json_payload["advice"]

def test_empty_json(client):
    create_new_author(client)
    response = create_new_advice(client, 
        json={}, 
        code=400)
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "'advice' and 'author_id' field are required"

def test_no_json(client):
    response = client.post(advice_url)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Request body must be JSON"
@pytest.mark.parametrize(
    "payload, error_message",
    [
        pytest.param(
            empty_advice,
            "Advice cannot be empty",
            id="empty_advice"
        ),
        pytest.param(
            integer_advice,
            "Advice must be a string",
            id="integer_advice"
        ),
        pytest.param(
            invalid_key,
            "'advice' and 'author_id' field are required",
            id="invalid_key"
        )

    ]
)
def test_create_empty_advice(client, payload, error_message):
    author_id = create_new_author(client)
    payload["author_id"] = author_id
    response = create_new_advice(client,
        json=payload,
        code=400)
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == error_message

def test_create_author_not_exist(client):
    json_payload["author_id"] = sample_id
    response = create_new_advice(
        client, json_payload, code=404
    )
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Author not found. Check author id"
    

def test_update_advice(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    new_advice = create_new_advice(
        client, json_payload
    )
    advice_id = new_advice.get_json()["data"]["advice_id"]

    new_json_payload["author_id"] = author_id
    response = client.put(
        f"{advice_url}/{advice_id}",
        json=new_json_payload
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Advice update successfully"
    response = client.get(
        f"{advice_url}/{advice_id}"
    )
    data = response.get_json()
    assert data["data"]["advice"] == new_json_payload["advice"]

def test_update_not_found(client):
    response = client.put(
        f"{advice_url}/{sample_id}",
        json=new_json_payload
    )
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Advice not found. Check advice id"

def test_update_invalid_payload(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    new_advice = create_new_advice(
        client, json_payload
    )
    advice_id = new_advice.get_json()["data"]["advice_id"]
    
    response = client.put(
        f"{advice_url}/{advice_id}",
        json=invalid_key
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "'advice' and 'author_id' field are required"

def test_update_author_not_exist(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    new_advice = create_new_advice(
        client, json_payload
    )
    advice_id = new_advice.get_json()["data"]["advice_id"]

    new_json_payload["author_id"] = sample_id + 1
    response = client.put(
        f"{advice_url}/{advice_id}",
        json=new_json_payload
    )
    assert response.status_code == 404

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Author not found. Check author id"

def test_delete_advice(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    delete_payload = {
        "author_id": author_id
    }
    new_advice = create_new_advice(
        client, json_payload
    )
    advice_id = new_advice.get_json()["data"]["advice_id"]
    
    response = client.delete(
        f"{advice_url}/{advice_id}", json=delete_payload
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Advice deleted successfully"
    response = client.get("/advice/1")
    assert response.status_code == 404

def test_delete_not_found(client):
    response = client.delete(f"{advice_url}/{sample_id}")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Advice not found. Check advice id"

def test_delete_invalid_key(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    delete_payload = {
        "author": author_id
    }
    new_advice = create_new_advice(
        client, json_payload
    )
    advice_id = new_advice.get_json()["data"]["advice_id"]
    
    response = client.delete(
        f"{advice_url}/{advice_id}", json=delete_payload
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == " 'author_id' field is required"

def test_delete_no_payload(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    new_advice = create_new_advice(
        client, json_payload
    )
    advice_id = new_advice.get_json()["data"]["advice_id"]
    
    response = client.delete(
        f"{advice_url}/{advice_id}"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Request body must be JSON"


def test_delete_author_not_exist(client):
    author_id = create_new_author(client)
    json_payload["author_id"] = author_id
    new_advice = create_new_advice(
        client, json_payload
    )
    advice_id = new_advice.get_json()["data"]["advice_id"]

    new_json_payload["author_id"] = sample_id + 1
    response = client.delete(
        f"{advice_url}/{advice_id}",
        json=new_json_payload
    )
    assert response.status_code == 404

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Author not found. Check author id"
