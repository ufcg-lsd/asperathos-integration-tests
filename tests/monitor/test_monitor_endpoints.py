import requests

def test_invalid_get():
    response = requests.get("http://localhost:1501/")
    assert response.status_code == 404

def test_invalid_post():
    response = requests.post("http://localhost:1501/", {})
    assert response.status_code == 404

def test_invalid_delete():
    response = requests.delete("http://localhost:1501/")
    assert response.status_code == 404

def test_invalid_put():
    response = requests.put("http://localhost:1501/", {})
    assert response.status_code == 404
