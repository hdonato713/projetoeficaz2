from unittest.mock import MagicMock, patch

import pytest

from app import app, connect_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("app.connect_db")
def test_listar_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    mock_cursor.fetchall.return_value = [
        (
            1,
            "Rua das Flores",
            "Rua",
            "Vila Mariana",
            "São Paulo",
            "04101-000",
            "apartamento",
            750000.0,
            "2024-01-15",
        )
    ]

    response = client.get("/imoveis")

    assert response.status_code == 200
    assert response.get_json() == {
        "imoveis": [
            {
                "id": 1,
                "logradouro": "Rua das Flores",
                "tipo_logradouro": "Rua",
                "bairro": "Vila Mariana",
                "cidade": "São Paulo",
                "cep": "04101-000",
                "tipo": "apartamento",
                "valor": 750000.0,
                "data_aquisicao": "2024-01-15",
            }
        ]
    }
    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis")

@patch("app.connect_db")
def test_listar_imoveis_sem_conexao(mock_connect_db, client):
    mock_connect_db.return_value = None

    response = client.get("/imoveis")

    assert response.status_code == 500
    assert response.get_json() == {
        "erro": "Erro ao conectar ao banco de dados"
    }

@patch("app.mysql.connector.connect")
def test_connect_db_retorna_conexao(mock_mysql_connect):
    mock_conn = MagicMock()
    mock_conn.is_connected.return_value = True
    mock_mysql_connect.return_value = mock_conn

    assert connect_db() is mock_conn