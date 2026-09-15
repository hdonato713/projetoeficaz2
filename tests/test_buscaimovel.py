from unittest.mock import MagicMock, patch


def test_busca_imovel_por_id(client):
    conexao_mock = MagicMock()
    cursor_mock = MagicMock()

    conexao_mock.cursor.return_value = cursor_mock

    cursor_mock.fetchone.return_value = (
        1,
        "Avenida Paulista",
        "Avenida",
        "Bela Vista",
        "São Paulo",
        "01310-100",
        "Apartamento",
        850000.00,
        "2024-01-15",
    )

    with patch("app.connect_db", return_value=conexao_mock):
        resposta = client.get("/imoveis/1")

    assert resposta.status_code == 200
    assert resposta.get_json() == {
        "id": 1,
        "logradouro": "Avenida Paulista",
        "tipo_logradouro": "Avenida",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "cep": "01310-100",
        "tipo": "Apartamento",
        "valor": 850000.00,
        "data_aquisicao": "2024-01-15",
    }

    cursor_mock.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (1,),
    )