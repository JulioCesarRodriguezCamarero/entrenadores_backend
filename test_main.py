import pytest
from fastapi.testclient import TestClient
from app.main import app  # Asegúrate de que la ruta a tu aplicación sea correcta

client = TestClient(app)


def test_read_client_info():
    # Adjust "1" with a valid cliente_id from your database
    response = client.get("/clientes_info/8/")

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the returned JSON structure matches the expected schema
    json_response = response.json()
    assert "cliente_id" in json_response
    assert "cliente_nombre" in json_response
    assert "entrenador" in json_response
    assert "rutinas" in json_response
    assert "nutricion" in json_response


if __name__ == "__main__":
    pytest.main()
