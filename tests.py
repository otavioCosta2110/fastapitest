from unittest.mock import patch
import requests

def test_healthcheck():
    url = 'http://localhost:8000/'
    res = requests.get(url)
    assert res.status_code == 200

def test_list_users():
    url = 'http://localhost:8000/list'
    res = requests.get(url)
    assert res.status_code == 200

@patch('requests.post')
def test_create_user(mock_post):
    mock_response = { "message": "User created successfully" }
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.status_code = 200
    url = 'http://localhost:8000/create'
    userBody = {
        "name": "otavio",
        "email": "otavio@email.com",
        "password": "senha123"
    }

    response = requests.post(url, json=userBody)

    assert response.status_code == 200
    assert response.json()['message'] == "User created successfully"

@patch('requests.delete')
def test_delete_user(mock_delete):
    mock_response = { "message": "User deleted successfully" }
    mock_delete.return_value.json.return_value = mock_response
    mock_delete.return_value.status_code = 200
    user_id = 12
    url = f'http://localhost:8000/delete/{user_id}'

    response = requests.delete(url)

    assert response.status_code == 200
    assert response.json()['message'] == "User deleted successfully"

@patch('requests.put')
def test_update_user(mock_update):
    mock_response = { "message": "User updated successfully" }
    mock_update.return_value.json.return_value = mock_response
    mock_update.return_value.status_code = 200
    url = 'http://localhost:8000/delete/'
    userBody = {
        "email": "otavio@email.com",
        "name": "joao",
        "password": "senha123"
    }

    response = requests.put(url, json=userBody)

    assert response.status_code == 200
    assert response.json()['message'] == "User updated successfully"
