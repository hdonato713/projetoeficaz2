from unittest.mock import MagicMock, patch

def test_busca_imovel_por_id(client):
    conexao_mock = MagicMock()
    cursor_mock = MagicMock()

    conexao_mock.cursor.return_value = cursor_mock
    cursor_mock.fetchone.return_value = {
        "id": 1,
        "tipo": "Apartamento",
        "cidade": "São Paulo"
    }

    with patch("app.connect_db", return_value=conexao_mock):
        resposta = client.get("/imoveis/1")

    assert resposta.status_code == 200
    assert resposta.get_json() == {
        "id": 1,
        "tipo": "Apartamento",
        "cidade": "São Paulo"
    }

    cursor_mock.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (1,)
    )