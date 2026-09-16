from unittest.mock import MagicMock, patch


def test_buscar_imoveis_por_cidade(client):
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
        resposta = client.get("/imoveis/cidade/São Paulo")

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
                "_links": {
                    "self": {"href": "/imoveis/1", "method": "GET"},
                    "update": {"href": "/imoveis/1", "method": "PUT"},
                    "delete": {"href": "/imoveis/1", "method": "DELETE"},
                    "collection": {"href": "/imoveis", "method": "GET"},
                },
            }
        ],
        "_links": {
            "self": {
                "href": "/imoveis/cidade/S%C3%A3o%20Paulo",
                "method": "GET",
            },
            "collection": {"href": "/imoveis", "method": "GET"},
            "create": {"href": "/imoveis", "method": "POST"},
        },
    }
    cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE cidade = %s",
        ("São Paulo",),
    )


def test_buscar_imoveis_por_cidade_sem_resultados(client):
    conexao = MagicMock()
    cursor = MagicMock()
    conexao.cursor.return_value = cursor
    cursor.fetchall.return_value = []

    with patch("app.connect_db", return_value=conexao):
        resposta = client.get("/imoveis/cidade/Recife")

    assert resposta.status_code == 200
    assert resposta.json == {
        "imoveis": [],
        "_links": {
            "self": {"href": "/imoveis/cidade/Recife", "method": "GET"},
            "collection": {"href": "/imoveis", "method": "GET"},
            "create": {"href": "/imoveis", "method": "POST"},
        },
    }


def test_buscar_imoveis_por_cidade_sem_conexao(client):
    with patch("app.connect_db", return_value=None):
        resposta = client.get("/imoveis/cidade/São Paulo")

    assert resposta.status_code == 500
    assert resposta.json == {"erro": "Erro ao conectar ao banco de dados"}
