# Global variables
base_url = "/advice"
author_url = "/author"
first_name = "john"
second_name = "James"
sample_id = 1

json_payload = {
    "advice": "Test before push to production",
    "author_id": sample_id
}
author_payload = {
    "first_name": first_name,
    "second_name": second_name
}
delete_payload = {
    "author_id": sample_id
}
new_json_payload = {
    "advice": " New test before push to production",
    "author_id": sample_id
}
empty_json = {}
empty_advice = {
    "advice": " ",
    "author_id": sample_id
}
invalid_key = {
    "advi": "Test before push to production",
    "author_id": sample_id
}
integer_advice = {
    "advice": 1234,
    "author_id": sample_id
}

# Helper function
def create_new_advice(client, json=json_payload, code=201):
    response = client.post(base_url, json=json)
    assert response.status_code == code
    return response

def create_new_author(client, json=author_payload, code=201):
    response = client.post(author_url, json=json)
    assert response.status_code == code
    return response

#---------------------TESTING----------------------
def test_get_empty_advices(client):
    response = client.get(base_url)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "No available advice"
    assert data["data"] is None


def test_get_all_advices(client):
    create_new_author(client)
    create_new_advice(client)
    response = client.get(base_url)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "All advices"
    assert data["data"][0]["advice"] == json_payload["advice"]

def test_get_advice_success(client):
    create_new_author(client)
    create_new_advice(client)
    
    response = client.get(f"{base_url}/{sample_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["advice_id"] == sample_id
    assert data["data"]["advice"] == json_payload["advice"]
    assert data["message"] == "Advice retrieved successfuly"


def test_advice_not_found(client):
    response = client.get(f"{base_url}/{sample_id}")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Advice not found. Check advice id"

def test_create_advice(client):
    create_new_author(client)
    response = create_new_advice(client)
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Advice saved successfuly"
    assert isinstance(data["data"]["advice_id"], int)
    assert data["data"]["advice"] == json_payload["advice"]

def test_create_empty_json(client):
    create_new_author(client)
    response = create_new_advice(client, 
        json=empty_json, 
        code=400)
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "'advice' and 'author_id' field is required"

def test_create_no_json(client):
    response = client.post(base_url)
    assert response.status_code == 400
    data = response.get_json()
    

def test_create_invalide_key(client):
    create_new_author(client)
    response = create_new_advice(client, 
        json=invalid_key,
        code=400)
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "'advice' and 'author_id' field is required"

def test_create_empty_advice(client):
    create_new_author(client)
    response = create_new_advice(client,
        json=empty_advice,
        code=400)
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Advice cannot be empty"

def test_create_advice_integer(client):
    create_new_author(client)
    response = create_new_advice(client,
        json=integer_advice,
        code=400)
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Advice must be a string"

def test_update_advice(client):
    create_new_author(client)
    create_new_advice(client)
    
    response = client.put(f"{base_url}/{sample_id}", 
        json=new_json_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Advice update successfuly"
    
    response = client.get(f"{base_url}/{sample_id}")
    data = response.get_json()
    assert data["data"]["advice"] == new_json_payload["advice"]

def test_update_not_found(client):
    response = client.put(f"{base_url}/{sample_id}", 
        json=new_json_payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Advice not found. Check advice id"

def test_update_invalid_payload(client):
    create_new_author(client)
    create_new_advice(client)
    response = client.put(f"{base_url}/{sample_id}", 
        json=invalid_key)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "'advice' and 'author_id' field is required"

def test_delete_advice(client):
    create_new_author(client)
    create_new_advice(client)
    response = client.delete(f"{base_url}/{sample_id}", json=delete_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Advice deleted successfuly"
    response = client.get("/advice/1")
    assert response.status_code == 404

def test_delete_not_found(client):
    response = client.delete(f"{base_url}/{sample_id}")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "ERROR!! Advice not found. Check advice id"
