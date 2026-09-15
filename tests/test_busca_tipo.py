from unittest.mock import MagicMock, patch


def test_buscar_imoveis_por_tipo(client):
    conexao = MagicMock()
    cursor = MagicMock()
    conexao.cursor.return_value = cursor
    cursor.fetchall.return_value = [
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

    with patch("app.connect_db", return_value=conexao):
        resposta = client.get("/imoveis/tipo/apartamento")

    assert resposta.status_code == 200
    assert resposta.json == {
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
    cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE tipo = %s",
        ("apartamento",),
    )