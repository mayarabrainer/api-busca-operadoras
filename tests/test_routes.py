import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"status": "ok", "message": "API is operational"}

def test_search_operators(client, mocker):
    mock_operators = [
        {
            "Razao_Social": "Empresa X",
            "CNPJ": "12345678000190",
            "Cidade": "Sao Paulo",
            "UF": "SP",
            "Telefone": "(11) 987654321",
            "Endereco_eletronico": "email@empresax.com"
        }
    ]

    mocker.patch("app.load_operators", return_value=mock_operators)

    response = client.get('/search_operators?q=Empresa X')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["Business_Name"] == "Empresa X"

    response = client.get('/search_operators?q=12345678000190')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["CNPJ"] == "12345678000190"

    response = client.get('/search_operators?q=Inexistente')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []